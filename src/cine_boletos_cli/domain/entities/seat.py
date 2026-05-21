"""
seat.py

Entidad de dominio que representa un asiento dentro de una función de cine.

El asiento controla su propio estado y protege las reglas básicas de negocio
relacionadas con disponibilidad, bloqueo temporal y compra.

Esta entidad NO conoce detalles de infraestructura como base de datos,
Redis, workers o CLI.
"""

from datetime import datetime

from cine_boletos_cli.domain.exceptions.domain_errors import (
    InvalidSeatStateTransitionError,
    SeatAlreadyBookedError,
    SeatLockedError,
    SeatNotAvailableError,
)
from cine_boletos_cli.shared.constants import (
    AVAILABLE,
    BOOKED,
    LOCKED,
)


class Seat:
    """
    Representa un asiento perteneciente a una función.

    Parameters
    ----------
    seat_id : SeatId
        Identificador formal del asiento.

    showtime_id : str
        Identificador de la función.

    status : str
        Estado actual del asiento.

    lock_id : str | None, optional
        Identificador del lock activo.

    locked_until : datetime | None, optional
        Fecha de expiración del lock.
    """

    def __init__(
        self,
        seat_id,
        showtime_id,
        status=AVAILABLE,
        lock_id=None,
        locked_until=None,
    ):
        self.seat_id = seat_id
        self.showtime_id = showtime_id
        self.status = status
        self.lock_id = lock_id
        self.locked_until = locked_until

    def is_available(self):
        """
        Indica si el asiento está disponible.

        Returns
        -------
        bool
            True si el asiento está libre.
        """

        if self.status == LOCKED and self.is_lock_expired():
            self.unlock()

        return self.status == AVAILABLE

    def is_lock_expired(self):
        """
        Indica si el bloqueo actual del asiento ya expiró.

        Returns
        -------
        bool
            True si el lock venció.
            False en cualquier otro caso.
        """

        if self.status != LOCKED:
            return False

        if self.locked_until is None:
            return False

        return datetime.utcnow() > self.locked_until

    def lock(self, lock_id, locked_until):
        """
        Bloquea temporalmente el asiento.

        Parameters
        ----------
        lock_id : str
            Identificador único del lock.

        locked_until : datetime
            Fecha de expiración del lock.

        Raises
        ------
        SeatAlreadyBookedError
            Si el asiento ya fue comprado.

        SeatLockedError
            Si el asiento ya está bloqueado.
        """

        if self.status == LOCKED and self.is_lock_expired():
            self.unlock()

        if self.status == BOOKED:
            raise SeatAlreadyBookedError(
                "No se puede bloquear un asiento ya comprado."
            )

        if self.status == LOCKED:
            raise SeatLockedError(
                "El asiento ya se encuentra bloqueado."
            )

        self.validate_transition(LOCKED)

        self.status = LOCKED
        self.lock_id = lock_id
        self.locked_until = locked_until

    def unlock(self):
        """
        Libera el lock actual del asiento.

        Raises
        ------
        InvalidSeatStateTransitionError
            Si el asiento no está bloqueado.
        """

        if self.status != LOCKED:
            raise InvalidSeatStateTransitionError(
                "Solo un asiento bloqueado puede liberarse."
            )

        self.validate_transition(AVAILABLE)

        self.status = AVAILABLE
        self.lock_id = None
        self.locked_until = None

    def book(self):
        """
        Marca el asiento como comprado.

        Raises
        ------
        SeatNotAvailableError
            Si el asiento no estaba bloqueado correctamente.

        SeatLockedError
            Si el lock expiró antes de confirmar la compra.
        """

        if self.status != LOCKED:
            raise SeatNotAvailableError(
                "El asiento debe estar bloqueado antes de comprarse."
            )

        if self.is_lock_expired():
            self.unlock()

            raise SeatLockedError(
                "El lock del asiento expiró."
            )

        self.validate_transition(BOOKED)

        self.status = BOOKED
        self.lock_id = None
        self.locked_until = None

    def validate_transition(self, new_status):
        """
        Valida si una transición de estado es válida.

        Parameters
        ----------
        new_status : str
            Nuevo estado solicitado.

        Raises
        ------
        InvalidSeatStateTransitionError
            Si la transición no está permitida.
        """

        valid_transitions = {
            AVAILABLE: [LOCKED],
            LOCKED: [AVAILABLE, BOOKED],
            BOOKED: [],
        }

        allowed = valid_transitions.get(self.status, [])

        if new_status not in allowed:
            raise InvalidSeatStateTransitionError(
                f"Transición inválida: {self.status} -> {new_status}"
            )

        return True
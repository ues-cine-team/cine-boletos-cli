"""
showtime.py

Entidad de dominio que representa una función de cine.

Showtime encapsula reglas relacionadas con:
- programación de funciones,
- disponibilidad temporal,
- control de estados,
- precio base de boletos,
- y vigencia de la función.

Esta entidad NO conoce detalles de infraestructura como:
- base de datos,
- Redis,
- workers,
- CLI,
- sistemas de pago.

La disponibilidad de asientos por función se modela en otra entidad,
por ejemplo ShowtimeSeat.
"""

from datetime import datetime, timedelta
from typing import Optional

from cine_boletos_cli.domain.exceptions.domain_errors import (
    InvalidBookingStateError,
)
from cine_boletos_cli.domain.value_objects.money import Money
from cine_boletos_cli.shared.constants import (
    SHOWTIME_ACTIVE,
    SHOWTIME_CANCELLED,
    SHOWTIME_FINISHED,
    SHOWTIME_SCHEDULED,
)


class Showtime:
    """
    Representa una función de cine dentro del sistema.

    Parameters
    ----------
    showtime_id : str
        Identificador único de la función.

    movie_id : str
        Identificador de la película.

    room_id : str
        Identificador de la sala.

    starts_at : datetime
        Fecha y hora de inicio.

    duration_minutes : int
        Duración de la función en minutos.

    base_price : Money
        Precio base del boleto.

    status : str, optional
        Estado actual de la función.

    ends_at : datetime | None, optional
        Fecha de finalización de la función.

    created_at : datetime | None, optional
        Fecha de creación.

    updated_at : datetime | None, optional
        Fecha de última actualización.
    """

    VALID_STATUSES = {
        SHOWTIME_SCHEDULED,
        SHOWTIME_ACTIVE,
        SHOWTIME_FINISHED,
        SHOWTIME_CANCELLED,
    }

    def __init__(
        self,
        showtime_id: str,
        movie_id: str,
        room_id: str,
        starts_at: datetime,
        duration_minutes: int,
        base_price: Money,
        status: str = SHOWTIME_SCHEDULED,
        ends_at: Optional[datetime] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        if not showtime_id:
            raise ValueError("showtime_id no puede estar vacío.")

        if not movie_id:
            raise ValueError("movie_id no puede estar vacío.")

        if not room_id:
            raise ValueError("room_id no puede estar vacío.")

        if duration_minutes <= 0:
            raise ValueError(
                "duration_minutes debe ser mayor que cero."
            )

        if starts_at is None:
            raise ValueError("starts_at no puede ser None.")

        if base_price is None:
            raise ValueError("base_price no puede ser None.")

        if status not in self.VALID_STATUSES:
            raise ValueError(f"Estado inválido: {status}")

        computed_ends_at = starts_at + timedelta(
            minutes=duration_minutes
        )

        if ends_at is not None and ends_at <= starts_at:
            raise ValueError(
                "ends_at debe ser mayor que starts_at."
            )

        if ends_at is not None and ends_at != computed_ends_at:
            raise ValueError(
                "ends_at no coincide con starts_at + duration_minutes."
            )

        self.showtime_id = showtime_id
        self.movie_id = movie_id
        self.room_id = room_id

        self.starts_at = starts_at
        self.duration_minutes = duration_minutes
        self.ends_at = ends_at or computed_ends_at

        self.base_price = base_price
        self.status = status

        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or self.created_at

    def has_started(self, now: Optional[datetime] = None) -> bool:
        """
        Indica si la función ya comenzó.
        """
        now = now or datetime.utcnow()
        return now >= self.starts_at

    def has_finished(self, now: Optional[datetime] = None) -> bool:
        """
        Indica si la función ya terminó.
        """
        now = now or datetime.utcnow()
        return now >= self.ends_at

    def is_active(self, now: Optional[datetime] = None) -> bool:
        """
        Indica si la función sigue activa.
        """
        now = now or datetime.utcnow()
        return self.status == SHOWTIME_ACTIVE and now < self.ends_at

    def is_scheduled(self) -> bool:
        """
        Indica si la función sigue programada.
        """
        return self.status == SHOWTIME_SCHEDULED

    def is_cancelled(self) -> bool:
        """
        Indica si la función fue cancelada.
        """
        return self.status == SHOWTIME_CANCELLED

    def is_finished(self) -> bool:
        """
        Indica si la función fue finalizada.
        """
        return self.status == SHOWTIME_FINISHED

    def change_status(self, new_status: str):
        """
        Cambia el estado de la función.
        """
        self._validate_transition(new_status)
        self.status = new_status
        self.updated_at = datetime.utcnow()

    def activate(self, now: Optional[datetime] = None):
        """
        Marca la función como activa.
        """
        now = now or datetime.utcnow()

        if now < self.starts_at:
            raise InvalidBookingStateError(
                "No se puede activar una función antes de starts_at."
            )

        self.change_status(SHOWTIME_ACTIVE)

    def finish(self, now: Optional[datetime] = None):
        """
        Marca la función como finalizada.
        """
        now = now or datetime.utcnow()

        if not self.has_started(now):
            raise InvalidBookingStateError(
                "No se puede finalizar una función que aún no inicia."
            )

        self.change_status(SHOWTIME_FINISHED)

    def cancel(self):
        """
        Cancela la función.
        """
        self.change_status(SHOWTIME_CANCELLED)

    def change_price(self, new_price: Money):
        """
        Actualiza el precio base de la función.
        """
        if new_price is None:
            raise ValueError("new_price no puede ser None.")

        self.base_price = new_price
        self.updated_at = datetime.utcnow()

    def _validate_transition(self, new_status: str):
        """
        Valida si una transición de estado es permitida.
        """
        valid_transitions = {
            SHOWTIME_SCHEDULED: [
                SHOWTIME_ACTIVE,
                SHOWTIME_CANCELLED,
            ],
            SHOWTIME_ACTIVE: [
                SHOWTIME_FINISHED,
                SHOWTIME_CANCELLED,
            ],
            SHOWTIME_FINISHED: [],
            SHOWTIME_CANCELLED: [],
        }

        allowed = valid_transitions.get(self.status, [])

        if new_status not in allowed:
            raise InvalidBookingStateError(
                f"Transición inválida: {self.status} -> {new_status}"
            )

        return True

    def __repr__(self):
        return (
            "Showtime("
            f"showtime_id={self.showtime_id!r}, "
            f"movie_id={self.movie_id!r}, "
            f"room_id={self.room_id!r}, "
            f"starts_at={self.starts_at!r}, "
            f"ends_at={self.ends_at!r}, "
            f"status={self.status!r})"
        )
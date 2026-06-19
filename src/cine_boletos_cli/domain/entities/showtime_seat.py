"""
showtime_seat.py

Entidad de dominio que representa un asiento específico
dentro de una función de cine.

Un Seat representa un asiento físico.

Un ShowtimeSeat representa el estado de ese asiento
para una función concreta.

Ejemplo:

Seat:
    A1

Showtime:
    Batman 2026-06-20 18:00

ShowtimeSeat:
    A1
    AVAILABLE
"""

from datetime import datetime
from typing import Optional

from cine_boletos_cli.shared.constants import (
    SEAT_AVAILABLE,
    SEAT_BOOKED,
    SEAT_LOCKED,
)


class ShowtimeSeat:
    """
    Representa un asiento dentro de una función.

    Parameters
    ----------
    showtime_seat_id : str
        Identificador único.

    showtime_id : str
        Identificador de la función.

    seat_id : str
        Identificador del asiento físico.

    status : str, optional
        Estado actual del asiento.
    """

    VALID_STATUSES = {
        SEAT_AVAILABLE,
        SEAT_LOCKED,
        SEAT_BOOKED,
    }

    def __init__(
        self,
        showtime_seat_id: str,
        showtime_id: str,
        seat_id: str,
        status: str = SEAT_AVAILABLE,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        if not showtime_seat_id:
            raise ValueError(
                "showtime_seat_id no puede estar vacío."
            )

        if not showtime_id:
            raise ValueError(
                "showtime_id no puede estar vacío."
            )

        if not seat_id:
            raise ValueError(
                "seat_id no puede estar vacío."
            )

        if status not in self.VALID_STATUSES:
            raise ValueError(
                f"Estado inválido: {status}"
            )

        self.showtime_seat_id = showtime_seat_id
        self.showtime_id = showtime_id
        self.seat_id = seat_id
        self.status = status

        self.created_at = (
            created_at or datetime.utcnow()
        )

        self.updated_at = (
            updated_at or self.created_at
        )

    def is_available(self) -> bool:
        """
        Indica si el asiento está disponible.
        """
        return self.status == SEAT_AVAILABLE

    def is_locked(self) -> bool:
        """
        Indica si el asiento está bloqueado.
        """
        return self.status == SEAT_LOCKED

    def is_booked(self) -> bool:
        """
        Indica si el asiento fue vendido.
        """
        return self.status == SEAT_BOOKED

    def lock(self):
        """
        AVAILABLE -> LOCKED
        """
        if self.status != SEAT_AVAILABLE:
            raise ValueError(
                "Solo un asiento disponible puede bloquearse."
            )

        self.status = SEAT_LOCKED
        self.updated_at = datetime.utcnow()

    def release(self):
        """
        LOCKED -> AVAILABLE
        """
        if self.status != SEAT_LOCKED:
            raise ValueError(
                "Solo un asiento bloqueado puede liberarse."
            )

        self.status = SEAT_AVAILABLE
        self.updated_at = datetime.utcnow()

    def cancel_booking(self):
        """
        BOOKED -> AVAILABLE

        Se utiliza cuando una reserva confirmada
        es cancelada y los asientos deben volver
        a quedar disponibles.
        """
        if self.status != SEAT_BOOKED:
            raise ValueError(
                "Solo un asiento comprado puede liberarse por cancelación."
            )

        self.status = SEAT_AVAILABLE

        self.updated_at = datetime.utcnow()

    def book(self):
        """
        LOCKED -> BOOKED
        """
        if self.status != SEAT_LOCKED:
            raise ValueError(
                "Solo un asiento bloqueado puede comprarse."
            )

        self.status = SEAT_BOOKED
        self.updated_at = datetime.utcnow()
        
    def __repr__(self):
        return (
            "ShowtimeSeat("
            f"showtime_seat_id={self.showtime_seat_id!r}, "
            f"showtime_id={self.showtime_id!r}, "
            f"seat_id={self.seat_id!r}, "
            f"status={self.status!r}"
            ")"
        )
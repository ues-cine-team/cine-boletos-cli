"""
booking.py

Entidad de dominio que representa una reserva de boletos.
"""

from datetime import datetime
from typing import Optional

from cine_boletos_cli.domain.exceptions.domain_errors import (
    BookingAlreadyCancelledError,
    BookingAlreadyConfirmedError,
    InvalidBookingStateError,
)

from cine_boletos_cli.shared.constants import (
    BOOKING_CANCELLED,
    BOOKING_CONFIRMED,
    BOOKING_PENDING,
    PAYMENT_FAILED,
    PAYMENT_PAID,
    PAYMENT_PENDING,
)


class Booking:
    """
    Entidad del dominio que representa una reserva o compra.
    """

    def __init__(
        self,
        booking_id,
        customer_id,
        showtime_id,
        seat_ids,
        total_amount,
        status,
        payment_status,
        created_at: datetime,
        updated_at: Optional[datetime] = None,
        idempotency_key: Optional[str] = None,
    ):
        self.booking_id = booking_id

        self.customer_id = customer_id

        self.showtime_id = showtime_id

        self.seat_ids = seat_ids

        self.total_amount = total_amount

        self.status = status

        self.payment_status = payment_status

        self.created_at = created_at

        self.updated_at = updated_at or created_at

        self.idempotency_key = idempotency_key

    def calculate_total(self):
        """
        Devuelve el total actual del booking.
        """

        return self.total_amount

    def confirm(self):
        """
        Confirma la reserva.
        """

        if self.status == BOOKING_CANCELLED:
            raise BookingAlreadyCancelledError(
                "No puede confirmarse un booking cancelado."
            )

        if self.status == BOOKING_CONFIRMED:
            raise BookingAlreadyConfirmedError(
                "El booking ya fue confirmado."
            )

        self.validate_transition(
            BOOKING_CONFIRMED
        )

        self.status = BOOKING_CONFIRMED

        self.updated_at = datetime.utcnow()

    def cancel(self):
        """
        Cancela la reserva.

        Para el MVP permitimos cancelar bookings:
        - PENDING
        - CONFIRMED

        La liberación de asientos se coordina desde BookingService.
        """

        if self.status == BOOKING_CANCELLED:
            raise BookingAlreadyCancelledError(
                "El booking ya fue cancelado."
            )

        self.validate_transition(
            BOOKING_CANCELLED
        )

        self.status = BOOKING_CANCELLED

        self.updated_at = datetime.utcnow()

    def mark_payment_pending(self):
        """
        Marca el pago como pendiente.
        """

        self.payment_status = PAYMENT_PENDING

        self.updated_at = datetime.utcnow()

    def mark_paid(self):
        """
        Marca el pago como completado.
        """

        self.payment_status = PAYMENT_PAID

        self.updated_at = datetime.utcnow()

    def mark_failed(self):
        """
        Marca el pago como fallido.
        """

        self.payment_status = PAYMENT_FAILED

        self.updated_at = datetime.utcnow()

    def is_cancellable(self):
        """
        Indica si el booking puede cancelarse.
        """

        return self.status in [
            BOOKING_PENDING,
            BOOKING_CONFIRMED,
        ]

    def validate_transition(
        self,
        new_status,
    ):
        """
        Valida transiciones de estado.
        """

        valid_transitions = {
            BOOKING_PENDING: [
                BOOKING_CONFIRMED,
                BOOKING_CANCELLED,
            ],
            BOOKING_CONFIRMED: [
                BOOKING_CANCELLED,
            ],
            BOOKING_CANCELLED: [],
        }

        allowed = valid_transitions.get(
            self.status,
            [],
        )

        if new_status not in allowed:
            raise InvalidBookingStateError(
                f"Transición inválida: "
                f"{self.status} -> {new_status}"
            )

        return True
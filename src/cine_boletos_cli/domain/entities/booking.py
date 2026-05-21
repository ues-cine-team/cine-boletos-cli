"""
booking.py

Entidad de dominio que representa una reserva o compra de boletos.

Booking encapsula las reglas principales relacionadas con:
- estado de la reserva,
- estado del pago,
- confirmación,
- cancelación,
- consistencia de la compra.

Esta entidad NO conoce detalles de infraestructura como base de datos,
pasarelas de pago, Redis, workers o CLI.
"""

from datetime import datetime

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
    Representa una reserva de boletos dentro del sistema.

    Parameters
    ----------
    booking_id : str
        Identificador único de la reserva.

    customer_id : str
        Identificador del cliente.

    showtime_id : str
        Identificador de la función.

    seat_ids : list
        Lista de asientos asociados.

    total_amount : Money
        Monto total de la reserva.

    status : str
        Estado actual del booking.

    payment_status : str
        Estado actual del pago.

    created_at : datetime
        Fecha de creación.

    updated_at : datetime, optional
        Fecha de última modificación.

    idempotency_key : str, optional
        Clave de idempotencia de la operación.
    """

    def __init__(
        self,
        booking_id,
        customer_id,
        showtime_id,
        seat_ids,
        total_amount,
        status=BOOKING_PENDING,
        payment_status=PAYMENT_PENDING,
        created_at=None,
        updated_at=None,
        idempotency_key=None,
    ):
        self.booking_id = booking_id
        self.customer_id = customer_id
        self.showtime_id = showtime_id
        self.seat_ids = seat_ids
        self.total_amount = total_amount

        self.status = status
        self.payment_status = payment_status

        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or self.created_at

        self.idempotency_key = idempotency_key

    def calculate_total(self):
        """
        Devuelve el monto total de la reserva.

        Returns
        -------
        Money
            Total asociado al booking.
        """

        return self.total_amount

    def confirm(self):
        """
        Confirma la reserva.

        Raises
        ------
        BookingAlreadyCancelledError
            Si la reserva ya fue cancelada.

        BookingAlreadyConfirmedError
            Si la reserva ya fue confirmada.

        InvalidBookingStateError
            Si el pago todavía no fue completado.
        """

        if self.status == BOOKING_CANCELLED:
            raise BookingAlreadyCancelledError(
                "No se puede confirmar una reserva cancelada."
            )

        if self.status == BOOKING_CONFIRMED:
            raise BookingAlreadyConfirmedError(
                "La reserva ya fue confirmada."
            )

        if self.payment_status != PAYMENT_PAID:
            raise InvalidBookingStateError(
                "La reserva no puede confirmarse sin pago exitoso."
            )

        self.validate_transition(BOOKING_CONFIRMED)

        self.status = BOOKING_CONFIRMED
        self.updated_at = datetime.utcnow()

    def cancel(self):
        """
        Cancela la reserva.

        Raises
        ------
        BookingAlreadyCancelledError
            Si la reserva ya fue cancelada.

        BookingAlreadyConfirmedError
            Si la reserva ya fue confirmada.
        """

        if self.status == BOOKING_CANCELLED:
            raise BookingAlreadyCancelledError(
                "La reserva ya fue cancelada."
            )

        if self.status == BOOKING_CONFIRMED:
            raise BookingAlreadyConfirmedError(
                "No se puede cancelar una reserva confirmada."
            )

        self.validate_transition(BOOKING_CANCELLED)

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
        Marca el pago como exitoso.
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
        Indica si la reserva todavía puede cancelarse.

        Returns
        -------
        bool
            True si el booking sigue pendiente.
        """

        return self.status == BOOKING_PENDING

    def validate_transition(self, new_status):
        """
        Valida si una transición de estado es válida.

        Parameters
        ----------
        new_status : str
            Estado destino.

        Raises
        ------
        InvalidBookingStateError
            Si la transición no es válida.
        """

        valid_transitions = {
            BOOKING_PENDING: [
                BOOKING_CONFIRMED,
                BOOKING_CANCELLED,
            ],
            BOOKING_CONFIRMED: [],
            BOOKING_CANCELLED: [],
        }

        allowed = valid_transitions.get(self.status, [])

        if new_status not in allowed:
            raise InvalidBookingStateError(
                f"Transición inválida: "
                f"{self.status} -> {new_status}"
            )

        return True
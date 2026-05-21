"""booking.py

Entidad de dominio que representa una reserva de boletos.

Booking agrupa los asientos reservados por un cliente para una función
específica y protege las reglas del estado de la reserva.

Responsibilities
----------------
- representar una reserva o compra,
- mantener consistencia entre asientos, total y estado,
- permitir confirmar o cancelar de forma válida,
- marcar el estado del pago de la reserva,
- evitar transiciones ilegales.

Notes
-----
Esta entidad NO debe:
- cobrar pagos,
- acceder a bases de datos,
- hablar con la consola,
- coordinar infraestructura externa.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional, Sequence

from cine_boletos_cli.domain.exceptions.domain_errors import (
    BookingAlreadyCancelledError,
    BookingAlreadyConfirmedError,
    InvalidBookingStateTransitionError,
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
    """Entidad del dominio que representa una reserva o compra de boletos.

    Parameters
    ----------
    booking_id : Any
        Identificador único de la reserva.
    customer_id : Any
        Identificador del cliente que realizó la reserva.
    showtime_id : Any
        Identificador de la función asociada.
    seat_ids : Sequence[Any]
        Lista de identificadores de los asientos incluidos en la reserva.
    total_amount : Money
        Monto total de la reserva.
    status : str, optional
        Estado actual del booking. Por defecto es ``BOOKING_PENDING``.
    payment_status : str, optional
        Estado actual del pago. Por defecto es ``PAYMENT_PENDING``.
    created_at : datetime, optional
        Fecha y hora de creación de la reserva.
    updated_at : datetime, optional
        Fecha y hora de la última actualización.
    idempotency_key : str, optional
        Clave para evitar operaciones duplicadas.

    Attributes
    ----------
    booking_id : Any
        Identificador de la reserva.
    customer_id : Any
        Identificador del cliente.
    showtime_id : Any
        Identificador de la función.
    seat_ids : list[Any]
        Identificadores de los asientos reservados.
    total_amount : Money
        Total monetario de la reserva.
    status : str
        Estado del booking.
    payment_status : str
        Estado del pago.
    created_at : datetime
        Momento de creación.
    updated_at : datetime
        Momento de última actualización.
    idempotency_key : str | None
        Clave de idempotencia.
    """

    def __init__(
        self,
        booking_id,
        customer_id,
        showtime_id,
        seat_ids: Sequence,
        total_amount,
        status: str = BOOKING_PENDING,
        payment_status: str = PAYMENT_PENDING,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        idempotency_key: Optional[str] = None,
    ):
        self.booking_id = booking_id
        self.customer_id = customer_id
        self.showtime_id = showtime_id
        self.seat_ids = list(seat_ids)
        self.total_amount = total_amount
        self.status = status
        self.payment_status = payment_status
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or self.created_at
        self.idempotency_key = idempotency_key

    def calculate_total(self):
        """Retorna el total monetario de la reserva.

        Notes
        -----
        El total ya debe venir calculado por la capa de aplicación o por el
        servicio de dominio correspondiente. Este método existe para mantener
        la intención del modelo clara y facilitar futuras extensiones.

        Returns
        -------
        Money
            Total monetario de la reserva.
        """
        return self.total_amount

    def confirm(self):
        """Confirma la reserva.

        Raises
        ------
        BookingAlreadyConfirmedError
            Si la reserva ya fue confirmada.
        BookingAlreadyCancelledError
            Si la reserva ya fue cancelada.
        """
        if self.status == BOOKING_CONFIRMED:
            raise BookingAlreadyConfirmedError(
                "La reserva ya fue confirmada."
            )

        if self.status == BOOKING_CANCELLED:
            raise BookingAlreadyCancelledError(
                "No se puede confirmar una reserva cancelada."
            )

        self.validate_transition(BOOKING_CONFIRMED)
        self.status = BOOKING_CONFIRMED
        self.payment_status = PAYMENT_PAID
        self.updated_at = datetime.utcnow()

    def cancel(self):
        """Cancela la reserva.

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
        self.payment_status = PAYMENT_FAILED
        self.updated_at = datetime.utcnow()

    def mark_payment_pending(self):
        """Marca el pago como pendiente.

        Notes
        -----
        Esta operación es útil cuando la reserva ya existe pero el pago todavía
        no se ha resuelto.
        """
        self.payment_status = PAYMENT_PENDING
        self.updated_at = datetime.utcnow()

    def mark_paid(self):
        """Marca el pago como completado."""
        self.payment_status = PAYMENT_PAID
        self.updated_at = datetime.utcnow()

    def mark_failed(self):
        """Marca el pago como fallido."""
        self.payment_status = PAYMENT_FAILED
        self.updated_at = datetime.utcnow()

    def is_cancellable(self):
        """Indica si la reserva todavía puede cancelarse.

        Returns
        -------
        bool
            ``True`` si el booking está en un estado cancelable.
        """
        return self.status == BOOKING_PENDING

    def validate_transition(self, new_status: str):
        """Valida si el cambio de estado solicitado es permitido.

        Parameters
        ----------
        new_status : str
            Nuevo estado solicitado para el booking.

        Returns
        -------
        bool
            ``True`` si la transición es válida.

        Raises
        ------
        InvalidBookingStateTransitionError
            Si la transición no está permitida.
        """
        valid_transitions = {
            BOOKING_PENDING: [BOOKING_CONFIRMED, BOOKING_CANCELLED],
            BOOKING_CONFIRMED: [],
            BOOKING_CANCELLED: [],
        }

        allowed = valid_transitions.get(self.status, [])

        if new_status not in allowed:
            raise InvalidBookingStateTransitionError(
                f"Transición inválida: {self.status} -> {new_status}"
            )

        return True

    def __repr__(self):
        """Retorna una representación legible de la reserva.

        Returns
        -------
        str
            Representación textual del objeto.
        """
        return (
            "Booking("
            f"booking_id={self.booking_id!r}, "
            f"customer_id={self.customer_id!r}, "
            f"showtime_id={self.showtime_id!r}, "
            f"seat_ids={self.seat_ids!r}, "
            f"total_amount={self.total_amount!r}, "
            f"status={self.status!r}, "
            f"payment_status={self.payment_status!r}"
            ")"
        )

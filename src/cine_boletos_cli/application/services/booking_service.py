"""booking_service.py

Servicio de aplicación para coordinar el flujo de reservas y compras.

Este servicio actúa como orquestador entre entidades de dominio y
componentes externos del caso de uso. No contiene reglas de negocio de bajo
nivel: solo coordina el proceso completo.

Responsibilities
----------------
- validar que una reserva pueda realizarse,
- bloquear y liberar asientos a través del servicio correspondiente,
- calcular el total de la compra,
- crear y recuperar bookings,
- confirmar o cancelar reservas,
- coordinar acciones compensatorias cuando ocurre un fallo.

Notes
-----
Este servicio NO debe:
- imprimir en consola,
- ejecutar SQL directo,
- reemplazar las reglas internas de ``Seat`` o ``Booking``,
- depender de detalles concretos de infraestructura.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional, Sequence
from uuid import uuid4

from cine_boletos_cli.domain.entities.booking import Booking
from cine_boletos_cli.domain.value_objects.money import Money
from cine_boletos_cli.domain.value_objects.seat_id import SeatId
from cine_boletos_cli.shared.constants import (
    BOOKING_PENDING,
    PAYMENT_PENDING,
)


class BookingService:
    """Servicio encargado de coordinar reservas y compras.

    Parameters
    ----------
    booking_repository : object
        Repositorio encargado de persistir bookings.
    showtime_repository : object
        Repositorio encargado de recuperar funciones.
    seat_service : object
        Servicio encargado de bloquear, liberar y confirmar asientos.
    payment_service : object
        Servicio encargado de procesar pagos.
    idempotency_service : object
        Servicio encargado de evitar operaciones duplicadas.
    unit_of_work : object
        Coordinador transaccional del sistema.
    """

    def __init__(
        self,
        booking_repository,
        showtime_repository,
        seat_service,
        payment_service,
        idempotency_service,
        unit_of_work,
    ):
        self.booking_repository = booking_repository
        self.showtime_repository = showtime_repository
        self.seat_service = seat_service
        self.payment_service = payment_service
        self.idempotency_service = idempotency_service
        self.unit_of_work = unit_of_work

    def create_booking(
        self,
        customer_id: str,
        showtime_id: str,
        seat_ids: Sequence[SeatId],
        idempotency_key: Optional[str] = None,
    ):
        """Crea una reserva temporal.

        Parameters
        ----------
        customer_id : str
            Identificador del cliente.
        showtime_id : str
            Identificador de la función.
        seat_ids : Sequence[SeatId]
            Asientos solicitados.
        idempotency_key : str, optional
            Clave única para evitar duplicados.

        Returns
        -------
        Booking
            Reserva creada.
        """
        self.validate_booking(showtime_id, seat_ids)

        if idempotency_key is not None:
            existing_booking = self.idempotency_service.get(
                idempotency_key
            )
            if existing_booking is not None:
                return existing_booking

        self.seat_service.lock_seats(
            showtime_id=showtime_id,
            seat_ids=seat_ids,
        )

        total = self.calculate_total(
            showtime_id=showtime_id,
            seat_ids=seat_ids,
        )

        booking = Booking(
            booking_id=str(uuid4()),
            customer_id=customer_id,
            showtime_id=showtime_id,
            seat_ids=seat_ids,
            total_amount=total,
            status=BOOKING_PENDING,
            payment_status=PAYMENT_PENDING,
            created_at=datetime.utcnow(),
            idempotency_key=idempotency_key,
        )

        self.booking_repository.save(booking)

        if idempotency_key is not None:
            self.idempotency_service.store(idempotency_key, booking)

        self.unit_of_work.commit()
        return booking

    def confirm_booking(
        self,
        booking_id: str,
        payment_reference: Optional[str] = None,
    ):
        """Confirma una reserva después de un pago exitoso.

        Parameters
        ----------
        booking_id : str
            Identificador de la reserva.
        payment_reference : str, optional
            Referencia externa del pago.

        Returns
        -------
        Booking
            Reserva confirmada.
        """
        booking = self.get_booking(booking_id)

        if booking is None:
            raise ValueError("El booking no existe.")

        if payment_reference is not None:
            self.payment_service.register_payment_reference(
                booking_id=booking_id,
                payment_reference=payment_reference,
            )

        self.payment_service.mark_as_paid(booking_id=booking_id)

        self.seat_service.confirm_seats(
            showtime_id=booking.showtime_id,
            seat_ids=booking.seat_ids,
        )

        booking.confirm()
        self.booking_repository.save(booking)
        self.unit_of_work.commit()
        return booking

    def cancel_booking(
        self,
        booking_id: str,
        reason: Optional[str] = None,
    ):
        """Cancela una reserva existente.

        Parameters
        ----------
        booking_id : str
            Identificador del booking.
        reason : str, optional
            Motivo de cancelación.

        Returns
        -------
        Booking
            Reserva cancelada.
        """
        booking = self.get_booking(booking_id)

        if booking is None:
            raise ValueError("El booking no existe.")

        self.seat_service.release_seats(
            showtime_id=booking.showtime_id,
            seat_ids=booking.seat_ids,
        )

        if reason is not None:
            self.payment_service.register_cancellation_reason(
                booking_id=booking_id,
                reason=reason,
            )

        booking.cancel()
        self.booking_repository.save(booking)
        self.unit_of_work.commit()
        return booking

    def get_booking(self, booking_id: str):
        """Recupera un booking por su identificador.

        Parameters
        ----------
        booking_id : str
            Identificador del booking.

        Returns
        -------
        Booking | None
            Booking encontrado o None.
        """
        return self.booking_repository.get_by_id(booking_id)

    def release_failed_booking(self, booking_id: str):
        """Ejecuta acciones compensatorias cuando una compra falla.

        Parameters
        ----------
        booking_id : str
            Identificador del booking fallido.

        Returns
        -------
        None
        """
        booking = self.get_booking(booking_id)

        if booking is None:
            return

        self.seat_service.release_seats(
            showtime_id=booking.showtime_id,
            seat_ids=booking.seat_ids,
        )

        booking.mark_failed()
        self.booking_repository.save(booking)
        self.unit_of_work.commit()

    def calculate_total(
        self,
        showtime_id: str,
        seat_ids: Sequence[SeatId],
    ) -> Money:
        """Calcula el costo total de una compra.

        Parameters
        ----------
        showtime_id : str
            Identificador de la función.
        seat_ids : Sequence[SeatId]
            Asientos seleccionados.

        Returns
        -------
        Money
            Total calculado.
        """
        showtime = self.showtime_repository.get_by_id(showtime_id)

        if showtime is None:
            raise ValueError("La función no existe.")

        seat_price = showtime.ticket_price
        return seat_price * len(seat_ids)

    def validate_booking(
        self,
        showtime_id: str,
        seat_ids: Sequence[SeatId],
    ) -> None:
        """Valida que una reserva pueda realizarse.

        Parameters
        ----------
        showtime_id : str
            Identificador de la función.
        seat_ids : Sequence[SeatId]
            Asientos solicitados.

        Returns
        -------
        None
        """
        showtime = self.showtime_repository.get_by_id(showtime_id)

        if showtime is None:
            raise ValueError("La función no existe.")

        self.seat_service.validate_availability(
            showtime_id=showtime_id,
            seat_ids=seat_ids,
        )

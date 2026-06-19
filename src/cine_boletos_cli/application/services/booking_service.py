from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from cine_boletos_cli.domain.entities.booking import Booking
from cine_boletos_cli.domain.value_objects.money import Money
from cine_boletos_cli.shared.constants import (
    BOOKING_PENDING,
    PAYMENT_PAID,
)


class BookingService:
    """
    Servicio mínimo para confirmar compra de varios asientos bloqueados.
    """

    def __init__(
        self,
        booking_repository,
        showtime_repository,
        showtime_seat_repository,
    ):
        self.booking_repository = booking_repository
        self.showtime_repository = showtime_repository
        self.showtime_seat_repository = showtime_seat_repository

    def create_booking_from_locked_seats(
        self,
        customer_id: str,
        showtime_id: str,
        seat_ids: list[str],
    ):
        showtime = self.showtime_repository.get_by_id(
            showtime_id
        )

        if showtime is None:
            raise ValueError(
                f"Showtime '{showtime_id}' not found."
            )

        if not seat_ids:
            raise ValueError(
                "At least one seat is required."
            )

        showtime_seats = []

        for seat_id in seat_ids:
            showtime_seat = (
                self.showtime_seat_repository
                .get_by_showtime_and_seat_id(
                    showtime_id=showtime_id,
                    seat_id=seat_id,
                )
            )

            if showtime_seat is None:
                raise ValueError(
                    f"Seat '{seat_id}' not found for showtime."
                )

            if not showtime_seat.is_locked():
                raise ValueError(
                    f"Seat '{seat_id}' must be locked before booking."
                )

            showtime_seats.append(
                showtime_seat
            )

        total_amount = Money(
            str(5 * len(showtime_seats))
        )

        booking = Booking(
            booking_id=str(uuid4()),
            customer_id=customer_id,
            showtime_id=showtime_id,
            seat_ids=seat_ids,
            total_amount=total_amount,
            status=BOOKING_PENDING,
            payment_status=PAYMENT_PAID,
            created_at=datetime.utcnow(),
        )

        for showtime_seat in showtime_seats:
            showtime_seat.book()

            self.showtime_seat_repository.save(
                showtime_seat
            )

        booking.confirm()

        return self.booking_repository.save(
            booking
        )

    def get_booking(
        self,
        booking_id: str,
    ):
        return self.booking_repository.get_by_id(
            booking_id
        )

    def list_bookings(self):
        return self.booking_repository.list_all()

    def count(self):
        return self.booking_repository.count()

    def cancel_booking(
        self,
        booking_id: str,
    ):
        """
        Cancela una reserva y libera sus asientos.
        """

        booking = self.booking_repository.get_by_id(
            booking_id
        )

        if booking is None:
            raise ValueError(
                f"Booking '{booking_id}' not found."
            )

        if not booking.is_cancellable():
            raise ValueError(
                f"Booking '{booking_id}' cannot be cancelled."
            )

        for seat_id in booking.seat_ids:

            showtime_seat = (
                self.showtime_seat_repository
                .get_by_showtime_and_seat_id(
                    showtime_id=booking.showtime_id,
                    seat_id=seat_id,
                )
            )

            if showtime_seat is None:
                continue

            if showtime_seat.is_booked():
                showtime_seat.cancel_booking()

                self.showtime_seat_repository.save(
                    showtime_seat
                )

        booking.cancel()

        return self.booking_repository.save(
            booking
        )
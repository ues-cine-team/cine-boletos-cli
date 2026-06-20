from cine_boletos_cli.domain.entities.showtime_seat import (
    ShowtimeSeat,
)


class ShowtimeSeatService:
    """
    Servicio encargado de coordinar operaciones
    sobre asientos por función.
    """

    def __init__(
        self,
        showtime_seat_repository,
    ):
        self.showtime_seat_repository = (
            showtime_seat_repository
        )

    def create_showtime_seat(
        self,
        showtime_seat_id,
        showtime_id,
        seat_id,
    ):
        """
        Crea un asiento para una función.
        """

        seat = ShowtimeSeat(
            showtime_seat_id=showtime_seat_id,
            showtime_id=showtime_id,
            seat_id=seat_id,
        )

        return self.showtime_seat_repository.save(
            seat
        )

    def list_by_showtime(
        self,
        showtime_id,
    ):
        """
        Lista asientos de una función.
        """

        return (
            self.showtime_seat_repository
            .list_by_showtime(showtime_id)
        )

    def list_available(
        self,
        showtime_id,
    ):
        """
        Lista asientos disponibles.
        """

        return (
            self.showtime_seat_repository
            .list_available(showtime_id)
        )

    def lock_seat(
        self,
        showtime_seat_id,
    ):
        """
        Bloquea un asiento.
        """

        seat = (
            self.showtime_seat_repository
            .get_by_id(showtime_seat_id)
        )

        if seat is None:
            raise ValueError(
                "ShowtimeSeat not found."
            )

        seat.lock()

        return seat

    def release_seat(
        self,
        showtime_seat_id,
    ):
        """
        Libera un asiento.
        """

        seat = (
            self.showtime_seat_repository
            .get_by_id(showtime_seat_id)
        )

        if seat is None:
            raise ValueError(
                "ShowtimeSeat not found."
            )

        seat.release()

        return seat

    def book_seat(
        self,
        showtime_seat_id,
    ):
        """
        Marca asiento como vendido.
        """

        seat = (
            self.showtime_seat_repository
            .get_by_id(showtime_seat_id)
        )

        if seat is None:
            raise ValueError(
                "ShowtimeSeat not found."
            )

        seat.book()

        return seat

    def get_by_showtime_and_seat_id(
        self,
        showtime_id,
        seat_id,
    ):
        return (
            self.showtime_seat_repository
            .get_by_showtime_and_seat_id(
                showtime_id=showtime_id,
                seat_id=seat_id,
            )
        )

    def save(
        self,
        showtime_seat,
    ):
        return self.showtime_seat_repository.save(
            showtime_seat
        )
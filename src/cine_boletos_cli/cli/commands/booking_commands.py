from __future__ import annotations

from typing import List


class BookingCommands:
    """
    Flujo interactivo de compra de boletos.
    """

    def __init__(
        self,
        movie_service,
        showtime_service,
        showtime_seat_service,
        booking_service,
        logger=None,
    ):
        self.movie_service = movie_service
        self.showtime_service = showtime_service
        self.showtime_seat_service = showtime_seat_service
        self.booking_service = booking_service
        self.logger = logger

        self.is_running = False

    def run(self) -> None:
        self.is_running = True

        while self.is_running:
            self._render_movies_menu()

            option = self._read_user_option(
                "\nSeleccione una película: "
            )

            self._handle_movie_selection(option)

    def stop(self) -> None:
        self.is_running = False

    def _render_movies_menu(self) -> None:
        print("\n" + "=" * 50)
        print("              COMPRA DE BOLETOS")
        print("=" * 50)

        movies = self._load_movies()

        if not movies:
            print("\nNo hay películas disponibles.")
            print("\n0. Regresar")
            return

        for index, movie in enumerate(movies, start=1):
            print(f"{index}. {movie.title}")

        print("\n0. Regresar")

    def _load_movies(self) -> List:
        return self.movie_service.list_movies()

    def _handle_movie_selection(
        self,
        option: str,
    ) -> None:
        if option == "0":
            self.stop()
            return

        if not option.isdigit():
            self._handle_invalid_option()
            return

        movies = self._load_movies()
        movie_index = int(option) - 1

        if movie_index < 0 or movie_index >= len(movies):
            self._handle_invalid_option()
            return

        selected_movie = movies[movie_index]

        self._open_movie_showtimes(selected_movie)

    def _open_movie_showtimes(
        self,
        movie,
    ) -> None:
        showtimes = (
            self.showtime_service
            .list_showtimes_by_movie(
                movie.movie_id
            )
        )

        if not showtimes:
            print("\nNo hay funciones disponibles para esta película.")
            self._pause()
            return

        print("\n" + "=" * 50)
        print(f"FUNCIONES DE {movie.title.upper()}")
        print("=" * 50)

        for index, showtime in enumerate(showtimes, start=1):
            print(f"{index}.")
            print(f"ID de función: {showtime.showtime_id}")
            print(f"Sala: {showtime.room_id}")
            print(f"Inicio: {showtime.starts_at}")
            print("-" * 50)

        print("\n0. Regresar")

        option = self._read_user_option(
            "\nSeleccione una función: "
        )

        if option == "0":
            return

        if not option.isdigit():
            self._handle_invalid_option()
            self._pause()
            return

        showtime_index = int(option) - 1

        if (
            showtime_index < 0
            or showtime_index >= len(showtimes)
        ):
            self._handle_invalid_option()
            self._pause()
            return

        selected_showtime = showtimes[showtime_index]

        self._open_seat_selection(
            movie=movie,
            showtime=selected_showtime,
        )

    def _open_seat_selection(
        self,
        movie,
        showtime,
    ) -> None:
        while True:
            seats = (
                self.showtime_seat_service
                .list_by_showtime(
                    showtime.showtime_id
                )
            )

            if not seats:
                print("\nNo hay asientos para esta función.")
                self._pause()
                return

            self._render_seat_map(
                movie=movie,
                showtime=showtime,
                seats=seats,
            )

            selected_input = self._read_user_option(
                "\nSeleccione los asientos separados por coma "
                "(ejemplo: A1,B2,C1): "
            ).upper()

            if selected_input == "0":
                return

            selected_labels = self._parse_selected_labels(
                selected_input
            )

            if not selected_labels:
                print("\nNo seleccionó asientos.")
                self._pause()
                continue

            self._process_seat_selection(
                movie=movie,
                showtime=showtime,
                selected_labels=selected_labels,
            )

            self._pause()

    def _render_seat_map(
        self,
        movie,
        showtime,
        seats,
    ) -> None:
        print("\n" + "=" * 50)
        print("              MAPA DE ASIENTOS")
        print("=" * 50)
        print(f"Película: {movie.title}")
        print(f"Sala: {showtime.room_id}")
        print(f"Inicio: {showtime.starts_at}")
        print("-" * 50)

        seats_by_row = {}

        for seat in seats:
            label = seat.seat_id.split("-")[-1]
            row = label[0]

            seats_by_row.setdefault(
                row,
                [],
            ).append(seat)

        for row in sorted(seats_by_row.keys()):
            row_seats = sorted(
                seats_by_row[row],
                key=lambda seat: int(
                    seat.seat_id.split("-")[-1][1:]
                ),
            )

            labels = []

            for seat in row_seats:
                label = seat.seat_id.split("-")[-1]

                if seat.is_available():
                    labels.append(label)
                elif seat.is_locked():
                    labels.append(f"{label}[L]")
                elif seat.is_booked():
                    labels.append(f"{label}[B]")

            print("  ".join(labels))

        print("\nLeyenda:")
        print("[L] Bloqueado")
        print("[B] Comprado")
        print("Sin marca = Disponible")
        print("\n0. Regresar")

    def _parse_selected_labels(
        self,
        selected_input: str,
    ) -> List[str]:
        return [
            value.strip()
            for value in selected_input.split(",")
            if value.strip()
        ]

    def _process_seat_selection(
        self,
        movie,
        showtime,
        selected_labels: List[str],
    ) -> None:
        seat_ids = [
            f"{showtime.room_id}-{label}"
            for label in selected_labels
        ]

        locked_seats = []

        try:
            locked_seats = self._lock_selected_seats(
                showtime_id=showtime.showtime_id,
                seat_ids=seat_ids,
            )

            self._render_locked_seats(
                selected_labels
            )

            confirmed = self._confirm_purchase(
                movie=movie,
                showtime=showtime,
                selected_labels=selected_labels,
                seat_ids=seat_ids,
            )

            if not confirmed:
                self._release_locked_seats(
                    locked_seats
                )

                print("\nCompra cancelada. Asientos liberados.")
                return

            booking = (
                self.booking_service
                .create_booking_from_locked_seats(
                    customer_id="guest",
                    showtime_id=showtime.showtime_id,
                    seat_ids=seat_ids,
                )
            )

            self._render_purchase_success(
                booking=booking,
                movie=movie,
                showtime=showtime,
                selected_labels=selected_labels,
            )

        except Exception as exc:
            print("\nNo se pudo completar la compra.")
            print(str(exc))

            self._release_locked_seats_safely(
                locked_seats
            )

            if self.logger:
                self.logger.error(
                    "Purchase flow failed: %s",
                    exc,
                )

    def _lock_selected_seats(
        self,
        showtime_id: str,
        seat_ids: List[str],
    ) -> List:
        locked_seats = []

        for seat_id in seat_ids:
            showtime_seat = (
                self.showtime_seat_service
                .get_by_showtime_and_seat_id(
                    showtime_id=showtime_id,
                    seat_id=seat_id,
                )
            )

            if showtime_seat is None:
                raise ValueError(
                    f"Asiento '{seat_id}' no encontrado."
                )

            if showtime_seat.is_booked():
                raise ValueError(
                    f"Asiento '{seat_id}' ya fue comprado."
                )

            if showtime_seat.is_locked():
                raise ValueError(
                    f"Asiento '{seat_id}' ya está bloqueado."
                )

            showtime_seat.lock()

            self.showtime_seat_service.save(
                showtime_seat
            )

            locked_seats.append(
                showtime_seat
            )

        return locked_seats

    def _render_locked_seats(
        self,
        selected_labels: List[str],
    ) -> None:
        print("\nAsientos bloqueados temporalmente:")

        for label in selected_labels:
            print(f"- {label}")

    def _confirm_purchase(
        self,
        movie,
        showtime,
        selected_labels: List[str],
        seat_ids: List[str],
    ) -> bool:
        total = 5 * len(seat_ids)

        print("\n" + "=" * 50)
        print("RESUMEN DE COMPRA")
        print("=" * 50)
        print(f"Película: {movie.title}")
        print(f"Sala: {showtime.room_id}")
        print(f"Inicio: {showtime.starts_at}")
        print(f"Asientos: {', '.join(selected_labels)}")
        print(f"Total: {total}.00 USD")

        print("\n1. Confirmar compra")
        print("0. Cancelar")

        option = self._read_user_option(
            "\nSeleccione una opción: "
        )

        return option == "1"

    def _render_purchase_success(
        self,
        booking,
        movie,
        showtime,
        selected_labels: List[str],
    ) -> None:
        print("\nCompra registrada correctamente.")
        print("=" * 50)
        print(f"ID de reserva: {booking.booking_id}")
        print(f"Película: {movie.title}")
        print(f"Sala: {showtime.room_id}")
        print(f"Inicio: {showtime.starts_at}")
        print("Asientos:")

        for label in selected_labels:
            print(f"- {label}")

        print(
            f"Total: {booking.total_amount.amount} "
            f"{booking.total_amount.currency}"
        )

    def _release_locked_seats(
        self,
        locked_seats: List,
    ) -> None:
        for showtime_seat in locked_seats:
            showtime_seat.release()

            self.showtime_seat_service.save(
                showtime_seat
            )

    def _release_locked_seats_safely(
        self,
        locked_seats: List,
    ) -> None:
        for showtime_seat in locked_seats:
            if showtime_seat.is_locked():
                showtime_seat.release()

                self.showtime_seat_service.save(
                    showtime_seat
                )

    def _read_user_option(
        self,
        message: str,
    ) -> str:
        return input(message).strip()

    def _handle_invalid_option(self) -> None:
        print("\nOpción inválida.")

    def _pause(self) -> None:
        input("\nPresione ENTER para continuar...")
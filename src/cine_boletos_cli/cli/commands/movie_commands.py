from __future__ import annotations

from typing import List


class MovieCommands:
    """
    Módulo interactivo de películas.
    """

    def __init__(
        self,
        movie_service,
        showtime_service=None,
        showtime_seat_repository=None,
        booking_service=None,
        logger=None,
    ):
        self.movie_service = movie_service
        self.showtime_service = showtime_service
        self.showtime_seat_repository = showtime_seat_repository
        self.booking_service = booking_service
        self.logger = logger

        self.is_running = False

    def run(self) -> None:
        self.is_running = True

        while self.is_running:
            self._render_movies_menu()

            option = self._read_user_option()

            self._handle_movies_option(option)

    def stop(self) -> None:
        self.is_running = False

    def _render_movies_menu(self) -> None:
        print("\n" + "=" * 50)
        print("                  PELÍCULAS")
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

    def _read_user_option(self) -> str:
        return input("\nSeleccione una película: ").strip()

    def _handle_movies_option(
        self,
        option: str,
    ) -> None:
        if option == "0":
            self.stop()
            return

        if not option.isdigit():
            self._handle_invalid_option()
            return

        movie_index = int(option) - 1

        movies = self._load_movies()

        if movie_index < 0 or movie_index >= len(movies):
            self._handle_invalid_option()
            return

        selected_movie = movies[movie_index]

        self._open_movie_details(selected_movie)

    def _open_movie_details(
        self,
        movie,
    ) -> None:
        print("\n" + "=" * 50)
        print(f"PELÍCULA: {movie.title}")
        print("=" * 50)

        print(f"Duración: {movie.duration_minutes} minutos")
        print(f"Clasificación: {movie.classification}")

        if getattr(movie, "genre", None):
            print(f"Género: {movie.genre}")

        if getattr(movie, "description", None):
            print(f"\nDescripción:\n{movie.description}")

        self._render_movie_actions(movie)

    def _render_movie_actions(
        self,
        movie,
    ) -> None:
        print("\n1. Ver funciones")
        print("0. Regresar")

        option = input("\nSeleccione una opción: ").strip()

        if option == "1":
            self._open_movie_showtimes(movie)

    def _open_movie_showtimes(
        self,
        movie,
    ) -> None:
        if self.showtime_service is None:
            print("\nServicio de funciones no disponible.")
            return

        showtimes = (
            self.showtime_service
            .list_showtimes_by_movie(
                movie.movie_id
            )
        )

        if not showtimes:
            print("\nNo hay funciones disponibles.")
            self._pause()
            return

        print(
            f"\nFUNCIONES DE "
            f"{movie.title.upper()}"
        )
        print("-" * 50)

        for index, showtime in enumerate(showtimes, start=1):
            print(f"{index}.")
            print(f"ID de función: {showtime.showtime_id}")
            print(f"Sala: {showtime.room_id}")
            print(f"Inicio: {showtime.starts_at}")
            print("-" * 50)

        option = input(
            "\nSeleccione una función para ver asientos "
            "(0. Regresar): "
        ).strip()

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

        self._render_showtime_seats(
            selected_showtime
        )

    def _render_showtime_seats(
        self,
        showtime,
    ) -> None:
        if self.showtime_seat_repository is None:
            print("\nMapa de asientos no disponible.")
            self._pause()
            return

        while True:
            seats = (
                self.showtime_seat_repository
                .list_by_showtime(
                    showtime.showtime_id
                )
            )

            if not seats:
                print("\nNo hay asientos para esta función.")
                self._pause()
                return

            print("\n" + "=" * 50)
            print("            MAPA DE ASIENTOS")
            print("=" * 50)

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

            selected_input = input(
                "\nSeleccione los asientos separados por coma "
                "(ejemplo: A1,B2,C1): "
            ).strip().upper()

            if selected_input == "0":
                return

            selected_labels = [
                value.strip()
                for value in selected_input.split(",")
                if value.strip()
            ]

            if not selected_labels:
                print("\nNo seleccionó asientos.")
                self._pause()
                continue

            seat_ids = [
                f"{showtime.room_id}-{label}"
                for label in selected_labels
            ]

            locked_seats = []

            try:
                for seat_id in seat_ids:
                    showtime_seat = (
                        self.showtime_seat_repository
                        .get_by_showtime_and_seat_id(
                            showtime_id=showtime.showtime_id,
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

                    self.showtime_seat_repository.save(
                        showtime_seat
                    )

                    locked_seats.append(
                        showtime_seat
                    )

                print("\nAsientos bloqueados temporalmente:")
                for label in selected_labels:
                    print(f"- {label}")

                print("\n1. Confirmar compra")
                print("0. Cancelar")

                option = input(
                    "\nSeleccione una opción: "
                ).strip()

                if option == "0":
                    for showtime_seat in locked_seats:
                        showtime_seat.release()

                        self.showtime_seat_repository.save(
                            showtime_seat
                        )

                    print("\nCompra cancelada. Asientos liberados.")
                    self._pause()
                    continue

                if option != "1":
                    self._handle_invalid_option()

                    for showtime_seat in locked_seats:
                        showtime_seat.release()

                        self.showtime_seat_repository.save(
                            showtime_seat
                        )

                    self._pause()
                    continue

                if self.booking_service is None:
                    raise ValueError(
                        "Servicio de reservas no disponible."
                    )

                booking = (
                    self.booking_service
                    .create_booking_from_locked_seats(
                        customer_id="guest",
                        showtime_id=showtime.showtime_id,
                        seat_ids=seat_ids,
                    )
                )

                print("\nCompra registrada correctamente.")
                print(f"ID de reserva: {booking.booking_id}")
                print("Asientos:")

                for label in selected_labels:
                    print(f"- {label}")

                print(
                    f"Total: {booking.total_amount.amount} "
                    f"{booking.total_amount.currency}"
                )

            except Exception as exc:
                print("\nNo se pudo completar la compra.")
                print(str(exc))

                for showtime_seat in locked_seats:
                    if showtime_seat.is_locked():
                        showtime_seat.release()

                        self.showtime_seat_repository.save(
                            showtime_seat
                        )

            self._pause()

    def _handle_invalid_option(self) -> None:
        print("\nOpción inválida.")

    def _pause(self) -> None:
        input("\nPresione ENTER para continuar...")
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
        logger=None,
    ):
        self.movie_service = movie_service
        self.showtime_service = showtime_service
        self.showtime_seat_repository = showtime_seat_repository
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
        print("                    MOVIES")
        print("=" * 50)

        movies = self._load_movies()

        if not movies:
            print("\nNo movies available.")
            print("\n0. Back")
            return

        for index, movie in enumerate(movies, start=1):
            print(f"{index}. {movie.title}")

        print("\n0. Back")

    def _load_movies(self) -> List:
        return self.movie_service.list_movies()

    def _read_user_option(self) -> str:
        return input("\nSelect a movie: ").strip()

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
        print(f"TITLE: {movie.title}")
        print("=" * 50)

        print(f"Duration: {movie.duration_minutes} minutes")
        print(f"Classification: {movie.classification}")

        if getattr(movie, "genre", None):
            print(f"Genre: {movie.genre}")

        if getattr(movie, "description", None):
            print(f"\nDescription:\n{movie.description}")

        self._render_movie_actions(movie)

    def _render_movie_actions(
        self,
        movie,
    ) -> None:
        print("\n1. View Showtimes")
        print("0. Back")

        option = input("\nSelect an option: ").strip()

        if option == "1":
            self._open_movie_showtimes(movie)

    def _open_movie_showtimes(
        self,
        movie,
    ) -> None:
        if self.showtime_service is None:
            print("\nShowtime service unavailable.")
            return

        showtimes = (
            self.showtime_service
            .list_showtimes_by_movie(
                movie.movie_id
            )
        )

        if not showtimes:
            print("\nNo showtimes available.")
            self._pause()
            return

        print(
            f"\nSHOWTIMES FOR "
            f"{movie.title.upper()}"
        )
        print("-" * 50)

        for index, showtime in enumerate(showtimes, start=1):
            print(f"{index}.")
            print(f"Showtime ID: {showtime.showtime_id}")
            print(f"Room: {showtime.room_id}")
            print(f"Starts: {showtime.starts_at}")
            print("-" * 50)

        option = input(
            "\nSelect a showtime to view seats "
            "(0. Back): "
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
            print("\nSeat map unavailable.")
            self._pause()
            return

        seats = (
            self.showtime_seat_repository
            .list_by_showtime(
                showtime.showtime_id
            )
        )

        if not seats:
            print("\nNo seats available for this showtime.")
            self._pause()
            return

        print("\n" + "=" * 50)
        print("                SEAT MAP")
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

        print("\nLegend:")
        print("[L] Locked")
        print("[B] Booked")
        print("No mark = Available")

        self._pause()

    def _handle_invalid_option(self) -> None:
        print("\nInvalid option. Please try again.")

    def _pause(self) -> None:
        input("\nPress ENTER to continue...")
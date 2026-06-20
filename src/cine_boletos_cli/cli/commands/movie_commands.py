from __future__ import annotations

from typing import List


class MovieCommands:
    """
    Módulo interactivo de películas.

    Responsabilidad:
    - listar películas,
    - mostrar detalle,
    - mostrar funciones asociadas.

    No compra boletos.
    La compra vive en BookingCommands.
    """

    def __init__(
        self,
        movie_service,
        showtime_service=None,
        logger=None,
    ):
        self.movie_service = movie_service
        self.showtime_service = showtime_service
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
            self._pause()
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

        print("\nPara comprar boletos use:")
        print("MAIN MENU -> Purchase Tickets")

        self._pause()

    def _handle_invalid_option(self) -> None:
        print("\nOpción inválida.")

    def _pause(self) -> None:
        input("\nPresione ENTER para continuar...")
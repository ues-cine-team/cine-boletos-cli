"""
MovieCommands.

Este archivo define el módulo interactivo de navegación relacionado con
películas dentro de la aplicación CLI.

IMPORTANTE
----------
Este archivo NO representa comandos individuales tipo terminal UNIX.

En cambio, representa:
- pantallas,
- menús,
- navegación interactiva,
- flujo guiado de consola.

¿Por qué existe?
----------------
Porque el usuario necesita interactuar con el catálogo del cine de manera
simple y guiada.

Este módulo será responsable de:
- mostrar películas,
- navegar catálogo,
- visualizar detalles,
- seleccionar películas,
- conectar con funciones disponibles.

Responsabilidad principal
-------------------------
Coordinar interacción CLI relacionada con películas.

Relación con otros módulos
--------------------------
Este módulo trabajará junto con:

- `MovieService`
    Consulta de catálogo.

- `ShowtimeService`
    Consulta de funciones.

- `MovieDTO`
    Transporte de películas.

- `ShowtimeDTO`
    Transporte de funciones.

- `CommandRouter`
    Navegación principal.

Qué debe resolver este módulo
-----------------------------
- navegación del catálogo,
- renderizado de películas,
- selección de opciones,
- visualización de detalles,
- transición hacia funciones/showtimes.

Qué NO debe hacer
-----------------
- No debe contener lógica del dominio.
- No debe acceder directamente a repositories.
- No debe manejar pagos.
- No debe modificar entidades.
- No debe contener reglas de negocio.

La lógica vive en:
- services,
- use cases,
- entidades del dominio.

Este módulo solamente:
- muestra información,
- recoge input,
- delega operaciones.

Cómo debe sentirse
------------------
Como una aplicación real de consola.

Ejemplo conceptual:

==================================================
                    MOVIES
==================================================

1. Interstellar
2. Dune
3. Batman Begins
4. Back

Select a movie:

Importante
----------
Este archivo representa una pantalla interactiva del sistema.
"""

from __future__ import annotations

from typing import List, Optional


class MovieCommands:
    """
    Módulo interactivo de películas.

    Notes
    -----
    Esta clase coordina:
    - navegación del catálogo,
    - renderizado de películas,
    - selección de películas,
    - visualización de detalles.
    """

    def __init__(
        self,
        movie_service,
        showtime_service=None,
        logger=None,
    ):
        """
        Inicializa módulo de películas.

        Parameters
        ----------
        movie_service : object
            Servicio de películas.

        showtime_service : object, optional
            Servicio de funciones.

        logger : object, optional
            Sistema de logging.
        """
        self.movie_service = movie_service
        self.showtime_service = showtime_service
        self.logger = logger

        self.is_running = False

    def run(self) -> None:
        """
        Ejecuta navegación del catálogo.

        Flujo esperado
        --------------
        1. cargar películas,
        2. mostrar catálogo,
        3. seleccionar película,
        4. mostrar detalles,
        5. navegar a funciones,
        6. volver atrás.
        """
        self.is_running = True

        while self.is_running:
            self._render_movies_menu()

            option = self._read_user_option()

            self._handle_movies_option(option)

    def stop(self) -> None:
        """
        Finaliza navegación actual.
        """
        self.is_running = False

    def _render_movies_menu(self) -> None:
        """
        Renderiza menú principal de películas.

        Notes
        -----
        Más adelante este método podrá:
        - paginar resultados,
        - renderizar tablas,
        - mostrar posters ASCII,
        - mostrar filtros.
        """
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
        """
        Carga películas disponibles.

        Returns
        -------
        list
            Lista de MovieDTO.

        Notes
        -----
        Más adelante este método podrá:
        - filtrar cartelera,
        - consultar disponibilidad,
        - ordenar resultados.
        """
        return self.movie_service.list_movies()

    def _read_user_option(self) -> str:
        """
        Lee opción ingresada por usuario.

        Returns
        -------
        str
            Valor ingresado.
        """
        return input("\nSelect a movie: ").strip()

    def _handle_movies_option(
        self,
        option: str,
    ) -> None:
        """
        Procesa opción seleccionada.

        Parameters
        ----------
        option : str
            Valor ingresado.
        """
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
        """
        Muestra detalles de película seleccionada.

        Parameters
        ----------
        movie : MovieDTO
            Película seleccionada.

        Notes
        -----
        Más adelante este método podrá:
        - renderizar descripción,
        - mostrar clasificación,
        - mostrar duración,
        - mostrar showtimes,
        - permitir navegación avanzada.
        """
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
        """
        Renderiza acciones disponibles para película.

        Parameters
        ----------
        movie : MovieDTO
            Película objetivo.
        """
        print("\n1. View Showtimes")
        print("0. Back")

        option = input("\nSelect an option: ").strip()

        if option == "1":
            self._open_movie_showtimes(movie)

    def _open_movie_showtimes(
        self,
        movie,
    ) -> None:
        """
        Navega a funciones relacionadas con película.

        Parameters
        ----------
        movie : MovieDTO
            Película seleccionada.

        Notes
        -----
        Más adelante este método delegará navegación hacia:
        - `showtime_commands.py`
        - selección de horarios,
        - flujo de booking.
        """
        if self.showtime_service is None:
            print("\nShowtime service unavailable.")
            return

        print(f"\nLoading showtimes for: {movie.title}")

    def _handle_invalid_option(self) -> None:
        """
        Maneja opciones inválidas.
        """
        print("\nInvalid option. Please try again.")

    def _pause(self) -> None:
        """
        Pausa interacción.

        Notes
        -----
        Helper reutilizable para navegación CLI.
        """
        input("\nPress ENTER to continue...")


"""
Ejemplo conceptual futuro
-------------------------

    movie_commands = MovieCommands(
        movie_service=movie_service,
        showtime_service=showtime_service,
    )

    movie_commands.run()

Flujo esperado
--------------
MOVIES
    ├── list movies
    ├── select movie
    ├── view details
    ├── open showtimes
    └── back

Importante
----------
Este módulo NO contiene lógica de negocio.

Solamente coordina:
- navegación,
- renderizado,
- interacción de usuario,
- flujo visual CLI.
"""
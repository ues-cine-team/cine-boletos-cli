"""
AdminCommands.

Este archivo define el panel administrativo interactivo del sistema de
boletos de cine.

IMPORTANTE
----------
Este módulo representa:
- navegación administrativa,
- operaciones internas,
- panel operativo CLI,
- flujo de administración.

NO representa:
- lógica del dominio,
- persistencia,
- transacciones,
- reglas operacionales.

Toda lógica real vive en:
- services,
- use cases,
- entidades del dominio.

Este módulo solamente:
- renderiza menús,
- recibe input,
- coordina navegación,
- delega operaciones.

¿Por qué existe?
----------------
Porque el sistema necesita operaciones internas para administrar:
- películas,
- funciones,
- bookings,
- salas,
- estado operacional.

Este módulo representa el panel interno del cine.

Responsabilidad principal
-------------------------
Coordinar interacción administrativa CLI.

Relación con otros módulos
--------------------------
Este módulo trabajará junto con:

- `CreateMovieUseCase`
    Creación de películas.

- `CreateShowtimeUseCase`
    Creación de funciones.

- `MovieService`
    Consulta de películas.

- `ShowtimeService`
    Consulta de funciones.

- `BookingService`
    Consulta de reservas.

- `CommandRouter`
    Navegación principal.

Qué debe resolver este módulo
-----------------------------
- navegación administrativa,
- renderizado de paneles,
- formularios básicos,
- operaciones operacionales,
- visualización administrativa.

Qué NO debe hacer
-----------------
- No debe acceder directo a repositories.
- No debe modificar entidades manualmente.
- No debe manejar transacciones.
- No debe contener SQL.
- No debe contener reglas del negocio.

Cómo debe sentirse
------------------
Como un panel administrativo real.

Ejemplo conceptual:

==================================================
                ADMIN PANEL
==================================================

1. Create Movie
2. Create Showtime
3. View Bookings
4. View Rooms
5. Back

Select an option:

Importante
----------
Este archivo representa el panel interno operativo del sistema.
"""

from __future__ import annotations

from typing import Optional


class AdminCommands:
    """
    Panel administrativo interactivo.

    Notes
    -----
    Esta clase coordina:
    - operaciones administrativas,
    - navegación interna,
    - formularios básicos,
    - visualización operacional.
    """

    def __init__(
        self,
        create_movie_use_case,
        create_showtime_use_case,
        movie_service,
        showtime_service,
        booking_service,
        logger=None,
    ):
        """
        Inicializa panel administrativo.

        Parameters
        ----------
        create_movie_use_case : object
            Caso de uso de creación de películas.

        create_showtime_use_case : object
            Caso de uso de creación de funciones.

        movie_service : object
            Servicio de películas.

        showtime_service : object
            Servicio de funciones.

        booking_service : object
            Servicio de reservas.

        logger : object, optional
            Sistema de logging.
        """
        self.create_movie_use_case = create_movie_use_case
        self.create_showtime_use_case = create_showtime_use_case

        self.movie_service = movie_service
        self.showtime_service = showtime_service
        self.booking_service = booking_service

        self.logger = logger

        self.is_running = False

    def run(self) -> None:
        """
        Ejecuta panel administrativo.

        Flujo esperado
        --------------
        1. renderizar panel,
        2. seleccionar operación,
        3. ejecutar flujo,
        4. volver al panel.
        """
        self.is_running = True

        while self.is_running:
            self._render_admin_menu()

            option = self._read_user_option()

            self._handle_admin_option(option)

    def stop(self) -> None:
        """
        Finaliza navegación administrativa.
        """
        self.is_running = False

    def _render_admin_menu(self) -> None:
        """
        Renderiza panel administrativo principal.
        """
        print("\n" + "=" * 50)
        print("                ADMIN PANEL")
        print("=" * 50)

        print("1. Create Movie")
        print("2. Create Showtime")
        print("3. View Movies")
        print("4. View Showtimes")
        print("5. View Bookings")
        print("0. Back")

    def _read_user_option(self) -> str:
        """
        Lee input administrativo.

        Returns
        -------
        str
            Opción ingresada.
        """
        return input("\nSelect an option: ").strip()

    def _handle_admin_option(
        self,
        option: str,
    ) -> None:
        """
        Procesa opción administrativa.

        Parameters
        ----------
        option : str
            Opción seleccionada.
        """
        handlers = {
            "1": self._create_movie_flow,
            "2": self._create_showtime_flow,
            "3": self._view_movies,
            "4": self._view_showtimes,
            "5": self._view_bookings,
            "0": self.stop,
        }

        handler = handlers.get(option)

        if handler is None:
            self._handle_invalid_option()
            return

        handler()

    def _create_movie_flow(self) -> None:
        """
        Ejecuta flujo conceptual de creación de película.

        Notes
        -----
        Más adelante este método podrá:
        - validar formularios,
        - validar duración,
        - validar clasificación,
        - subir metadata,
        - registrar auditoría.
        """
        print("\nCREATE MOVIE")

        title = input("Title: ").strip()
        duration = input("Duration (minutes): ").strip()
        classification = input("Classification: ").strip()

        try:
            result = self.create_movie_use_case.execute(
                title=title,
                duration_minutes=duration,
                classification=classification,
            )

            print("\nMovie created successfully.")

        except Exception as exc:
            self._handle_admin_error(exc)

        self._pause()

    def _create_showtime_flow(self) -> None:
        """
        Ejecuta flujo conceptual de creación de función.

        Notes
        -----
        Más adelante este método podrá:
        - seleccionar sala,
        - validar horarios,
        - detectar conflictos,
        - configurar pricing,
        - configurar formatos especiales.
        """
        print("\nCREATE SHOWTIME")

        movie_id = input("Movie ID: ").strip()
        room_id = input("Room ID: ").strip()
        starts_at = input("Starts at: ").strip()

        try:
            result = self.create_showtime_use_case.execute(
                movie_id=movie_id,
                room_id=room_id,
                starts_at=starts_at,
            )

            print("\nShowtime created successfully.")

        except Exception as exc:
            self._handle_admin_error(exc)

        self._pause()

    def _view_movies(self) -> None:
        """
        Muestra películas registradas.

        Notes
        -----
        Más adelante este método podrá:
        - paginar resultados,
        - mostrar estadísticas,
        - mostrar estado de cartelera.
        """
        print("\nMOVIES")
        print("-" * 50)

        movies = self.movie_service.list_movies()

        if not movies:
            print("No movies available.")
            self._pause()
            return

        for movie in movies:
            print(f"- {movie.title}")

        self._pause()

    def _view_showtimes(self) -> None:
        """
        Muestra funciones registradas.

        Notes
        -----
        Más adelante este método podrá:
        - mostrar ocupación,
        - mostrar disponibilidad,
        - mostrar conflictos,
        - mostrar métricas.
        """
        print("\nSHOWTIMES")
        print("-" * 50)

        showtimes = self.showtime_service.list_showtimes()

        if not showtimes:
            print("No showtimes available.")
            self._pause()
            return

        for showtime in showtimes:
            print(
                f"- {showtime.movie.title} "
                f"at {showtime.starts_at}"
            )

        self._pause()

    def _view_bookings(self) -> None:
        """
        Muestra bookings registrados.

        Notes
        -----
        Más adelante este método podrá:
        - filtrar reservas,
        - mostrar revenue,
        - mostrar estados,
        - exportar reportes.
        """
        print("\nBOOKINGS")
        print("-" * 50)

        bookings = self.booking_service.list_bookings()

        if not bookings:
            print("No bookings available.")
            self._pause()
            return

        for booking in bookings:
            print(
                f"- Booking {booking.booking_id} "
                f"({booking.status})"
            )

        self._pause()

    def _handle_invalid_option(self) -> None:
        """
        Maneja opciones inválidas.
        """
        print("\nInvalid option.")

    def _handle_admin_error(
        self,
        exc: Exception,
    ) -> None:
        """
        Maneja errores administrativos.

        Parameters
        ----------
        exc : Exception
            Error capturado.

        Notes
        -----
        Más adelante este método podrá:
        - categorizar errores,
        - mostrar validaciones específicas,
        - registrar auditoría.
        """
        print("\nOperation failed.")
        print(str(exc))

        if self.logger:
            self.logger.error(
                "Admin operation failed: %s",
                exc,
            )

    def _pause(self) -> None:
        """
        Pausa interacción CLI.
        """
        input("\nPress ENTER to continue...")


"""
Ejemplo conceptual futuro
-------------------------

    admin_commands = AdminCommands(
        create_movie_use_case=create_movie_uc,
        create_showtime_use_case=create_showtime_uc,
        movie_service=movie_service,
        showtime_service=showtime_service,
        booking_service=booking_service,
    )

    admin_commands.run()

Flujo esperado
--------------
ADMIN PANEL
    ├── create movie
    ├── create showtime
    ├── view movies
    ├── view showtimes
    ├── view bookings
    └── back

Importante
----------
Este módulo NO contiene lógica del negocio.

Solamente coordina:
- navegación,
- renderizado,
- formularios,
- interacción administrativa CLI.
"""
"""
ShowtimeCommands.

Este archivo define el módulo interactivo de navegación relacionado con
funciones/showtimes dentro de la aplicación CLI.

IMPORTANTE
----------
Este archivo representa una pantalla interactiva guiada por menús.

NO es:
- un parser de terminal,
- un comando UNIX,
- un script aislado.

En cambio, representa:
- navegación,
- flujo visual,
- selección de horarios,
- interacción guiada.

¿Por qué existe?
----------------
Porque después de seleccionar una película, el usuario necesita:
- consultar funciones,
- revisar horarios,
- verificar disponibilidad,
- seleccionar una función,
- avanzar hacia compra de tickets.

Este módulo coordina exactamente ese flujo.

Responsabilidad principal
-------------------------
Coordinar interacción CLI relacionada con funciones/showtimes.

Relación con otros módulos
--------------------------
Este módulo trabajará junto con:

- `ShowtimeService`
    Consulta de funciones.

- `BookingService`
    Flujo de reservas.

- `ShowtimeDTO`
    Transporte de funciones.

- `BookingDTO`
    Transporte de reservas.

- `MovieCommands`
    Navegación desde películas.

- `BookingCommands`
    Flujo de compra.

Qué debe resolver este módulo
-----------------------------
- renderizar showtimes,
- mostrar horarios,
- mostrar disponibilidad,
- permitir selección,
- navegar hacia booking,
- controlar flujo visual.

Qué NO debe hacer
-----------------
- No debe contener lógica de negocio.
- No debe bloquear seats directamente.
- No debe procesar pagos.
- No debe acceder directamente a persistencia.
- No debe modificar entidades.

Toda lógica operacional vive en:
- services,
- use cases,
- dominio.

Este módulo solamente:
- muestra información,
- recibe input,
- delega operaciones.

Cómo debe sentirse
------------------
Como una aplicación interactiva real de consola.

Ejemplo conceptual:

==================================================
                SHOWTIMES
==================================================

Movie: Interstellar

1. 14:00 - Room A
2. 17:30 - Room B
3. 21:00 - IMAX

0. Back

Select a showtime:

Importante
----------
Este archivo representa navegación interactiva CLI.
"""

from __future__ import annotations

from typing import List, Optional


class ShowtimeCommands:
    """
    Módulo interactivo de funciones/showtimes.

    Notes
    -----
    Esta clase coordina:
    - visualización de horarios,
    - navegación de funciones,
    - selección de showtimes,
    - transición hacia booking.
    """

    def __init__(
        self,
        showtime_service,
        booking_commands=None,
        logger=None,
    ):
        """
        Inicializa módulo de showtimes.

        Parameters
        ----------
        showtime_service : object
            Servicio de funciones.

        booking_commands : object, optional
            Navegación de bookings.

        logger : object, optional
            Sistema de logging.
        """
        self.showtime_service = showtime_service
        self.booking_commands = booking_commands
        self.logger = logger

        self.is_running = False

    def run(
        self,
        movie_id: Optional[str] = None,
    ) -> None:
        """
        Ejecuta navegación de funciones.

        Parameters
        ----------
        movie_id : str, optional
            Permite filtrar showtimes por película.

        Flujo esperado
        --------------
        1. cargar showtimes,
        2. renderizar horarios,
        3. seleccionar función,
        4. mostrar disponibilidad,
        5. avanzar a booking,
        6. volver atrás.
        """
        self.is_running = True

        while self.is_running:
            self._render_showtimes_menu(movie_id)

            option = self._read_user_option()

            self._handle_showtime_option(
                option=option,
                movie_id=movie_id,
            )

    def stop(self) -> None:
        """
        Finaliza navegación actual.
        """
        self.is_running = False

    def _render_showtimes_menu(
        self,
        movie_id: Optional[str] = None,
    ) -> None:
        """
        Renderiza menú de funciones.

        Parameters
        ----------
        movie_id : str, optional
            Película filtrada.

        Notes
        -----
        Más adelante este método podrá:
        - renderizar tablas,
        - paginar resultados,
        - mostrar ocupación,
        - mostrar horarios enriquecidos.
        """
        print("\n" + "=" * 50)
        print("                SHOWTIMES")
        print("=" * 50)

        showtimes = self._load_showtimes(movie_id)

        if not showtimes:
            print("\nNo showtimes available.")
            print("\n0. Back")
            return

        for index, showtime in enumerate(showtimes, start=1):
            room_name = getattr(
                showtime.room,
                "room_name",
                "Unknown Room",
            )

            starts_at = getattr(
                showtime,
                "starts_at",
                "Unknown Time",
            )

            print(f"{index}. {starts_at} - {room_name}")

        print("\n0. Back")

    def _load_showtimes(
        self,
        movie_id: Optional[str] = None,
    ) -> List:
        """
        Carga funciones disponibles.

        Parameters
        ----------
        movie_id : str, optional
            Filtro de película.

        Returns
        -------
        list
            Lista de ShowtimeDTO.

        Notes
        -----
        Más adelante este método podrá:
        - filtrar por fecha,
        - filtrar por disponibilidad,
        - ordenar horarios,
        - excluir funciones agotadas.
        """
        if movie_id:
            return self.showtime_service.list_showtimes_by_movie(
                movie_id,
            )

        return self.showtime_service.list_showtimes()

    def _read_user_option(self) -> str:
        """
        Lee input del usuario.

        Returns
        -------
        str
            Valor ingresado.
        """
        return input("\nSelect a showtime: ").strip()

    def _handle_showtime_option(
        self,
        option: str,
        movie_id: Optional[str] = None,
    ) -> None:
        """
        Procesa opción seleccionada.

        Parameters
        ----------
        option : str
            Opción ingresada.

        movie_id : str, optional
            Filtro activo.
        """
        if option == "0":
            self.stop()
            return

        if not option.isdigit():
            self._handle_invalid_option()
            return

        showtime_index = int(option) - 1

        showtimes = self._load_showtimes(movie_id)

        if showtime_index < 0 or showtime_index >= len(showtimes):
            self._handle_invalid_option()
            return

        selected_showtime = showtimes[showtime_index]

        self._open_showtime_details(selected_showtime)

    def _open_showtime_details(
        self,
        showtime,
    ) -> None:
        """
        Muestra detalles de función.

        Parameters
        ----------
        showtime : ShowtimeDTO
            Función seleccionada.

        Notes
        -----
        Más adelante este método podrá:
        - mostrar mapa de seats,
        - mostrar ocupación,
        - mostrar pricing,
        - mostrar idioma,
        - mostrar formatos especiales.
        """
        print("\n" + "=" * 50)
        print("SHOWTIME DETAILS")
        print("=" * 50)

        print(f"Movie: {showtime.movie.title}")
        print(f"Room: {showtime.room.room_name}")
        print(f"Starts at: {showtime.starts_at}")

        if getattr(showtime, "language", None):
            print(f"Language: {showtime.language}")

        if getattr(showtime, "format_type", None):
            print(f"Format: {showtime.format_type}")

        self._render_showtime_actions(showtime)

    def _render_showtime_actions(
        self,
        showtime,
    ) -> None:
        """
        Renderiza acciones disponibles para función.

        Parameters
        ----------
        showtime : ShowtimeDTO
            Función objetivo.
        """
        print("\n1. Purchase Tickets")
        print("0. Back")

        option = input("\nSelect an option: ").strip()

        if option == "1":
            self._open_booking_flow(showtime)

    def _open_booking_flow(
        self,
        showtime,
    ) -> None:
        """
        Navega hacia flujo de booking.

        Parameters
        ----------
        showtime : ShowtimeDTO
            Función seleccionada.

        Notes
        -----
        Más adelante este método delegará control hacia:
        - selección de seats,
        - lock de asientos,
        - confirmación,
        - pagos.
        """
        if self.booking_commands is None:
            print("\nBooking system unavailable.")
            return

        self.booking_commands.run(
            showtime_id=showtime.showtime_id,
        )

    def _handle_invalid_option(self) -> None:
        """
        Maneja opciones inválidas.
        """
        print("\nInvalid option. Please try again.")

    def _pause(self) -> None:
        """
        Pausa interacción CLI.

        Notes
        -----
        Helper reutilizable de navegación.
        """
        input("\nPress ENTER to continue...")


"""
Ejemplo conceptual futuro
-------------------------

    showtime_commands = ShowtimeCommands(
        showtime_service=showtime_service,
        booking_commands=booking_commands,
    )

    showtime_commands.run(movie_id="movie-001")

Flujo esperado
--------------
SHOWTIMES
    ├── list showtimes
    ├── select showtime
    ├── view details
    ├── purchase tickets
    └── back

Importante
----------
Este módulo NO contiene lógica de negocio.

Solamente coordina:
- navegación,
- renderizado,
- interacción visual,
- transición entre pantallas.
"""
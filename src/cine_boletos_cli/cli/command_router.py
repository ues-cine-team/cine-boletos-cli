"""
CommandRouter.

Este archivo define el núcleo de navegación de la aplicación de consola del
sistema de boletos de cine.

IMPORTANTE
----------
Esta NO es una CLI tradicional basada en comandos tipo:

    app create-movie --title ...

En cambio, este sistema utiliza una:

    CLI interactiva guiada por menús

Es decir:
- el usuario navega entre pantallas,
- selecciona opciones,
- avanza entre menús,
- vuelve atrás,
- interactúa paso a paso.

¿Por qué existe este router?
----------------------------
Porque toda aplicación interactiva necesita un controlador central de
navegación.

Este archivo será responsable de:
- mostrar el menú principal,
- controlar el ciclo principal de la app,
- enrutar navegación,
- delegar a módulos especializados,
- manejar interacción básica.

Responsabilidad principal
-------------------------
Coordinar la navegación entre pantallas CLI.

Relación con otros módulos
--------------------------
Este router trabajará junto con:

- `movie_commands.py`
    Navegación del catálogo.

- `showtime_commands.py`
    Navegación de funciones.

- `booking_commands.py`
    Flujo de compra.

- `admin_commands.py`
    Operaciones administrativas.

Qué debe resolver este router
-----------------------------
- ciclo principal,
- navegación,
- menús,
- selección de opciones,
- validación básica,
- flujo entre pantallas.

Qué NO debe hacer
-----------------
- No debe contener lógica del dominio.
- No debe procesar pagos.
- No debe modificar entidades.
- No debe acceder directamente a persistencia.
- No debe contener reglas del negocio.

El router solamente coordina navegación.

Cómo debe sentirse el sistema
-----------------------------
La experiencia debe parecer una aplicación real de consola.

Ejemplo conceptual:

==================================================
            CINEMA TICKET SYSTEM
==================================================

1. View Movies
2. View Showtimes
3. Purchase Tickets
4. Admin Panel
5. Exit

Select an option:

Importante
----------
Este archivo representa la capa de interacción humana del sistema.
"""

from __future__ import annotations

from typing import Callable, Dict


class CommandRouter:
    """
    Router principal de navegación CLI.

    Notes
    -----
    Esta clase coordina:
    - menús,
    - navegación,
    - pantallas,
    - flujo interactivo.
    """

    def __init__(
        self,
        movie_commands=None,
        showtime_commands=None,
        booking_commands=None,
        admin_commands=None,
        logger=None,
    ):
        """
        Inicializa el router principal.

        Parameters
        ----------
        movie_commands : object, optional
            Módulo de películas.

        showtime_commands : object, optional
            Módulo de funciones.

        booking_commands : object, optional
            Módulo de reservas.

        admin_commands : object, optional
            Módulo administrativo.

        logger : object, optional
            Sistema de logging.
        """
        self.movie_commands = movie_commands
        self.showtime_commands = showtime_commands
        self.booking_commands = booking_commands
        self.admin_commands = admin_commands
        self.logger = logger

        self.is_running = False

    def run(self) -> None:
        """
        Ejecuta la aplicación CLI.

        Flujo esperado
        --------------
        1. iniciar aplicación,
        2. mostrar menú principal,
        3. recibir input,
        4. navegar entre pantallas,
        5. finalizar sistema.

        Notes
        -----
        Este método representa el ciclo principal interactivo.
        """
        self.is_running = True

        self._show_welcome_screen()

        while self.is_running:
            self._render_main_menu()

            option = self._read_user_option()

            self._handle_main_menu_option(option)

    def stop(self) -> None:
        """
        Detiene la aplicación CLI.

        Notes
        -----
        Este método terminará el ciclo principal.
        """
        self.is_running = False

    def _show_welcome_screen(self) -> None:
        """
        Muestra pantalla inicial del sistema.

        Notes
        -----
        Más adelante aquí podrá existir:
        - branding,
        - banners,
        - versión,
        - información operacional.
        """
        print("=" * 50)
        print("        CINEMA TICKET SYSTEM")
        print("=" * 50)

    def _render_main_menu(self) -> None:
        """
        Renderiza el menú principal.

        Notes
        -----
        Este menú será el punto central de navegación.
        """
        print("\nMAIN MENU")
        print("-" * 50)
        print("1. View Movies")
        print("2. View Showtimes")
        print("3. Purchase Tickets")
        print("4. Admin Panel")
        print("5. Exit")

    def _read_user_option(self) -> str:
        """
        Lee opción ingresada por usuario.

        Returns
        -------
        str
            Valor ingresado.

        Notes
        -----
        Más adelante aquí podrá existir:
        - validación avanzada,
        - normalización,
        - sanitización.
        """
        return input("\nSelect an option: ").strip()

    def _handle_main_menu_option(
        self,
        option: str,
    ) -> None:
        """
        Procesa opción seleccionada.

        Parameters
        ----------
        option : str
            Opción ingresada.
        """
        handlers: Dict[str, Callable[[], None]] = {
            "1": self._open_movies_menu,
            "2": self._open_showtimes_menu,
            "3": self._open_booking_menu,
            "4": self._open_admin_menu,
            "5": self.stop,
        }

        handler = handlers.get(option)

        if handler is None:
            self._handle_invalid_option()
            return

        handler()

    def _open_movies_menu(self) -> None:
        """
        Navega al módulo de películas.

        Notes
        -----
        Delegará control a `movie_commands.py`.
        """
        if self.movie_commands:
            self.movie_commands.run()

    def _open_showtimes_menu(self) -> None:
        """
        Navega al módulo de funciones.

        Notes
        -----
        Delegará control a `showtime_commands.py`.
        """
        if self.showtime_commands:
            self.showtime_commands.run()

    def _open_booking_menu(self) -> None:
        """
        Navega al flujo de compra.

        Notes
        -----
        Delegará control a `booking_commands.py`.
        """
        if self.booking_commands:
            self.booking_commands.run()

    def _open_admin_menu(self) -> None:
        """
        Navega al panel administrativo.

        Notes
        -----
        Delegará control a `admin_commands.py`.
        """
        if self.admin_commands:
            self.admin_commands.run()

    def _handle_invalid_option(self) -> None:
        """
        Maneja opciones inválidas.

        Notes
        -----
        Más adelante aquí podrá existir:
        - reintentos,
        - validación avanzada,
        - mensajes enriquecidos,
        - auditoría.
        """
        print("\nInvalid option. Please try again.")

    def _pause(self) -> None:
        """
        Pausa interacción hasta confirmación del usuario.

        Notes
        -----
        Este helper será útil entre pantallas.
        """
        input("\nPress ENTER to continue...")


"""
Ejemplo conceptual futuro
-------------------------

    router = CommandRouter(
        movie_commands=movie_commands,
        showtime_commands=showtime_commands,
        booking_commands=booking_commands,
        admin_commands=admin_commands,
    )

    router.run()

Flujo esperado
--------------
MAIN MENU
    ├── Movies
    ├── Showtimes
    ├── Purchase Tickets
    ├── Admin
    └── Exit

Importante
----------
Este router NO contiene lógica de negocio.

Solamente coordina:
- navegación,
- menús,
- flujo interactivo,
- experiencia de consola.
"""
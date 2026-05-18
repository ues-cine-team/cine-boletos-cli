"""
BookingCommands.

Este archivo define el módulo interactivo relacionado con reservas y compra de
tickets dentro de la aplicación CLI.

IMPORTANTE
----------
Este archivo representa:
- navegación interactiva,
- flujo guiado,
- experiencia de compra,
- pantallas CLI.

NO representa:
- lógica de negocio,
- persistencia,
- pagos reales,
- locking real.

Toda lógica operacional vive en:
- services,
- use cases,
- entidades del dominio.

Este módulo solamente:
- guía al usuario,
- muestra información,
- recibe input,
- delega operaciones.

¿Por qué existe?
----------------
Porque comprar tickets es el flujo principal del sistema.

Este módulo será responsable de:
- selección de seats,
- visualización de disponibilidad,
- confirmación de compra,
- inicio de pagos,
- cancelaciones,
- navegación del flujo de booking.

Responsabilidad principal
-------------------------
Coordinar interacción CLI relacionada con bookings.

Relación con otros módulos
--------------------------
Este módulo trabajará junto con:

- `PurchaseTicketsUseCase`
    Flujo principal de compra.

- `BookingService`
    Operaciones de reservas.

- `SeatService`
    Disponibilidad y selección.

- `PaymentService`
    Flujo de pagos.

- `BookingDTO`
    Transporte de reservas.

- `ShowtimeDTO`
    Información de funciones.

- `ShowtimeCommands`
    Navegación desde funciones.

Qué debe resolver este módulo
-----------------------------
- renderizar mapa de seats,
- permitir selección,
- confirmar compra,
- iniciar pagos,
- mostrar resultados,
- manejar navegación visual.

Qué NO debe hacer
-----------------
- No debe bloquear seats directamente.
- No debe modificar entidades.
- No debe acceder a repositories.
- No debe manejar transacciones.
- No debe contener reglas del dominio.

Cómo debe sentirse
------------------
Como una aplicación real de compra de tickets.

Ejemplo conceptual:

==================================================
            SELECT YOUR SEATS
==================================================

SCREEN THIS WAY
--------------------------------

A [ ] [ ] [X] [ ]
B [ ] [X] [ ] [ ]
C [ ] [ ] [ ] [ ]

[ ] available
[X] booked

Select seats:

Importante
----------
Este archivo representa la experiencia interactiva principal del sistema.
"""

from __future__ import annotations

from typing import List, Optional


class BookingCommands:
    """
    Módulo interactivo de bookings y compra.

    Notes
    -----
    Esta clase coordina:
    - selección de seats,
    - flujo de compra,
    - confirmaciones,
    - pagos,
    - navegación de booking.
    """

    def __init__(
        self,
        purchase_tickets_use_case,
        booking_service,
        seat_service,
        payment_service,
        logger=None,
    ):
        """
        Inicializa módulo de booking.

        Parameters
        ----------
        purchase_tickets_use_case : object
            Caso de uso principal de compra.

        booking_service : object
            Servicio de reservas.

        seat_service : object
            Servicio de asientos.

        payment_service : object
            Servicio de pagos.

        logger : object, optional
            Sistema de logging.
        """
        self.purchase_tickets_use_case = purchase_tickets_use_case
        self.booking_service = booking_service
        self.seat_service = seat_service
        self.payment_service = payment_service
        self.logger = logger

        self.is_running = False

    def run(
        self,
        showtime_id: Optional[str] = None,
    ) -> None:
        """
        Ejecuta flujo interactivo de booking.

        Parameters
        ----------
        showtime_id : str, optional
            Función objetivo.

        Flujo esperado
        --------------
        1. cargar seats,
        2. renderizar mapa,
        3. seleccionar seats,
        4. confirmar selección,
        5. iniciar pago,
        6. completar booking,
        7. mostrar resultado.
        """
        self.is_running = True

        while self.is_running:
            self._render_booking_screen(showtime_id)

            selected_seats = self._read_seat_selection()

            if not selected_seats:
                self.stop()
                continue

            self._confirm_booking_flow(
                showtime_id=showtime_id,
                selected_seats=selected_seats,
            )

    def stop(self) -> None:
        """
        Finaliza flujo actual.
        """
        self.is_running = False

    def _render_booking_screen(
        self,
        showtime_id: Optional[str],
    ) -> None:
        """
        Renderiza pantalla principal de selección.

        Parameters
        ----------
        showtime_id : str, optional
            Función activa.

        Notes
        -----
        Más adelante este método podrá:
        - renderizar mapas reales,
        - mostrar estados en tiempo real,
        - mostrar pricing dinámico,
        - mostrar leyendas visuales.
        """
        print("\n" + "=" * 50)
        print("            SELECT YOUR SEATS")
        print("=" * 50)

        print("\nSCREEN THIS WAY")
        print("-" * 32)

        seat_map = self._load_seat_map(showtime_id)

        self._render_seat_map(seat_map)

        print("\n[ ] available")
        print("[X] booked")
        print("[L] locked")

        print("\nType seat ids separated by commas.")
        print("Example: A1,A2")

        print("Type 0 to go back.")

    def _load_seat_map(
        self,
        showtime_id: Optional[str],
    ):
        """
        Carga mapa conceptual de seats.

        Parameters
        ----------
        showtime_id : str, optional
            Función activa.

        Notes
        -----
        Más adelante este método podrá:
        - consultar disponibilidad real,
        - renderizar estados live,
        - integrar locks temporales.
        """
        return self.seat_service.get_seat_map(showtime_id)

    def _render_seat_map(
        self,
        seat_map,
    ) -> None:
        """
        Renderiza mapa de asientos.

        Parameters
        ----------
        seat_map : object
            Estructura de seats.

        Notes
        -----
        Más adelante este método podrá:
        - renderizar ASCII avanzado,
        - usar colores,
        - mostrar ocupación,
        - destacar seats seleccionados.
        """
        for row in seat_map:
            print(row)

    def _read_seat_selection(self) -> List[str]:
        """
        Lee selección de seats.

        Returns
        -------
        list[str]
            Lista de seat ids seleccionados.
        """
        raw_input = input("\nSelect seats: ").strip()

        if raw_input == "0":
            return []

        selected_seats = [
            seat.strip()
            for seat in raw_input.split(",")
            if seat.strip()
        ]

        return selected_seats

    def _confirm_booking_flow(
        self,
        showtime_id: Optional[str],
        selected_seats: List[str],
    ) -> None:
        """
        Ejecuta confirmación conceptual de booking.

        Parameters
        ----------
        showtime_id : str, optional
            Función objetivo.

        selected_seats : list[str]
            Seats elegidos.

        Notes
        -----
        Más adelante este método coordinará:
        - locking,
        - validación,
        - pagos,
        - confirmación final,
        - rollback,
        - compensaciones.
        """
        self._render_booking_summary(
            showtime_id=showtime_id,
            selected_seats=selected_seats,
        )

        confirmed = self._ask_booking_confirmation()

        if not confirmed:
            return

        self._execute_purchase(
            showtime_id=showtime_id,
            selected_seats=selected_seats,
        )

    def _render_booking_summary(
        self,
        showtime_id: Optional[str],
        selected_seats: List[str],
    ) -> None:
        """
        Muestra resumen conceptual de compra.

        Parameters
        ----------
        showtime_id : str, optional
            Función seleccionada.

        selected_seats : list[str]
            Seats elegidos.
        """
        print("\n" + "=" * 50)
        print("BOOKING SUMMARY")
        print("=" * 50)

        print(f"Showtime: {showtime_id}")
        print(f"Seats: {', '.join(selected_seats)}")

    def _ask_booking_confirmation(self) -> bool:
        """
        Solicita confirmación del usuario.

        Returns
        -------
        bool
            True si usuario confirma.
        """
        option = input("\nConfirm purchase? (y/n): ").strip().lower()

        return option == "y"

    def _execute_purchase(
        self,
        showtime_id: Optional[str],
        selected_seats: List[str],
    ) -> None:
        """
        Ejecuta compra conceptual.

        Parameters
        ----------
        showtime_id : str, optional
            Función seleccionada.

        selected_seats : list[str]
            Seats elegidos.

        Notes
        -----
        Más adelante este método utilizará:
        - PurchaseTicketsUseCase,
        - idempotencia,
        - locking,
        - pagos reales,
        - UoW,
        - compensación.
        """
        print("\nProcessing purchase...")

        try:
            result = self.purchase_tickets_use_case.execute(
                showtime_id=showtime_id,
                seat_ids=selected_seats,
            )

            self._render_purchase_success(result)

        except Exception as exc:
            self._handle_purchase_error(exc)

    def _render_purchase_success(
        self,
        booking_result,
    ) -> None:
        """
        Muestra resultado exitoso.

        Parameters
        ----------
        booking_result : object
            Resultado del booking.

        Notes
        -----
        Más adelante este método podrá:
        - mostrar tickets,
        - mostrar QR,
        - mostrar payment info,
        - mostrar booking id.
        """
        print("\nPurchase completed successfully.")

        self._pause()

        self.stop()

    def _handle_purchase_error(
        self,
        exc: Exception,
    ) -> None:
        """
        Maneja errores de booking.

        Parameters
        ----------
        exc : Exception
            Error capturado.

        Notes
        -----
        Más adelante este método podrá:
        - mostrar errores específicos,
        - manejar expiraciones,
        - manejar conflictos de concurrencia,
        - sugerir retry.
        """
        print("\nPurchase failed.")
        print(str(exc))

        if self.logger:
            self.logger.error(
                "Booking flow failed: %s",
                exc,
            )

        self._pause()

    def _pause(self) -> None:
        """
        Pausa interacción CLI.
        """
        input("\nPress ENTER to continue...")


"""
Ejemplo conceptual futuro
-------------------------

    booking_commands = BookingCommands(
        purchase_tickets_use_case=use_case,
        booking_service=booking_service,
        seat_service=seat_service,
        payment_service=payment_service,
    )

    booking_commands.run(showtime_id="showtime-001")

Flujo esperado
--------------
BOOKING FLOW
    ├── render seat map
    ├── select seats
    ├── confirm selection
    ├── execute payment
    ├── create booking
    └── render result

Importante
----------
Este módulo NO contiene reglas del negocio.

Solamente coordina:
- experiencia de usuario,
- navegación,
- interacción CLI,
- flujo visual de compra.
"""
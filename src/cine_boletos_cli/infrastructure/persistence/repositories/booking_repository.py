"""
Este archivo define el contrato del repositorio de bookings.
¿Por qué existe?
Porque la entidad Booking no debe saber cómo se guarda en una base de datos ni
cómo se consulta desde fuera. Esa responsabilidad se separa aquí para mantener
el dominio limpio y evitar mezclar reglas de negocio con detalles técnicos.
¿Cómo se usará más adelante?
- `booking_service.py` usará este repositorio para crear, buscar y actualizar reservas.
- `purchase_tickets.py` lo usará para persistir el resultado de la compra.
- `cancel_booking.py` lo usará para recuperar y cancelar reservas.
- `notification_worker.py` o futuros procesos podrían consultarlo para saber
  qué reservas fueron confirmadas, canceladas o fallidas.
Qué debe resolver este repositorio:
- guardar bookings,
- recuperar bookings por ID,
- listar reservas por cliente o por función,
- actualizar estados de pago o cancelación,
- ayudar a mantener trazabilidad sobre el flujo de compra.
Importante:
Este archivo NO debe decidir si una reserva puede confirmarse o cancelarse.
Eso pertenece a la entidad Booking y a los servicios del dominio.
El repositorio solo guarda, recupera y actualiza datos.
"""


class BookingRepository:
    """
    Repositorio de reservas en memoria.
    Usa un diccionario interno para simular persistencia.
    """

    def __init__(self):
        # Diccionario: booking_id -> objeto Booking
        self._storage = {}

    def save(self, booking):
        """
        Guarda o actualiza una reserva.

        Args:
            booking: Entidad Booking ya validada por el dominio.

        Returns:
            Booking: la reserva persistida.
        """
        self._storage[booking.id] = booking
        return booking

    def get_by_id(self, booking_id):
        """
        Busca una reserva por su identificador.

        Args:
            booking_id: Identificador formal de la reserva.

        Returns:
            Booking | None: la reserva encontrada o None si no existe.
        """
        return self._storage.get(booking_id, None)

    def list_by_customer(self, customer_id):
        """
        Devuelve todas las reservas de un cliente.

        Args:
            customer_id: Identificador del cliente.

        Returns:
            list[Booking]: lista de reservas asociadas al cliente.
        """
        return [
            booking for booking in self._storage.values()
            if getattr(booking, "customer_id", None) == customer_id
        ]

    def list_by_showtime(self, showtime_id):
        """
        Devuelve todas las reservas de una función.

        Args:
            showtime_id: Identificador de la función.

        Returns:
            list[Booking]: lista de reservas asociadas a la función.
        """
        return [
            booking for booking in self._storage.values()
            if getattr(booking, "showtime_id", None) == showtime_id
        ]

    def list_by_status(self, status):
        """
        Devuelve todas las reservas que coinciden con un estado concreto.

        Args:
            status: Estado de la reserva (PENDING, CONFIRMED, CANCELLED).

        Returns:
            list[Booking]: lista filtrada por estado.
        """
        return [
            booking for booking in self._storage.values()
            if getattr(booking, "status", None) == status
        ]

    def delete(self, booking_id):
        """
        Elimina una reserva del almacenamiento.

        Args:
            booking_id: Identificador de la reserva.
        """
        if booking_id in self._storage:
            del self._storage[booking_id]

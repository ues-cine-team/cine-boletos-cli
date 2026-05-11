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
    Contrato del repositorio de reservas.

    Más adelante aquí irá la implementación real de persistencia.
    """

    def save(self, booking):
        """
        Guarda o actualiza una reserva.

        Debe usarse cuando:
        - se crea una nueva booking,
        - cambia el estado a confirmado,
        - se cancela,
        - falla el pago,
        - o se actualiza cualquier dato persistido.

        Args:
            booking:
                Entidad Booking ya validada por el dominio.

        Returns:
            Booking: la reserva persistida.
        """
        pass

    def get_by_id(self, booking_id):
        """
        Busca una reserva por su identificador.

        Args:
            booking_id:
                Identificador formal de la reserva.

        Returns:
            Booking | None: la reserva encontrada o None si no existe.
        """
        pass

    def list_by_customer(self, customer_id):
        """
        Devuelve todas las reservas de un cliente.

        Args:
            customer_id:
                Identificador del cliente.

        Returns:
            list[Booking]: lista de reservas asociadas al cliente.
        """
        pass

    def list_by_showtime(self, showtime_id):
        """
        Devuelve todas las reservas de una función.

        Args:
            showtime_id:
                Identificador de la función.

        Returns:
            list[Booking]: lista de reservas asociadas a la función.
        """
        pass

    def list_by_status(self, status):
        """
        Devuelve todas las reservas que coinciden con un estado concreto.

        Args:
            status:
                Estado de la reserva.
                Ejemplos:
                - PENDING
                - CONFIRMED
                - CANCELLED

        Returns:
            list[Booking]: lista filtrada por estado.
        """
        pass

    def delete(self, booking_id):
        """
        Elimina una reserva o la marca como inactiva, según la estrategia del sistema.

        Args:
            booking_id:
                Identificador de la reserva.

        Returns:
            None
        """
        pass
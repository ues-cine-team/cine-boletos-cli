"""
Este archivo define el contrato del repositorio de asientos.
¿Por qué existe?
Porque la entidad Seat no debe saber cómo se guarda ni cómo se lee desde una
base de datos. Esa responsabilidad se separa aquí para mantener el dominio
limpio y evitar mezclar reglas de negocio con detalles técnicos.
¿Cómo se usará más adelante?
- `seat_service.py` usará este repositorio para consultar y actualizar asientos.
- `booking_service.py` lo usará para validar disponibilidad y confirmar cambios.
- `seat_lock_manager.py` podrá apoyarse en los estados persistidos de los asientos.
- `lock_expiry_worker.py` lo usará para liberar asientos que ya vencieron.
Qué debe resolver este repositorio:
- buscar asientos,
- guardar cambios de estado,
- listar asientos por función,
- consultar disponibilidad,
- recuperar asientos bloqueados, comprados o libres.
Importante:
Este archivo NO debe contener reglas de negocio.
No debe decidir si un asiento puede bloquearse o comprarse.
Eso pertenece a la entidad Seat y a los servicios del dominio.
El repositorio solo guarda, recupera y actualiza datos.
"""


class SeatRepository:
    """
    Repositorio de asientos en memoria.
    Usa un diccionario interno para simular persistencia.
    """

    def __init__(self):
        # Diccionario: seat_id -> objeto Seat
        self._storage = {}

    def save(self, seat):
        """
        Guarda o actualiza un asiento.

        Args:
            seat: Entidad Seat ya validada por el dominio.

        Returns:
            Seat: el asiento persistido.
        """
        self._storage[seat.id] = seat
        return seat

    def get_by_id(self, seat_id):
        """
        Busca un asiento por su identidad.

        Args:
            seat_id: Identificador del asiento.

        Returns:
            Seat | None: el asiento encontrado o None si no existe.
        """
        return self._storage.get(seat_id, None)

    def list_by_showtime(self, showtime_id):
        """
        Devuelve todos los asientos de una función.

        Args:
            showtime_id: Identificador de la función.

        Returns:
            list[Seat]: lista de asientos asociados a la función.
        """
        return [
            seat for seat in self._storage.values()
            if getattr(seat, "showtime_id", None) == showtime_id
        ]

    def list_available(self, showtime_id):
        """
        Devuelve los asientos disponibles de una función.

        Args:
            showtime_id: Identificador de la función.

        Returns:
            list[Seat]: asientos libres para reservar.
        """
        return [
            seat for seat in self.list_by_showtime(showtime_id)
            if getattr(seat, "status", None) == "AVAILABLE"
        ]

    def list_locked(self, showtime_id):
        """
        Devuelve los asientos bloqueados de una función.

        Args:
            showtime_id: Identificador de la función.

        Returns:
            list[Seat]: asientos actualmente bloqueados.
        """
        return [
            seat for seat in self.list_by_showtime(showtime_id)
            if getattr(seat, "status", None) == "LOCKED"
        ]

    def list_booked(self, showtime_id):
        """
        Devuelve los asientos ya comprados de una función.

        Args:
            showtime_id: Identificador de la función.

        Returns:
            list[Seat]: asientos confirmados como vendidos.
        """
        return [
            seat for seat in self.list_by_showtime(showtime_id)
            if getattr(seat, "status", None) == "BOOKED"
        ]

    def delete(self, seat_id):
        """
        Elimina un asiento del almacenamiento.

        Args:
            seat_id: Identificador del asiento.
        """
        if seat_id in self._storage:
            del self._storage[seat_id]

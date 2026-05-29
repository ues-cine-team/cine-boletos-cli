"""
Este archivo define el contrato del repositorio de funciones (Showtime).
¿Por qué existe?
Porque la entidad Showtime no debe saber cómo se guarda ni cómo se consulta
desde una base de datos. Esa responsabilidad se separa aquí para mantener el
dominio limpio y evitar mezclar reglas de negocio con detalles técnicos.
¿Cómo se usará más adelante?
- `showtime_service.py` usará este repositorio para crear y administrar funciones.
- `purchase_tickets.py` consultará funciones activas antes de permitir compras.
- `booking_service.py` verificará disponibilidad y estado de una función.
Qué debe resolver este repositorio:
- guardar funciones,
- recuperar funciones por ID,
- buscar funciones activas,
- listar funciones por película o sala,
- consultar funciones futuras,
- actualizar cambios de estado u horarios.
Importante:
Este archivo NO debe decidir:
- si una función puede cancelarse,
- si ya comenzó,
- si todavía acepta reservas,
- ni si sus cambios son válidos.
Eso pertenece a la entidad Showtime y a los servicios del dominio.
El repositorio solo guarda, recupera y actualiza datos.
"""

from datetime import datetime


class ShowtimeRepository:
    """
    Repositorio de funciones en memoria.
    Usa un diccionario interno para simular persistencia.
    """

    def __init__(self):
        # Diccionario: showtime_id -> objeto Showtime
        self._storage = {}

    def save(self, showtime):
        """
        Guarda o actualiza una función.

        Args:
            showtime: Entidad Showtime ya validada por el dominio.

        Returns:
            Showtime: la función persistida.
        """
        self._storage[showtime.id] = showtime
        return showtime

    def get_by_id(self, showtime_id):
        """
        Busca una función por su identificador.

        Args:
            showtime_id: Identificador formal de la función.

        Returns:
            Showtime | None: la función encontrada o None si no existe.
        """
        return self._storage.get(showtime_id, None)

    def list_active(self):
        """
        Devuelve todas las funciones activas.

        Returns:
            list[Showtime]: funciones activas.
        """
        return [
            showtime for showtime in self._storage.values()
            if getattr(showtime, "is_active", False)
        ]

    def list_by_movie(self, movie_id):
        """
        Devuelve todas las funciones asociadas a una película.

        Args:
            movie_id: Identificador de la película.

        Returns:
            list[Showtime]: funciones de la película.
        """
        return [
            showtime for showtime in self._storage.values()
            if getattr(showtime, "movie_id", None) == movie_id
        ]

    def list_by_room(self, room_id):
        """
        Devuelve todas las funciones asociadas a una sala.

        Args:
            room_id: Identificador de la sala.

        Returns:
            list[Showtime]: funciones de la sala.
        """
        return [
            showtime for showtime in self._storage.values()
            if getattr(showtime, "room_id", None) == room_id
        ]

    def list_future_showtimes(self):
        """
        Devuelve funciones futuras que todavía no comienzan.

        Returns:
            list[Showtime]: funciones futuras.
        """
        now = datetime.now()
        return [
            showtime for showtime in self._storage.values()
            if getattr(showtime, "start_time", None) and showtime.start_time > now
        ]

    def delete(self, showtime_id):
        """
        Elimina una función del almacenamiento.

        Args:
            showtime_id: Identificador de la función.
        """
        if showtime_id in self._storage:
            del self._storage[showtime_id]

from datetime import datetime


class ShowtimeRepository:
    """
    Repositorio de funciones en memoria.
    """

    def __init__(self):
        self._storage = {}

    def save(self, showtime):
        """
        Guarda o actualiza una función.
        """
        self._storage[
            showtime.showtime_id
        ] = showtime

        return showtime

    def get_by_id(self, showtime_id):
        """
        Recupera una función por id.
        """
        return self._storage.get(showtime_id)

    def exists(self, showtime_id):
        """
        Verifica si una función existe.
        """
        return showtime_id in self._storage

    def list_all(self):
        """
        Devuelve todas las funciones.
        """
        return list(
            self._storage.values()
        )

    def list_active(self):
        """
        Devuelve únicamente funciones activas.
        """
        return [
            showtime
            for showtime in self._storage.values()
            if showtime.is_active()
        ]

    def list_by_movie(self, movie_id):
        """
        Devuelve funciones de una película.
        """
        return [
            showtime
            for showtime in self._storage.values()
            if showtime.movie_id == movie_id
        ]

    def list_by_room(self, room_id):
        """
        Devuelve funciones de una sala.
        """
        return [
            showtime
            for showtime in self._storage.values()
            if showtime.room_id == room_id
        ]

    def list_future_showtimes(self):
        """
        Devuelve funciones futuras.
        """
        now = datetime.utcnow()

        return [
            showtime
            for showtime in self._storage.values()
            if showtime.starts_at > now
        ]

    def delete(self, showtime_id):
        """
        Elimina una función.
        """
        return self._storage.pop(
            showtime_id,
            None,
        )

    def count(self):
        """
        Devuelve cantidad total de funciones.
        """
        return len(self._storage)

    def clear(self):
        """
        Limpia repositorio.
        """
        self._storage.clear()
class RoomRepository:
    """
    Repositorio de salas en memoria.
    Usa un diccionario interno para simular persistencia.
    """

    def __init__(self):
        self._storage = {}

    def save(self, room):
        """
        Guarda o actualiza una sala.
        """
        self._storage[room.room_id] = room
        return room

    def get_by_id(self, room_id):
        """
        Recupera una sala por id.
        """
        return self._storage.get(room_id)

    def exists(self, room_id):
        """
        Verifica si una sala existe.
        """
        return room_id in self._storage

    def list_all(self):
        """
        Devuelve todas las salas.
        """
        return list(self._storage.values())

    def list_active(self):
        """
        Devuelve únicamente salas activas.
        """
        return [
            room
            for room in self._storage.values()
            if room.is_active()
        ]

    def delete(self, room_id):
        """
        Elimina una sala.
        """
        return self._storage.pop(room_id, None)

    def count(self):
        """
        Devuelve la cantidad total de salas.
        """
        return len(self._storage)

    def clear(self):
        """
        Limpia completamente el repositorio.
        Útil para pruebas.
        """
        self._storage.clear()
"""
Repositorio de asientos por función.

Responsable únicamente de persistir y recuperar
objetos ShowtimeSeat.
"""


class ShowtimeSeatRepository:

    def __init__(self):
        self._storage = {}

    def save(self, showtime_seat):
        """
        Guarda o actualiza un ShowtimeSeat.
        """
        self._storage[
            showtime_seat.showtime_seat_id
        ] = showtime_seat

        return showtime_seat

    def get_by_id(
        self,
        showtime_seat_id,
    ):
        """
        Recupera un asiento por función.
        """
        return self._storage.get(
            showtime_seat_id
        )

    def list_all(self):
        """
        Devuelve todos los registros.
        """
        return list(
            self._storage.values()
        )

    def list_by_showtime(
        self,
        showtime_id,
    ):
        """
        Devuelve todos los asientos
        de una función.
        """
        return [
            seat
            for seat in self._storage.values()
            if seat.showtime_id == showtime_id
        ]

    def list_available(
        self,
        showtime_id,
    ):
        """
        Devuelve asientos disponibles.
        """
        return [
            seat
            for seat in self.list_by_showtime(
                showtime_id
            )
            if seat.is_available()
        ]

    def list_locked(
        self,
        showtime_id,
    ):
        """
        Devuelve asientos bloqueados.
        """
        return [
            seat
            for seat in self.list_by_showtime(
                showtime_id
            )
            if seat.is_locked()
        ]

    def list_booked(
        self,
        showtime_id,
    ):
        """
        Devuelve asientos vendidos.
        """
        return [
            seat
            for seat in self.list_by_showtime(
                showtime_id
            )
            if seat.is_booked()
        ]

    def delete(
        self,
        showtime_seat_id,
    ):
        """
        Elimina un registro.
        """
        return self._storage.pop(
            showtime_seat_id,
            None,
        )

    def count(self):
        """
        Cantidad total almacenada.
        """
        return len(
            self._storage
        )

    def clear(self):
        """
        Limpia repositorio.
        """
        self._storage.clear()
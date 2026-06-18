from __future__ import annotations

from cine_boletos_cli.domain.entities.room import Room


class RoomService:
    """
    Servicio encargado de coordinar operaciones sobre salas.
    """

    def __init__(
        self,
        room_repository,
    ):
        self.room_repository = room_repository

    def create_room(
        self,
        room_id: str,
        name: str,
        total_rows: int,
        seats_per_row: int,
        status: str,
    ):
        """
        Crea una nueva sala.
        """

        self.validate_room_data(
            room_id=room_id,
            name=name,
            total_rows=total_rows,
            seats_per_row=seats_per_row,
        )

        room = Room(
            room_id=room_id,
            name=name,
            total_rows=total_rows,
            seats_per_row=seats_per_row,
            status=status,
        )

        return self.room_repository.save(room)

    def get_room_by_id(
        self,
        room_id: str,
    ):
        """
        Recupera una sala por ID.
        """

        return self.room_repository.get_by_id(room_id)

    def list_rooms(self):
        """
        Devuelve todas las salas.
        """

        return self.room_repository.list_all()

    def list_active_rooms(self):
        """
        Devuelve únicamente salas activas.
        """

        return self.room_repository.list_active()

    def delete_room(
        self,
        room_id: str,
    ):
        """
        Elimina una sala.
        """

        room = self.room_repository.delete(room_id)

        if room is None:
            raise ValueError(
                f"Room '{room_id}' not found."
            )

        return room

    def validate_room_data(
        self,
        room_id: str,
        name: str,
        total_rows: int,
        seats_per_row: int,
    ) -> None:
        """
        Valida datos básicos de una sala.
        """

        if not room_id:
            raise ValueError(
                "room_id is required."
            )

        if not name:
            raise ValueError(
                "name is required."
            )

        if total_rows <= 0:
            raise ValueError(
                "total_rows must be greater than zero."
            )

        if seats_per_row <= 0:
            raise ValueError(
                "seats_per_row must be greater than zero."
            )
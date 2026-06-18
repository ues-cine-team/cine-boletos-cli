"""
CreateShowtimeUseCase.

Caso de uso encargado de registrar nuevas funciones.
"""

from cine_boletos_cli.application.services.showtime_service import (
    ShowtimeService,
)


class CreateShowtimeUseCase:
    """
    Caso de uso para creación de funciones.
    """

    def __init__(
        self,
        showtime_service: ShowtimeService,
    ):
        self.showtime_service = showtime_service

    def execute(
        self,
        movie_id: str,
        room_id: str,
        starts_at,
    ):
        return self.showtime_service.create_showtime(
            movie_id=movie_id,
            room_id=room_id,
            starts_at=starts_at,
        )
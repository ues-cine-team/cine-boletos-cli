from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import uuid4

from cine_boletos_cli.domain.entities.showtime import Showtime
from cine_boletos_cli.domain.value_objects.money import Money


class ShowtimeService:

    def __init__(
        self,
        showtime_repository,
        movie_repository,
        seat_repository=None,
    ):
        self.showtime_repository = showtime_repository
        self.movie_repository = movie_repository
        self.seat_repository = seat_repository

    def create_showtime(
        self,
        movie_id: str,
        room_id: str,
        starts_at: datetime,
    ):
        movie = self.movie_repository.get_by_id(
            movie_id
        )

        if movie is None:
            raise ValueError(
                f"Movie '{movie_id}' not found."
            )

        showtime = Showtime(
            showtime_id=str(uuid4()),
            movie_id=movie_id,
            room_id=room_id,
            starts_at=starts_at,
            duration_minutes=movie.duration_minutes,
            base_price=Money("5.00"),
        )

        return self.showtime_repository.save(
            showtime
        )

    def get_showtime_by_id(
        self,
        showtime_id: str,
    ):
        return self.showtime_repository.get_by_id(
            showtime_id
        )

    def list_showtimes(self):
        """
        Devuelve todas las funciones.
        """
        return self.showtime_repository.list_all()
    
    def list_showtimes_by_movie(
        self,
        movie_id: str,
    ):
        return self.showtime_repository.list_by_movie(
            movie_id
        )

    def list_available_showtimes(self):
        return self.showtime_repository.list_all()

    def can_sell_tickets(
        self,
        showtime_id: str,
    ) -> bool:

        showtime = self.get_showtime_by_id(
            showtime_id
        )

        if showtime is None:
            return False

        if showtime.is_cancelled():
            return False

        if showtime.has_finished():
            return False

        return True

    def cancel_showtime(
        self,
        showtime_id: str,
        reason: Optional[str] = None,
    ):
        showtime = self.get_showtime_by_id(
            showtime_id
        )

        if showtime is None:
            raise ValueError(
                f"Showtime '{showtime_id}' not found."
            )

        showtime.cancel()

        self.showtime_repository.save(
            showtime
        )

        return showtime
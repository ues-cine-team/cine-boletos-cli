"""
MovieService.

Servicio encargado de coordinar operaciones relacionadas con películas.
"""

from __future__ import annotations

from typing import Iterable, Optional
from uuid import uuid4

from cine_boletos_cli.domain.entities.movie import Movie


class MovieService:
    """
    Servicio encargado de coordinar operaciones sobre películas.
    """

    def __init__(
        self,
        movie_repository,
        showtime_repository=None,
    ):
        self.movie_repository = movie_repository
        self.showtime_repository = showtime_repository

    def create_movie(
        self,
        title: str,
        duration_minutes: int,
        classification: str,
        description: Optional[str] = None,
        genre: str = "UNDEFINED",
    ):
        """
        Crea una nueva película.
        """

        self.validate_movie_data(
            title=title,
            duration_minutes=duration_minutes,
            classification=classification,
        )

        movie = Movie(
            movie_id=str(uuid4()),
            title=title,
            duration_minutes=duration_minutes,
            classification=classification,
            genre=genre,
            description=description or "",
            status=Movie.UPCOMING,
        )

        return self.movie_repository.save(movie)

    def get_movie_by_id(self, movie_id: str):
        """
        Recupera una película por ID.
        """

        return self.movie_repository.get_by_id(movie_id)

    def list_movies(self):
        """
        Devuelve todas las películas.
        """

        return self.movie_repository.list_all()

    def list_now_showing(self) -> Iterable:
        """
        Devuelve únicamente películas activas.
        """

        return self.movie_repository.list_active()

    def activate_movie(self, movie_id: str):
        """
        Activa una película.
        """

        movie = self.movie_repository.get_by_id(movie_id)

        if movie is None:
            raise ValueError(
                f"Movie '{movie_id}' not found."
            )

        movie.activate()

        self.movie_repository.save(movie)

        return movie

    def deactivate_movie(
        self,
        movie_id: str,
        reason: Optional[str] = None,
    ):
        """
        Desactiva una película.
        """

        movie = self.movie_repository.get_by_id(movie_id)

        if movie is None:
            raise ValueError(
                f"Movie '{movie_id}' not found."
            )

        movie.archive()

        self.movie_repository.save(movie)

        return movie

    def update_movie(
        self,
        movie_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
    ):
        """
        Actualiza datos básicos de una película.
        """

        movie = self.movie_repository.get_by_id(movie_id)

        if movie is None:
            raise ValueError(
                f"Movie '{movie_id}' not found."
            )

        if title is not None:
            movie.rename(title)

        if description is not None:
            movie.update_description(description)

        self.movie_repository.save(movie)

        return movie

    def delete_movie(self, movie_id: str):
        """
        Elimina una película.
        """

        movie = self.movie_repository.delete(movie_id)

        if movie is None:
            raise ValueError(
                f"Movie '{movie_id}' not found."
            )

        return movie

    def can_schedule_showtimes(
        self,
        movie_id: str,
    ) -> bool:
        """
        Determina si una película puede programarse.
        """

        movie = self.movie_repository.get_by_id(movie_id)

        if movie is None:
            return False

        return movie.is_active()

    def validate_movie_data(
        self,
        title: str,
        duration_minutes: int,
        classification: str,
    ) -> None:
        """
        Valida datos básicos de una película.
        """

        if not title or not title.strip():
            raise ValueError(
                "Movie title is required."
            )

        if duration_minutes <= 0:
            raise ValueError(
                "Movie duration must be greater than zero."
            )

        if duration_minutes > 500:
            raise ValueError(
                "Movie duration exceeds allowed limit."
            )

        if not classification:
            raise ValueError(
                "Movie classification is required."
            )
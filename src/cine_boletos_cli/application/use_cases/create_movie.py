"""
CreateMovieUseCase.

Caso de uso encargado de registrar nuevas películas.
"""

from cine_boletos_cli.application.services.movie_service import MovieService


class CreateMovieUseCase:
    """
    Caso de uso para creación de películas.
    """

    def __init__(
        self,
        movie_service: MovieService,
    ):
        self.movie_service = movie_service

    def execute(
        self,
        title: str,
        duration_minutes: int,
        classification: str,
        description: str = "",
        genre: str = "UNDEFINED",
    ):
        """
        Ejecuta la creación de una película.

        Returns
        -------
        Movie
            Película creada.
        """

        return self.movie_service.create_movie(
            title=title,
            duration_minutes=duration_minutes,
            classification=classification,
            description=description,
            genre=genre,
        )
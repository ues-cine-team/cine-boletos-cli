from cine_boletos_cli.infrastructure.persistence.repositories.movie_repository import (
    MovieRepository,
)

from cine_boletos_cli.application.services.movie_service import (
    MovieService,
)

from cine_boletos_cli.application.use_cases.create_movie import (
    CreateMovieUseCase,
)

from cine_boletos_cli.cli.commands.admin_commands import (
    AdminCommands,
)

from cine_boletos_cli.cli.commands.movie_commands import (
    MovieCommands,
)

from cine_boletos_cli.cli.command_router import (
    CommandRouter,
)


def main():

    movie_repository = MovieRepository()

    movie_service = MovieService(
        movie_repository=movie_repository,
    )

    create_movie_use_case = CreateMovieUseCase(
        movie_service=movie_service,
    )

    movie_commands = MovieCommands(
        movie_service=movie_service,
    )

    admin_commands = AdminCommands(
        create_movie_use_case=create_movie_use_case,
        create_showtime_use_case=None,
        movie_service=movie_service,
        showtime_service=None,
        booking_service=None,
    )

    router = CommandRouter(
        movie_commands=movie_commands,
        admin_commands=admin_commands,
    )

    router.run()


if __name__ == "__main__":
    main()
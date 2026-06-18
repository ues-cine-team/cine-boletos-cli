from cine_boletos_cli.infrastructure.persistence.repositories.movie_repository import (
    MovieRepository,
)

from cine_boletos_cli.infrastructure.persistence.repositories.showtime_repository import (
    ShowtimeRepository,
)

from cine_boletos_cli.application.services.movie_service import (
    MovieService,
)

from cine_boletos_cli.application.services.showtime_service import (
    ShowtimeService,
)

from cine_boletos_cli.application.use_cases.create_movie import (
    CreateMovieUseCase,
)

from cine_boletos_cli.application.use_cases.create_showtime import (
    CreateShowtimeUseCase,
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

    # ==================================================
    # REPOSITORIES
    # ==================================================

    movie_repository = MovieRepository()

    showtime_repository = ShowtimeRepository()

    # ==================================================
    # SERVICES
    # ==================================================

    movie_service = MovieService(
        movie_repository=movie_repository,
        showtime_repository=showtime_repository,
    )

    showtime_service = ShowtimeService(
        showtime_repository=showtime_repository,
        movie_repository=movie_repository,
        seat_repository=None,
    )

    # ==================================================
    # USE CASES
    # ==================================================

    create_movie_use_case = CreateMovieUseCase(
        movie_service=movie_service,
    )

    create_showtime_use_case = CreateShowtimeUseCase(
        showtime_service=showtime_service,
    )

    # ==================================================
    # CLI COMMANDS
    # ==================================================

    movie_commands = MovieCommands(
        movie_service=movie_service,
        showtime_service=showtime_service,
    )

    admin_commands = AdminCommands(
        create_movie_use_case=create_movie_use_case,
        create_showtime_use_case=create_showtime_use_case,
        movie_service=movie_service,
        showtime_service=showtime_service,
        booking_service=None,
    )

    # ==================================================
    # ROUTER
    # ==================================================

    router = CommandRouter(
        movie_commands=movie_commands,
        admin_commands=admin_commands,
    )

    router.run()


if __name__ == "__main__":
    main()
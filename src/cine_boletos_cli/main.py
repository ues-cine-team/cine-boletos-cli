from cine_boletos_cli.infrastructure.persistence.repositories.movie_repository import (
    MovieRepository,
)

from cine_boletos_cli.infrastructure.persistence.repositories.showtime_repository import (
    ShowtimeRepository,
)

from cine_boletos_cli.infrastructure.persistence.repositories.showtime_seat_repository import (
    ShowtimeSeatRepository,
)

from cine_boletos_cli.infrastructure.persistence.repositories.booking_repository import (
    BookingRepository,
)

from cine_boletos_cli.infrastructure.persistence.repositories.room_repository import (
    RoomRepository,
)

from cine_boletos_cli.infrastructure.persistence.repositories.seat_repository import (
    SeatRepository,
)

from cine_boletos_cli.application.services.movie_service import (
    MovieService,
)

from cine_boletos_cli.application.services.showtime_service import (
    ShowtimeService,
)

from cine_boletos_cli.application.services.booking_service import (
    BookingService,
)

from cine_boletos_cli.application.services.room_service import (
    RoomService,
)

from cine_boletos_cli.application.services.showtime_seat_service import (
    ShowtimeSeatService,
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

from cine_boletos_cli.cli.commands.booking_commands import (
    BookingCommands,
)

from cine_boletos_cli.cli.command_router import (
    CommandRouter,
)

from cine_boletos_cli.domain.entities.seat import (
    Seat,
)

from cine_boletos_cli.shared.constants import (
    ROOM_ACTIVE,
)


def main():

    # ==================================================
    # REPOSITORIES
    # ==================================================

    movie_repository = MovieRepository()
    showtime_repository = ShowtimeRepository()
    showtime_seat_repository = ShowtimeSeatRepository()
    booking_repository = BookingRepository()
    room_repository = RoomRepository()
    seat_repository = SeatRepository()

    # ==================================================
    # SERVICES
    # ==================================================

    movie_service = MovieService(
        movie_repository=movie_repository,
        showtime_repository=showtime_repository,
    )

    room_service = RoomService(
        room_repository=room_repository,
    )

    showtime_service = ShowtimeService(
        showtime_repository=showtime_repository,
        movie_repository=movie_repository,
        seat_repository=seat_repository,
        showtime_seat_repository=showtime_seat_repository,
    )

    booking_service = BookingService(
        booking_repository=booking_repository,
        showtime_repository=showtime_repository,
        showtime_seat_repository=showtime_seat_repository,
    )

    showtime_seat_service = ShowtimeSeatService(
        showtime_seat_repository=showtime_seat_repository,
    )

    # ==================================================
    # BOOTSTRAP ROOM
    # ==================================================

    room_service.create_room(
        room_id="room-1",
        name="Main Room",
        total_rows=5,
        seats_per_row=5,
        status=ROOM_ACTIVE,
    )

    room = room_service.get_room_by_id(
        "room-1"
    )

    for seat_label in room.generate_seat_map():

        row = seat_label[0]
        number = int(seat_label[1:])

        seat = Seat(
            seat_id=f"{room.room_id}-{seat_label}",
            room_id=room.room_id,
            row=row,
            number=number,
        )

        seat_repository.save(seat)

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

    booking_commands = BookingCommands(
        movie_service=movie_service,
        showtime_service=showtime_service,
        showtime_seat_service=showtime_seat_service,
        booking_service=booking_service,
    )

    admin_commands = AdminCommands(
        create_movie_use_case=create_movie_use_case,
        create_showtime_use_case=create_showtime_use_case,
        movie_service=movie_service,
        showtime_service=showtime_service,
        booking_service=booking_service,
    )

    # ==================================================
    # ROUTER
    # ==================================================

    router = CommandRouter(
        movie_commands=movie_commands,
        booking_commands=booking_commands,
        admin_commands=admin_commands,
    )

    router.run()

    print(
        "Seats loaded:",
        seat_repository.count(),
    )

    print(
        "Showtime seats:",
        showtime_seat_repository.count(),
    )

    print(
        "Bookings:",
        booking_repository.count(),
    )


if __name__ == "__main__":
    main()
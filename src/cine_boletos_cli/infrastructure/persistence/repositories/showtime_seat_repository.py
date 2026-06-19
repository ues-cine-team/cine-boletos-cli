import json
from pathlib import Path

from cine_boletos_cli.domain.entities.showtime_seat import (
    ShowtimeSeat,
)


class ShowtimeSeatRepository:
    """
    Repositorio de asientos por función con persistencia JSON.
    """

    def __init__(
        self,
        file_path="data/showtime_seats.json",
    ):
        self.file_path = Path(file_path)
        self._storage = {}

        self._ensure_file_exists()
        self._load()

    def save(self, showtime_seat):
        self._storage[
            showtime_seat.showtime_seat_id
        ] = showtime_seat

        self._persist()

        return showtime_seat

    def get_by_id(
        self,
        showtime_seat_id,
    ):
        return self._storage.get(
            showtime_seat_id
        )

    def get_by_showtime_and_seat_id(
        self,
        showtime_id,
        seat_id,
    ):
        for seat in self._storage.values():
            if (
                seat.showtime_id == showtime_id
                and seat.seat_id == seat_id
            ):
                return seat

        return None

    def list_all(self):
        return list(
            self._storage.values()
        )

    def list_by_showtime(
        self,
        showtime_id,
    ):
        return [
            seat
            for seat in self._storage.values()
            if seat.showtime_id == showtime_id
        ]

    def list_available(
        self,
        showtime_id,
    ):
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
        showtime_seat = self._storage.pop(
            showtime_seat_id,
            None,
        )

        if showtime_seat is not None:
            self._persist()

        return showtime_seat

    def count(self):
        return len(
            self._storage
        )

    def clear(self):
        self._storage.clear()
        self._persist()

    def _ensure_file_exists(self):
        self.file_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        if not self.file_path.exists():
            self.file_path.write_text(
                "[]",
                encoding="utf-8",
            )

    def _load(self):
        raw_data = (
            self.file_path.read_text(
                encoding="utf-8"
            ).strip()
        )

        if not raw_data:
            raw_data = "[]"

        data = json.loads(raw_data)

        self._storage = {}

        for item in data:
            showtime_seat = ShowtimeSeat.from_dict(
                item
            )

            self._storage[
                showtime_seat.showtime_seat_id
            ] = showtime_seat

    def _persist(self):
        data = [
            showtime_seat.to_dict()
            for showtime_seat in self._storage.values()
        ]

        self.file_path.write_text(
            json.dumps(
                data,
                indent=4,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
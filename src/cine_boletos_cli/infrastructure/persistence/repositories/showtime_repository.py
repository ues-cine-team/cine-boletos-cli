import json
from pathlib import Path

from cine_boletos_cli.domain.entities.showtime import Showtime


class ShowtimeRepository:
    """
    Repositorio de funciones con persistencia JSON.
    """

    def __init__(
        self,
        file_path="data/showtimes.json",
    ):
        self.file_path = Path(file_path)
        self._storage = {}

        self._ensure_file_exists()
        self._load()

    def save(self, showtime):
        self._storage[
            showtime.showtime_id
        ] = showtime

        self._persist()

        return showtime

    def get_by_id(
        self,
        showtime_id,
    ):
        return self._storage.get(
            showtime_id
        )

    def exists(
        self,
        showtime_id,
    ):
        return (
            showtime_id
            in self._storage
        )

    def list_all(self):
        return list(
            self._storage.values()
        )

    def list_active(self):
        return [
            showtime
            for showtime in self._storage.values()
            if showtime.is_active()
        ]

    def list_by_movie(
        self,
        movie_id,
    ):
        return [
            showtime
            for showtime in self._storage.values()
            if showtime.movie_id == movie_id
        ]

    def list_by_room(
        self,
        room_id,
    ):
        return [
            showtime
            for showtime in self._storage.values()
            if showtime.room_id == room_id
        ]

    def list_future_showtimes(self):
        from datetime import datetime

        now = datetime.utcnow()

        return [
            showtime
            for showtime in self._storage.values()
            if showtime.starts_at > now
        ]

    def delete(
        self,
        showtime_id,
    ):
        showtime = self._storage.pop(
            showtime_id,
            None,
        )

        if showtime is not None:
            self._persist()

        return showtime

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

            showtime = (
                Showtime.from_dict(
                    item
                )
            )

            self._storage[
                showtime.showtime_id
            ] = showtime

    def _persist(self):
        data = [
            showtime.to_dict()
            for showtime in self._storage.values()
        ]

        self.file_path.write_text(
            json.dumps(
                data,
                indent=4,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
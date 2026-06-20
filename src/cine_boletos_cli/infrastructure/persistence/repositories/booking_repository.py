import json
from pathlib import Path

from cine_boletos_cli.domain.entities.booking import Booking


class BookingRepository:
    """
    Repositorio de reservas con persistencia JSON.
    """

    def __init__(
        self,
        file_path="data/bookings.json",
    ):
        self.file_path = Path(file_path)
        self._storage = {}

        self._ensure_file_exists()
        self._load()

    def save(self, booking):
        self._storage[
            booking.booking_id
        ] = booking

        self._persist()

        return booking

    def get_by_id(
        self,
        booking_id,
    ):
        return self._storage.get(
            booking_id
        )

    def list_all(self):
        return list(
            self._storage.values()
        )

    def list_by_customer(
        self,
        customer_id,
    ):
        return [
            booking
            for booking in self._storage.values()
            if booking.customer_id == customer_id
        ]

    def list_by_showtime(
        self,
        showtime_id,
    ):
        return [
            booking
            for booking in self._storage.values()
            if booking.showtime_id == showtime_id
        ]

    def list_by_status(
        self,
        status,
    ):
        return [
            booking
            for booking in self._storage.values()
            if booking.status == status
        ]

    def delete(
        self,
        booking_id,
    ):
        booking = self._storage.pop(
            booking_id,
            None,
        )

        if booking is not None:
            self._persist()

        return booking

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
            booking = Booking.from_dict(
                item
            )

            self._storage[
                booking.booking_id
            ] = booking

    def _persist(self):
        data = [
            booking.to_dict()
            for booking in self._storage.values()
        ]

        self.file_path.write_text(
            json.dumps(
                data,
                indent=4,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
class BookingRepository:
    """
    Repositorio de reservas en memoria.
    """

    def __init__(self):
        self._storage = {}

    def save(self, booking):
        self._storage[
            booking.booking_id
        ] = booking

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
        return self._storage.pop(
            booking_id,
            None,
        )

    def count(self):
        return len(
            self._storage
        )

    def clear(self):
        self._storage.clear()
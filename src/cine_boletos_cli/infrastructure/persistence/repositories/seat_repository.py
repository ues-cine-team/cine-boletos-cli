class SeatRepository:

    def __init__(self):
        self._storage = {}

    def save(self, seat):
        self._storage[seat.seat_id] = seat
        return seat

    def get_by_id(self, seat_id):
        return self._storage.get(seat_id)

    def list_all(self):
        return list(self._storage.values())

    def delete(self, seat_id):
        return self._storage.pop(seat_id, None)

    def count(self):
        return len(self._storage)
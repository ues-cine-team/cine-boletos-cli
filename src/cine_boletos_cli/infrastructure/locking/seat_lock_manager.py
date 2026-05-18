"""
SeatLockManager

Este módulo se encarga de bloquear asientos de forma temporal para evitar que
dos usuarios compren el mismo asiento al mismo tiempo.

¿Por qué existe?
Porque el sistema de boletos necesita una forma segura de decir:
"este asiento ya está siendo usado por otra compra".

¿Cómo se relaciona con el resto del sistema?
- `seat.py` representa el estado del asiento.
- `seat_service.py` usará este manager para bloquear y liberar asientos.
- `booking_service.py` lo usará durante el flujo de compra.
- `lock_expiry_worker.py` lo usará para liberar locks vencidos.
- `seat_repository.py` guardará el estado persistido del asiento.

Idea general:
1. Un usuario selecciona un asiento.
2. El sistema lo bloquea por un tiempo corto.
3. Si paga bien, el asiento queda BOOKED.
4. Si no paga o se vence el tiempo, el asiento vuelve a AVAILABLE.

Ejemplo simple de uso:

    lock_id = "booking-123"

    lock_manager.lock_seat(
        showtime_id="showtime-1",
        seat_id="A1",
        lock_id=lock_id,
        ttl_seconds=300,
    )

    if lock_manager.is_locked("showtime-1", "A1"):
        print("El asiento ya está reservado temporalmente")

    lock_manager.release_lock(
        showtime_id="showtime-1",
        seat_id="A1",
        lock_id=lock_id,
    )
"""


class SeatLockManager:
    """
    Gestiona el bloqueo temporal de asientos.
    """

    def lock_seat(self, showtime_id, seat_id, lock_id, ttl_seconds):
        """
        Bloquea un asiento temporalmente.

        Debe impedir que otro usuario bloquee el mismo asiento mientras el
        lock siga activo.
        """
        pass

    def release_lock(self, showtime_id, seat_id, lock_id):
        """
        Libera un lock si pertenece al mismo dueño que lo creó.
        """
        pass

    def is_locked(self, showtime_id, seat_id):
        """
        Indica si el asiento está actualmente bloqueado.
        """
        pass

    def is_lock_expired(self, showtime_id, seat_id):
        """
        Indica si el lock ya venció.
        """
        pass

    def renew_lock(self, showtime_id, seat_id, lock_id, ttl_seconds):
        """
        Renueva el tiempo de vida del lock.
        """
        pass

    def clear_expired_locks(self):
        """
        Limpia los locks que ya vencieron.
        Este método será útil para el worker de expiración.
        """
        pass
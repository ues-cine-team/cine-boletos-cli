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

import time


class SeatLockManager:
    """
    Gestiona el bloqueo temporal de asientos.

    Internamente usa un diccionario con esta estructura:
    {
        (showtime_id, seat_id): {
            "lock_id": "booking-123",
            "expires_at": 1234567890.0   <- timestamp Unix
        }
    }
    """

    def __init__(self):
        # Diccionario que guarda los locks activos
        self._locks = {}

    def lock_seat(self, showtime_id, seat_id, lock_id, ttl_seconds):
        """
        Bloquea un asiento temporalmente.

        Debe impedir que otro usuario bloquee el mismo asiento mientras el
        lock siga activo.

        Parameters
        ----------
        showtime_id : str
            ID de la función (horario).
        seat_id : str
            ID del asiento.
        lock_id : str
            Identificador único del lock (ej: "booking-123").
        ttl_seconds : int
            Tiempo de vida del lock en segundos.

        Raises
        ------
        RuntimeError
            Si el asiento ya está bloqueado por otro lock activo.
        """
        key = (showtime_id, seat_id)

        # Si ya existe un lock activo y no ha vencido, no permitir
        if key in self._locks and not self.is_lock_expired(showtime_id, seat_id):
            raise RuntimeError(
                f"El asiento {seat_id} de la función {showtime_id} "
                f"ya está bloqueado."
            )

        # Registrar el lock con su tiempo de expiración
        self._locks[key] = {
            "lock_id": lock_id,
            "expires_at": time.time() + ttl_seconds,
        }

    def release_lock(self, showtime_id, seat_id, lock_id):
        """
        Libera un lock si pertenece al mismo dueño que lo creó.

        Parameters
        ----------
        showtime_id : str
            ID de la función.
        seat_id : str
            ID del asiento.
        lock_id : str
            Identificador del lock a liberar.

        Notes
        -----
        Solo el dueño original del lock puede liberarlo.
        Esto evita que otro proceso libere un lock ajeno.
        """
        key = (showtime_id, seat_id)

        if key not in self._locks:
            return  # No hay lock, nada que liberar

        # Solo liberar si el lock_id coincide con el dueño
        if self._locks[key]["lock_id"] == lock_id:
            del self._locks[key]

    def is_locked(self, showtime_id, seat_id):
        """
        Indica si el asiento está actualmente bloqueado y el lock es válido.

        Parameters
        ----------
        showtime_id : str
            ID de la función.
        seat_id : str
            ID del asiento.

        Returns
        -------
        bool
            True si el asiento tiene un lock activo y no vencido.
        """
        key = (showtime_id, seat_id)

        if key not in self._locks:
            return False

        # Si el lock venció, no cuenta como bloqueado
        return not self.is_lock_expired(showtime_id, seat_id)

    def is_lock_expired(self, showtime_id, seat_id):
        """
        Indica si el lock ya venció.

        Parameters
        ----------
        showtime_id : str
            ID de la función.
        seat_id : str
            ID del asiento.

        Returns
        -------
        bool
            True si el lock existe pero ya pasó su tiempo de vida.
        """
        key = (showtime_id, seat_id)

        if key not in self._locks:
            return False

        return time.time() > self._locks[key]["expires_at"]

    def renew_lock(self, showtime_id, seat_id, lock_id, ttl_seconds):
        """
        Renueva el tiempo de vida del lock.

        Parameters
        ----------
        showtime_id : str
            ID de la función.
        seat_id : str
            ID del asiento.
        lock_id : str
            Identificador del lock a renovar.
        ttl_seconds : int
            Nuevo tiempo de vida en segundos.

        Notes
        -----
        Solo el dueño original puede renovar el lock.
        """
        key = (showtime_id, seat_id)

        if key not in self._locks:
            return  # No hay lock que renovar

        # Solo renovar si el lock_id coincide
        if self._locks[key]["lock_id"] == lock_id:
            self._locks[key]["expires_at"] = time.time() + ttl_seconds

    def clear_expired_locks(self):
        """
        Limpia los locks que ya vencieron.

        Este método será útil para el worker de expiración
        (lock_expiry_worker.py) que corre periódicamente.
        """
        # Identificar keys vencidas
        expired = [
            key for key, data in self._locks.items()
            if time.time() > data["expires_at"]
        ]

        # Eliminarlas
        for key in expired:
            del self._locks[key]

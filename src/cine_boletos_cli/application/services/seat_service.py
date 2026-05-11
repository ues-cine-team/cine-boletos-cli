"""
SeatService.

Este servicio coordina las operaciones sobre asientos dentro del flujo de
compra y reserva.

¿Por qué existe?
----------------
La entidad Seat contiene las reglas del asiento, pero no debe encargarse sola de
todo el flujo real del sistema. Este servicio actúa como capa de coordinación:
reúne la lógica del dominio con el bloqueo temporal, la persistencia y la unidad
de trabajo para mantener el sistema consistente.

Relación con otros módulos
--------------------------
- `domain.entities.seat.Seat` aporta las reglas y el estado del asiento.
- `infrastructure.persistence.repositories.seat_repository.SeatRepository`
  guarda y recupera asientos.
- `infrastructure.locking.seat_lock_manager.SeatLockManager` administra los
  locks temporales.
- `infrastructure.persistence.unit_of_work.UnitOfWork` agrupa cambios como una
  sola operación consistente.
- `application.services.booking_service.BookingService` usará este servicio
  durante la compra y la cancelación.
- `workers.lock_expiry_worker.LockExpiryWorker` puede apoyarse en este servicio
  para liberar locks vencidos.

Qué resuelve este servicio
--------------------------
- consultar asientos,
- listar disponibilidad,
- bloquear asientos,
- liberar asientos,
- confirmar asientos comprados,
- liberar locks vencidos,
- coordinar cambios persistentes sin romper consistencia.

Qué no debe hacer
-----------------
- No debe hablar con la CLI.
- No debe procesar pagos.
- No debe imprimir mensajes de usuario.
- No debe contener infraestructura concreta como SQL o Redis.
- No debe reemplazar las reglas del dominio que viven en `Seat`.

Ejemplo mental del flujo
------------------------
1. llega una solicitud para apartar un asiento,
2. el servicio busca el asiento,
3. valida que pueda bloquearse,
4. pide al `SeatLockManager` un lock temporal,
5. actualiza el estado del asiento,
6. guarda el cambio en el repositorio,
7. confirma la operación dentro de `UnitOfWork`.

Si algo falla, la operación debe mantenerse consistente.

Ejemplo de uso
--------------
>>> service.lock_seat(
...     showtime_id="showtime-1",
...     seat_id=SeatId(row="A", number=1),
...     lock_id="booking-123",
...     ttl_seconds=300,
... )

Si el asiento ya está bloqueado o ya fue comprado, el servicio debe rechazar la
operación con un error del dominio.

Este archivo está pensado como base lista para implementación y extensión.
"""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Optional, Sequence

from cine_boletos_cli.domain.exceptions.domain_errors import (
    SeatAlreadyBookedError,
    SeatLockedError,
    SeatNotAvailableError,
)
from cine_boletos_cli.domain.value_objects.seat_id import SeatId


class SeatService:
    """
    Servicio de aplicación para coordinar operaciones sobre asientos.

    Parameters
    ----------
    seat_repository : object
        Repositorio encargado de persistir asientos.

    seat_lock_manager : object
        Componente encargado de administrar locks temporales.

    unit_of_work : object
        Coordinador transaccional para agrupar cambios como una sola unidad.

    Notes
    -----
    Esta clase usa duck typing para ser flexible mientras el proyecto evoluciona.
    Más adelante puede conectarse con una implementación en memoria, SQL o Redis.
    """

    def __init__(self, seat_repository, seat_lock_manager, unit_of_work):
        self.seat_repository = seat_repository
        self.seat_lock_manager = seat_lock_manager
        self.unit_of_work = unit_of_work

    def get_seat(self, showtime_id: str, seat_id: SeatId):
        """
        Obtiene un asiento específico.

        Parameters
        ----------
        showtime_id : str
            Identificador de la función.

        seat_id : SeatId
            Identificador formal del asiento.

        Returns
        -------
        Seat | None
            El asiento encontrado o None si no existe.
        """
        return self.seat_repository.get_by_id(showtime_id=showtime_id, seat_id=seat_id)

    def list_available_seats(self, showtime_id: str):
        """
        Lista los asientos disponibles de una función.

        Parameters
        ----------
        showtime_id : str
            Identificador de la función.

        Returns
        -------
        list[Seat]
            Asientos que pueden reservarse o comprarse.
        """
        return self.seat_repository.list_available_seats(showtime_id)

    def list_locked_seats(self, showtime_id: str):
        """
        Lista los asientos bloqueados de una función.

        Parameters
        ----------
        showtime_id : str
            Identificador de la función.

        Returns
        -------
        list[Seat]
            Asientos bloqueados temporalmente.
        """
        return self.seat_repository.list_locked_seats(showtime_id)

    def lock_seat(
        self,
        showtime_id: str,
        seat_id: SeatId,
        lock_id: str,
        ttl_seconds: int,
    ):
        """
        Bloquea temporalmente un asiento.

        Parameters
        ----------
        showtime_id : str
            Identificador de la función.

        seat_id : SeatId
            Identificador del asiento.

        lock_id : str
            Identificador único del bloqueo.

        ttl_seconds : int
            Tiempo de vida del bloqueo en segundos.

        Returns
        -------
        Seat
            Asiento actualizado y bloqueado.

        Raises
        ------
        SeatNotAvailableError
            Si el asiento no existe o no puede bloquearse.

        SeatLockedError
            Si el asiento ya está bloqueado por otro usuario.

        SeatAlreadyBookedError
            Si el asiento ya fue comprado.
        """
        seat = self._require_seat(showtime_id, seat_id)

        if self._seat_is_booked(seat):
            raise SeatAlreadyBookedError("The seat is already booked.")

        if self._seat_is_locked(seat):
            if not self._seat_lock_expired(seat):
                raise SeatLockedError("The seat is already locked.")

        if not self._seat_is_available(seat) and not self._seat_lock_expired(seat):
            raise SeatNotAvailableError("The seat is not available.")

        locked_until = self._build_locked_until(ttl_seconds)

        with self.unit_of_work:
            acquired = self.seat_lock_manager.lock_seat(
                showtime_id=showtime_id,
                seat_id=seat_id,
                lock_id=lock_id,
                ttl_seconds=ttl_seconds,
            )

            if not acquired:
                raise SeatLockedError("Could not lock the seat.")

            seat.lock(lock_id=lock_id, locked_until=locked_until)
            self.seat_repository.save(seat)

        return seat

    def unlock_seat(self, showtime_id: str, seat_id: SeatId, lock_id: Optional[str] = None):
        """
        Libera un asiento bloqueado.

        Parameters
        ----------
        showtime_id : str
            Identificador de la función.

        seat_id : SeatId
            Identificador del asiento.

        lock_id : str, optional
            Identificador del lock si se desea validar el dueño.

        Returns
        -------
        Seat
            Asiento liberado.
        """
        seat = self._require_seat(showtime_id, seat_id)

        with self.unit_of_work:
            self.seat_lock_manager.release_lock(
                showtime_id=showtime_id,
                seat_id=seat_id,
                lock_id=lock_id,
            )
            seat.unlock()
            self.seat_repository.save(seat)

        return seat

    def confirm_seat(self, showtime_id: str, seat_id: SeatId, lock_id: Optional[str] = None):
        """
        Marca un asiento como comprado.

        Parameters
        ----------
        showtime_id : str
            Identificador de la función.

        seat_id : SeatId
            Identificador del asiento.

        lock_id : str, optional
            Identificador del lock asociado.

        Returns
        -------
        Seat
            Asiento confirmado como vendido.

        Raises
        ------
        SeatAlreadyBookedError
            Si el asiento ya fue confirmado.

        SeatNotAvailableError
            Si el asiento no está bloqueado correctamente.
        """
        seat = self._require_seat(showtime_id, seat_id)

        if self._seat_is_booked(seat):
            raise SeatAlreadyBookedError("The seat is already booked.")

        if not self._seat_is_locked(seat) and not self.seat_lock_manager.is_locked(showtime_id, seat_id):
            raise SeatNotAvailableError("The seat must be locked before booking.")

        with self.unit_of_work:
            seat.book()
            self.seat_lock_manager.release_lock(
                showtime_id=showtime_id,
                seat_id=seat_id,
                lock_id=lock_id,
            )
            self.seat_repository.save(seat)

        return seat

    def release_expired_locks(self, showtime_id: Optional[str] = None):
        """
        Libera locks vencidos y sincroniza el estado persistido.

        Parameters
        ----------
        showtime_id : str, optional
            Si se proporciona, solo se revisan asientos de esa función.

        Returns
        -------
        int
            Cantidad de asientos liberados.
        """
        expired_seats = self.seat_repository.find_expired_locks()
        released = 0

        for seat in expired_seats:
            if showtime_id is not None and seat.showtime_id != showtime_id:
                continue

            with self.unit_of_work:
                old_lock_id = getattr(seat, "lock_id", None)
                seat.unlock()
                self.seat_repository.save(seat)
                self.seat_lock_manager.release_lock(
                    showtime_id=seat.showtime_id,
                    seat_id=seat.seat_id,
                    lock_id=old_lock_id,
                )
                released += 1

        return released

    def _require_seat(self, showtime_id: str, seat_id: SeatId):
        """
        Obtiene un asiento y falla si no existe.

        Parameters
        ----------
        showtime_id : str
            Identificador de la función.

        seat_id : SeatId
            Identificador del asiento.

        Returns
        -------
        Seat
            Asiento encontrado.

        Raises
        ------
        SeatNotAvailableError
            Si el asiento no existe.
        """
        seat = self.seat_repository.get_by_id(showtime_id=showtime_id, seat_id=seat_id)

        if seat is None:
            raise SeatNotAvailableError("The seat does not exist.")

        return seat

    @staticmethod
    def _build_locked_until(ttl_seconds: int) -> datetime:
        """
        Calcula el momento exacto de expiración del lock.

        Parameters
        ----------
        ttl_seconds : int
            Tiempo de vida del bloqueo.

        Returns
        -------
        datetime
            Momento en el que el bloqueo vence.
        """
        return datetime.utcnow() + timedelta(seconds=ttl_seconds)

    @staticmethod
    def _seat_is_available(seat) -> bool:
        """
        Determina si el asiento está disponible.

        Uses
        ----
        Usa el método `is_available()` si existe; de lo contrario, intenta
        inferirlo desde el estado del objeto.
        """
        method = getattr(seat, "is_available", None)
        if callable(method):
            return bool(method())

        status = getattr(seat, "status", None)
        return str(status).upper() == "AVAILABLE"

    @staticmethod
    def _seat_is_locked(seat) -> bool:
        """
        Determina si el asiento está bloqueado.
        """
        method = getattr(seat, "is_locked", None)
        if callable(method):
            return bool(method())

        status = getattr(seat, "status", None)
        return str(status).upper() == "LOCKED"

    @staticmethod
    def _seat_is_booked(seat) -> bool:
        """
        Determina si el asiento ya fue comprado.
        """
        method = getattr(seat, "is_booked", None)
        if callable(method):
            return bool(method())

        status = getattr(seat, "status", None)
        return str(status).upper() == "BOOKED"

    @staticmethod
    def _seat_lock_expired(seat) -> bool:
        """
        Determina si el lock del asiento ya expiró.
        """
        method = getattr(seat, "is_lock_expired", None)
        if callable(method):
            return bool(method())

        locked_until = getattr(seat, "locked_until", None)
        if locked_until is None:
            return False

        return datetime.utcnow() >= locked_until
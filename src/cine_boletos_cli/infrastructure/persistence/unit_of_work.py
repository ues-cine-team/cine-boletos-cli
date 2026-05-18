"""
Unit Of Work (Unidad de Trabajo).

Este módulo coordina múltiples operaciones de persistencia como una sola unidad
lógica y consistente.

¿Por qué existe?
----------------
En este sistema una compra puede involucrar:

- bloqueo de asientos,
- creación de bookings,
- actualización de estados,
- confirmación de pagos,
- cambios en múltiples repositories.

Si una parte falla, el sistema NO debe quedar parcialmente actualizado.

La Unit Of Work garantiza:

- consistencia,
- atomicidad,
- rollback ante errores,
- coordinación entre repositories.

Ejemplo conceptual
------------------
>>> with unit_of_work:
...     seat = unit_of_work.seat_repository.get_by_id(seat_id)
...     seat.lock(...)
...
...     booking = Booking(...)
...
...     unit_of_work.booking_repository.save(booking)
...
...     unit_of_work.commit()

Si cualquier operación falla:
- rollback automático,
- no quedan datos inconsistentes,
- no quedan asientos bloqueados parcialmente.

Importante
-----------
Este componente NO contiene reglas de negocio.

NO decide:
- si un asiento puede bloquearse,
- si una compra es válida,
- si un booking puede confirmarse.

Eso pertenece al dominio.

La Unit Of Work solamente coordina persistencia y transacciones.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from typing import Iterable


@dataclass
class UnitOfWork:
    """
    Coordina una transacción lógica entre múltiples repositories.

    Este componente permite agrupar operaciones relacionadas para que
    se ejecuten como una sola unidad consistente.

    Parameters
    ----------
    seat_repository : Any, optional
        Repositorio de asientos.

    booking_repository : Any, optional
        Repositorio de reservas.

    movie_repository : Any, optional
        Repositorio de películas.

    showtime_repository : Any, optional
        Repositorio de funciones.

    Notes
    -----
    Más adelante estos repositories podrían conectarse a:
    - PostgreSQL,
    - SQLAlchemy,
    - Redis,
    - almacenamiento distribuido,
    - sistemas event-driven.
    """

    seat_repository: Any = None
    booking_repository: Any = None
    movie_repository: Any = None
    showtime_repository: Any = None

    _active: bool = field(default=False, init=False)
    _committed: bool = field(default=False, init=False)
    _rolled_back: bool = field(default=False, init=False)

    def __enter__(self) -> "UnitOfWork":
        """
        Abre el contexto transaccional.

        Este método permite usar:

        >>> with unit_of_work:

        Returns
        -------
        UnitOfWork
            Instancia activa de la unidad de trabajo.

        Notes
        -----
        Más adelante aquí podrían abrirse:
        - conexiones SQL,
        - sesiones ORM,
        - locks distribuidos,
        - recursos transaccionales.
        """
        self._active = True
        self._committed = False
        self._rolled_back = False

        self._begin_repositories()

        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        """
        Cierra el contexto transaccional.

        Si ocurrió una excepción:
        - ejecuta rollback.

        Si todo salió bien:
        - ejecuta commit.

        Parameters
        ----------
        exc_type : type | None
            Tipo de excepción ocurrida.

        exc : Exception | None
            Instancia de la excepción.

        tb : traceback | None
            Traceback asociado al error.

        Returns
        -------
        bool
            False para permitir que las excepciones continúen propagándose.
        """
        try:
            if exc_type is not None:
                self.rollback()
            else:
                self.commit()

        finally:
            self._active = False
            self._close_repositories()

        return False

    def attach(
        self,
        *,
        seat_repository=None,
        booking_repository=None,
        movie_repository=None,
        showtime_repository=None,
    ) -> None:
        """
        Adjunta o reemplaza repositories.

        Parameters
        ----------
        seat_repository : Any, optional
            Repositorio de asientos.

        booking_repository : Any, optional
            Repositorio de reservas.

        movie_repository : Any, optional
            Repositorio de películas.

        showtime_repository : Any, optional
            Repositorio de funciones.
        """
        if seat_repository is not None:
            self.seat_repository = seat_repository

        if booking_repository is not None:
            self.booking_repository = booking_repository

        if movie_repository is not None:
            self.movie_repository = movie_repository

        if showtime_repository is not None:
            self.showtime_repository = showtime_repository

    def repositories(self) -> tuple:
        """
        Devuelve todos los repositories registrados.

        Returns
        -------
        tuple
            Tuple con todos los repositories configurados.
        """
        return (
            self.seat_repository,
            self.booking_repository,
            self.movie_repository,
            self.showtime_repository,
        )

    def commit(self) -> None:
        """
        Confirma todos los cambios realizados.

        Raises
        ------
        RuntimeError
            Si la Unit Of Work no está activa.

        RuntimeError
            Si ya se ejecutó rollback.

        Notes
        -----
        Cada repository puede implementar su propio método `commit`.
        """
        self._ensure_active()

        if self._rolled_back:
            raise RuntimeError(
                "Cannot commit after rollback has been executed."
            )

        if self._committed:
            return

        for repository in self._iter_repositories():
            self._call_hook(repository, "commit")

        self._committed = True

    def rollback(self) -> None:
        """
        Revierte todos los cambios realizados.

        Raises
        ------
        RuntimeError
            Si la Unit Of Work no está activa.

        RuntimeError
            Si ya se ejecutó commit.

        Notes
        -----
        El rollback se ejecuta en orden inverso para reducir riesgos de
        inconsistencias entre backends dependientes.
        """
        self._ensure_active()

        if self._committed:
            raise RuntimeError(
                "Cannot rollback after commit has been executed."
            )

        if self._rolled_back:
            return

        for repository in reversed(list(self._iter_repositories())):
            self._call_hook(repository, "rollback")

        self._rolled_back = True

    def is_active(self) -> bool:
        """
        Indica si la unidad de trabajo está activa.

        Returns
        -------
        bool
            True si el contexto transaccional está abierto.
        """
        return self._active

    def has_committed(self) -> bool:
        """
        Indica si ya se confirmó la transacción.

        Returns
        -------
        bool
            True si commit ya fue ejecutado.
        """
        return self._committed

    def has_rolled_back(self) -> bool:
        """
        Indica si ya se ejecutó rollback.

        Returns
        -------
        bool
            True si rollback ya fue ejecutado.
        """
        return self._rolled_back

    def _ensure_active(self) -> None:
        """
        Verifica que la Unit Of Work esté activa.

        Raises
        ------
        RuntimeError
            Si la transacción no está activa.
        """
        if not self._active:
            raise RuntimeError("UnitOfWork is not active.")

    def _iter_repositories(self) -> Iterable[Any]:
        """
        Itera sobre los repositories registrados.

        Yields
        ------
        Any
            Repositories configurados y válidos.
        """
        for repository in self.repositories():
            if repository is not None:
                yield repository

    def _begin_repositories(self) -> None:
        """
        Ejecuta el hook `begin` en cada repository si existe.
        """
        for repository in self._iter_repositories():
            self._call_hook(repository, "begin")

    def _close_repositories(self) -> None:
        """
        Ejecuta el hook `close` en cada repository si existe.
        """
        for repository in self._iter_repositories():
            self._call_hook(repository, "close")

    @staticmethod
    def _call_hook(repository: Any, hook_name: str) -> None:
        """
        Ejecuta un hook opcional sobre un repository.

        Parameters
        ----------
        repository : Any
            Repository objetivo.

        hook_name : str
            Nombre del hook a ejecutar.
        """
        if repository is None:
            return

        hook = getattr(repository, hook_name, None)

        if callable(hook):
            hook()
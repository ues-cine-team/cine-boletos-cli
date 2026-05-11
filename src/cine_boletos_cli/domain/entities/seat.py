"""
Este archivo define la entidad Seat.

¿Por qué existe?
Porque el asiento es una pieza central del sistema de boletos. No debe ser
solo un dato suelto; debe saber en qué estado está, cuándo puede bloquearse,
cuándo puede liberarse y cuándo ya fue comprado.

¿Cómo se usará en el futuro?
- `booking_service.py` usará Seat para bloquear, confirmar o liberar asientos.
- `seat_lock_manager.py` ayudará a proteger el bloqueo temporal.
- `lock_expiry_worker.py` liberará locks vencidos.
- `seat_repository.py` guardará y recuperará el estado del asiento.

Qué debe resolver esta entidad:
- representar un asiento de una función,
- mantener su estado actual,
- impedir transiciones inválidas,
- permitir bloqueo temporal,
- permitir liberación,
- permitir confirmación de compra.

Reglas básicas esperadas:
- AVAILABLE: el asiento está libre.
- LOCKED: el asiento está apartado temporalmente.
- BOOKED: el asiento ya fue comprado.

Flujo normal esperado:
1. El asiento inicia como AVAILABLE.
2. El sistema lo bloquea temporalmente cuando alguien empieza a comprar.
3. Si el pago sale bien, el asiento pasa a BOOKED.
4. Si la compra falla o el tiempo vence, el asiento vuelve a AVAILABLE.

Importante:
Esta clase NO debe encargarse de base de datos, CLI, pagos ni workers.
Solo debe contener la lógica del asiento como parte del dominio.
"""


class Seat:
    """
    Entidad de dominio que representa un asiento de cine dentro de una función.
    """

    def __init__(
        self,
        seat_id,
        showtime_id,
        status,
        lock_id=None,
        locked_until=None,
    ):
        """
        Crea un asiento con su identidad y estado actual.

        Args:
            seat_id:
                Identificador formal del asiento. Idealmente un Value Object.

            showtime_id:
                Identificador de la función a la que pertenece este asiento.

            status:
                Estado actual del asiento. Debe usar los valores oficiales
                definidos en shared/constants.py.

            lock_id:
                Identificador del bloqueo temporal, si existe.

            locked_until:
                Fecha y hora hasta la que el lock sigue siendo válido.
        """
        self.seat_id = seat_id
        self.showtime_id = showtime_id
        self.status = status
        self.lock_id = lock_id
        self.locked_until = locked_until

    def is_available(self):
        """
        Indica si el asiento puede reservarse o comprarse.

        Debe devolver True solo cuando el asiento esté libre y no tenga un
        bloqueo activo.
        """
        pass

    def lock(self, lock_id, locked_until):
        """
        Bloquea temporalmente el asiento.

        Debe:
        - validar que el asiento esté disponible,
        - guardar lock_id,
        - guardar locked_until,
        - cambiar el estado a LOCKED.

        Si el asiento ya está ocupado o bloqueado, debe rechazar la operación.
        """
        pass

    def unlock(self):
        """
        Libera el asiento cuando el lock venció o la compra falló.

        Debe:
        - limpiar lock_id,
        - limpiar locked_until,
        - devolver el estado a AVAILABLE si corresponde.

        No debería permitir liberar un asiento ya comprado sin una regla clara.
        """
        pass

    def book(self):
        """
        Marca el asiento como comprado.

        Debe:
        - validar que el estado actual permita compra,
        - cambiar el estado a BOOKED,
        - dejar el asiento cerrado para futuras reservas.

        Si el asiento no estaba bloqueado correctamente, debe lanzar el error
        de dominio correspondiente.
        """
        pass

    def validate_transition(self, new_status):
        """
        Valida si el cambio de estado solicitado es permitido.

        Ejemplos de transiciones esperadas:
        - AVAILABLE -> LOCKED
        - LOCKED -> BOOKED
        - LOCKED -> AVAILABLE

        Cualquier transición fuera de esas reglas debe rechazarse.
        """
        pass
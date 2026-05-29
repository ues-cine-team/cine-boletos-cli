"""
IdempotencyService
Este módulo evita que una misma operación crítica se ejecute varias veces.
¿Por qué existe?
----------------
En sistemas reales pueden ocurrir situaciones como:
- el usuario presiona "pagar" varias veces,
- la red falla y el cliente reintenta,
- el frontend reenvía la misma request,
- el backend recibe duplicados,
- un timeout genera reintentos automáticos.
SIN idempotencia:
-----------------
el sistema podría:
- cobrar dos veces,
- crear dos bookings,
- vender el mismo asiento varias veces,
- generar estados inconsistentes.
La idempotencia garantiza:
--------------------------
"La misma operación con la misma clave produce el mismo resultado."
Ejemplo conceptual
------------------
El cliente envía:
    idempotency_key = "payment-abc-123"
Primera vez:
- se procesa normalmente,
- se guarda el resultado.
Segunda vez con la misma key:
- NO se vuelve a ejecutar,
- se devuelve el resultado ya existente.
¿Cómo se relaciona con el sistema?
----------------------------------
Este módulo será usado principalmente por:
- booking_service.py
- payment_service.py
- purchase_tickets.py
Y trabajará junto con:
- UnitOfWork
- repositories
- locking
Flujo real simplificado
-----------------------
1. llega request de compra
2. se revisa idempotency key
3. si ya existe:
       devolver resultado anterior
4. si no existe:
       ejecutar operación
       guardar resultado
       marcar como completada
Importante
-----------
Este módulo NO procesa pagos.
NO crea bookings.
NO bloquea asientos.
Solo coordina protección contra duplicados.
"""
 
 
class IdempotencyService:
    """
    Servicio encargado de gestionar operaciones idempotentes.
    Usa un diccionario en memoria para almacenar las keys y sus resultados.
    """
 
    def __init__(self):
        # Diccionario que guarda: key -> resultado
        self._store = {}
 
    def exists(self, key):
        """
        Verifica si una idempotency key ya fue registrada.
 
        Parameters
        ----------
        key : str
            Clave única de idempotencia.
 
        Returns
        -------
        bool
            True si la operación ya fue procesada.
        """
        return key in self._store
 
    def register(self, key, result):
        """
        Registra una operación completada junto con su resultado.
 
        Parameters
        ----------
        key : str
            Clave única de idempotencia.
        result : Any
            Resultado final de la operación.
 
        Notes
        -----
        Más adelante esto podría persistirse en:
        - Redis
        - PostgreSQL
        - cache distribuido
        """
        self._store[key] = result
 
    def get_result(self, key):
        """
        Recupera el resultado asociado a una idempotency key.
 
        Parameters
        ----------
        key : str
            Clave de idempotencia.
 
        Returns
        -------
        Any
            Resultado previamente almacenado, o None si no existe.
        """
        return self._store.get(key, None)
 
    def clear(self, key):
        """
        Elimina una idempotency key registrada.
 
        Esto puede ser útil para:
        - limpieza,
        - expiración,
        - mantenimiento.
        """
        if key in self._store:
            del self._store[key]
 
 
"""
Ejemplo de uso futuro
---------------------
    if idempotency_service.exists(idempotency_key):
        return idempotency_service.get_result(idempotency_key)
    result = booking_service.purchase_tickets(...)
    idempotency_service.register(
        idempotency_key,
        result,
    )
    return result
Problema que evita
------------------
SIN idempotencia:
    Usuario hace doble click en "Pagar"
    → se crean 2 bookings
    → se cobran 2 veces
CON idempotencia:
    Segundo request detecta misma key
    → devuelve resultado anterior
    → NO duplica operación
"""

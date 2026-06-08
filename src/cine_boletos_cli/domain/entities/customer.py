from datetime import datetime
from enum import Enum
from typing import Optional


class CustomerStatus(Enum):
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"


class Customer:
    """
    Entidad del dominio que representa a un cliente del cine.
    """

    def __init__(
        self,
        customer_id: str,
        name: str,
        email: str,
        status: CustomerStatus,
        created_at: datetime,
        updated_at: Optional[datetime] = None,
    ):
        """
        Inicializa un cliente con sus datos principales de dominio.
        """
        self.customer_id = customer_id
        self.name = name
        self._email = email  # Usamos una propiedad protegida para validar el email
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at or created_at

        # Ejecutamos validaciones iniciales de consistencia
        self._validate_initial_state()

    @property
    def email(self) -> str:
        return self._email

    def _validate_initial_state(self):
        """Valida que los datos obligatorios no estén vacíos."""
        if not self.customer_id:
            raise ValueError("El customer_id no puede estar vacío.")
        if not self.name or not self.name.strip():
            raise ValueError("El nombre del cliente no puede estar vacío.")
        self._validate_email_format(self._email)

    def _validate_email_format(self, email: str):
        """Validación básica de estructura de email en el dominio."""
        if "@" not in email or "." not in email:
            raise ValueError(f"El formato del correo electrónico '{email}' es inválido.")

    def change_contact_info(self, new_name: str, new_email: str):
        """
        Permite al cliente actualizar sus datos de contacto.
        Valida que el cliente esté activo antes de realizar cambios.
        """
        if self.status == CustomerStatus.SUSPENDED:
            raise ValueError("No se pueden actualizar los datos de un cliente suspendido.")

        self._validate_email_format(new_email)
        
        if not new_name or not new_name.strip():
            raise ValueError("El nuevo nombre no puede estar vacío.")

        self.name = new_name
        self._email = new_email
        self.updated_at = datetime.now()

    def suspend(self, reason: str):
        """
        Suspende la cuenta del cliente (ej. por comportamiento indebido).
        """
        if self.status == CustomerStatus.SUSPENDED:
            return  # Idempotencia: si ya está suspendido, no hace nada.
        
        if not reason or not reason.strip():
            raise ValueError("Se debe proporcionar una razón para suspender al cliente.")

        self.status = CustomerStatus.SUSPENDED
        self.updated_at = datetime.now()

    def activate(self):
        """
        Reactiva la cuenta del cliente.
        """
        if self.status == CustomerStatus.ACTIVE:
            return

        self.status = CustomerStatus.ACTIVE
        self.updated_at = datetime.now()
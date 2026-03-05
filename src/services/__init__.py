"""
Módulo de servicios para la aplicación.

¿QUÉ ES UN PAQUETE DE SERVICIOS?
- Subpaquete que contiene la "lógica de negocios" (CRUD, persistencia, etc).
- Services son la "capa intermedia" en arquitectura.
- Manejan operaciones que van más allá de un solo modelo.

¿SEPARACIÓN DE CAPAS?
- Models (src.models): Representan datos, validan estructura.
- Services (src.services): Manejan colecciones, persistencia, reglas de negocio.
- UI/CLI (src.main): Presentación e interacción con usuario.

VENTAJAS:
- Mantenimiento: Cambios en persistencia no afectan UI.
- Testabilidad: Puedo mockear ClienteService en tests de main.
- Reutilización: Otro frontend (web, mobile) puede usar mismo servicio.

¿PATRÓN REPOSITORY?
- ClienteService es un "repository" (almacén de datos).
- Abstrae DÓNDE están los datos (JSON hoy, SQL mañana).
"""

# Importar servicio principal
from .cliente_service import ClienteService

# Definir API pública
__all__ = ["ClienteService"]

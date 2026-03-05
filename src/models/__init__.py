"""
Módulo de modelos de datos para la aplicación.

¿QUÉ ES UN PAQUETE DE MODELOS?
- Subpaquete que contiene todas las entidades del dominio (Cliente, etc).
- Models son la "capa de datos" en arquitectura.

¿ESTRUCTURA?
src/models/
  __init__.py        ← Este archivo
  base.py            ← Clase abstracta EntidadBase
  cliente.py         ← Clase Cliente

¿POR QUÉ IMPORTAR Y EXPORTAR EN __INIT__.PY?
- CONVENIENCIA: Usuario puede hacer:
  from src.models import Cliente      ← en lugar de:
                                         from src.models.cliente import Cliente

- PUBLIC API: Define qué es "público" en el paquete.
  - Si importamos en __init__.py → es público.
  - Si no importamos → es privado/interno.

¿__ALL__?
- Lista de nombres que se exportan con "from src.models import *".
- Buena práctica: Siempre especificar __all__ explícitamente.
- Previene accidentes (importar cosas que no quisiste exponer).
"""

# Importar clases principales desde sus módulos
# Esto hace que estén disponibles en el nivel del paquete
from .base import EntidadBase      # Clase abstracta
from .cliente import Cliente        # Clase concreta

# Definir API pública del paquete
# "Si alguien hace 'from src.models import *', obtendrá estos"
__all__ = ["EntidadBase", "Cliente"]

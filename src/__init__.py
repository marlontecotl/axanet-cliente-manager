"""
Módulo principal de la aplicación de gestión de clientes AXANET.

¿QUÉ ES __INIT__.PY?
- Archivo especial de Python que hace un directorio una "PAQUETE".
- Sin __init__.py, Python no reconoce el directorio como paquete.
- Con __init__.py, puedes importar módulos desde el paquete.

¿POR QUÉ IMPORTA?
- Desde fuera: from src.models.cliente import Cliente (necesita src/__init__.py)
- Sin __init__.py: Python piensa que src/ es solo un directorio, no un paquete.
- Python necesita saber que puede buscar módulos dentro de este directorio.

ESTRUCTURA CON __INIT__.PY:
src/
  __init__.py          ← Hace que src/ sea un paquete
  models/
    __init__.py        ← Hace que models/ sea un subpaquete
    cliente.py
    base.py
  services/
    __init__.py        ← Hace que services/ sea un subpaquete
    cliente_service.py
  validators/
    __init__.py        ← Hace que validators/ sea un subpaquete
    validators.py

VENTAJAS DE PAQUETES:
- Organización: Código agrpuado por responsabilidad.
- Reutilización: Otros proyectos pueden importar desde src.
- Namespace: Evita conflictos de nombres (Cliente en dos paquetes = OK).

VARIABLES A NIVEL DE PAQUETE:
- __version__: Versión del paquete (importante en DevOps/producción).
- __author__: Quién desarrolló el código.
- __all__: (opcional) Qué exporta este paquete cuando alguien hace from src import *.
"""

# Versión del paquete (importante para:
# - CI/CD pipelines (saber qué versión se está deployando)
# - Compatibilidad (si una API cambia, incrementar versión)
# - Releases (PyPI, Docker images, etc. necesitan versiones)
__version__ = "1.0.0"

# Autor del código (para documentación y responsabilidad)
__author__ = "Estudiante DevOps"

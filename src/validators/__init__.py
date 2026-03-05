"""
Módulo de validadores para la aplicación.

¿QUÉ ES UN PAQUETE DE VALIDADORES?
- Subpaquete que contiene funciones de validación.
- Validadores son la "capa de entrada" (verifican datos antes de procesarlos).
- Reutilizable: Usados por Models, Services, y UI.

¿VALIDACIÓN EN CAPAS?
- Nivel 1 (Modelo): Validar FORMATO de datos individuales (RFC es 12-13 chars).
- Nivel 2 (Servicio): Validar REGLAS DE NEGOCIO (RFC único en la colección).
- Nivel 3 (UI): Validar INPUT DEL USUARIO (mostrar errores antes de crear Model).

¿CENTRALIZACIÓN?
- Todas las funciones de validación en UN lugar (src/validators/validators.py).
- Si regla de RFC cambia, cambias en UN lugar (no 10 places).
- MANTENIMIENTO: Más fácil, menos bugs.

¿COMPILACIÓN REGEX A NIVEL DE MÓDULO?
- Patrones se compilan UNA VEZ cuando importas.
- Luego reutilizados en cada llamada a validar_*().
- PERFORMANCE: Regex compilado es 1000x más rápido que compilar cada vez.
- BUENA PRÁCTICA DEVOPS: Optimización sin sacrificar legibilidad.
"""

# Importar todas las funciones validadoras
from .validators import (
    validar_nombre,        # Valida nombres (3+ chars, sin números)
    validar_rfc,          # Valida RFC mexicano (12-13 chars)
    validar_email,        # Valida email (formato estándar)
    validar_telefono,     # Valida teléfono (10+ dígitos)
    validar_estado        # Valida estado (activo/inactivo)
)

# Definir API pública del paquete
__all__ = ["validar_nombre", "validar_rfc", "validar_email",
           "validar_telefono", "validar_estado"]

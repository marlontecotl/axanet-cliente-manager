"""
Módulo de validadores para RFC y email.
Validaciones simples con regex.
"""

import re


def validar_rfc(rfc):
    """
    Valida que el RFC tenga el formato correcto.
    Formato: 4 letras + 6 dígitos + 3 caracteres alfanuméricos
    Ejemplo: ABCD123456XYZ
    """
    patron = r'^[A-Z]{4}\d{6}[A-Z0-9]{3}$'
    return bool(re.match(patron, rfc.upper()))


def validar_email(email):
    """
    Valida que el email tenga un formato válido.
    Validación simple con regex.
    """
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(patron, email))

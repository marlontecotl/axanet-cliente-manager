"""
Módulo de funciones validadoras.

Este módulo contiene funciones para validar diferentes tipos de datos
como nombres, RFC, emails, teléfonos y estados.

CONCEPTOS:
- REGEX (Expresiones Regulares): Patrones para validar formato de strings.
- COMPILACIÓN A NIVEL DE MÓDULO: Los patrones se compilan UNA VEZ cuando se importa.
- TYPE HINTS: Pattern[str] indica que es un patrón compilado de regex.
"""

import re
from typing import Pattern


# ============================================================================
# PATRONES REGEX COMPILADOS A NIVEL DE MÓDULO
# ============================================================================
# ¿POR QUÉ COMPILAR EN MÓDULO?
# - re.compile() procesa el regex y lo optimiza (parsing, DFA).
# - Hacerlo UNA VEZ es mucho más rápido que hacerlo en cada llamada.
# - Si validar_email() se llama 1000 veces, re.compile() se evita 999 veces.
# - BUENA PRÁCTICA DEVOPS: Optimización de rendimiento (menos CPU, más rápido).
#
# ¿CÓMO FUNCIONA?
# - re.compile() retorna un objeto Pattern compilado.
# - Luego se usa .match() o .search() para comparar strings contra el patrón.
# ============================================================================

# PATRÓN RFC (Registro Federal de Contribuyentes - México)
# Formato: 3-4 letras + 6 dígitos + 0-3 caracteres (letras/números)
# Ejemplo: ABC123456XYZ (13 chars) o ABC123456XY0 (12 chars)
# Explicación del regex:
#   ^              : Inicio de string
#   [A-ZÑ&]{3,4}   : 3-4 caracteres mayúsculas (incluye Ñ para México)
#   \d{6}          : Exactamente 6 dígitos (0-9)
#   [A-Z0-9]{0,3}  : 0 a 3 caracteres alfanuméricos (verificador, opcional)
#   $              : Final de string
PATRON_RFC: Pattern = re.compile(r'^[A-ZÑ&]{3,4}\d{6}[A-Z0-9]{0,3}$')

# PATRÓN EMAIL (Correo electrónico estándar)
# Formato: usuario@dominio.extension
# Ejemplo: juan.garcia@empresa.co.mx
# Explicación del regex:
#   ^                        : Inicio de string
#   [a-zA-Z0-9._%+-]+        : 1+ caracteres válidos en "usuario"
#                              (permite puntos, guiones, símbolos comunes)
#   @                        : Símbolo arroba (obligatorio)
#   [a-zA-Z0-9.-]+           : 1+ caracteres para "dominio"
#   \.                       : Punto literal (escapado porque . es especial en regex)
#   [a-zA-Z]{2,}             : 2+ letras para "extensión" (.com, .co, .mx, .info)
#   $                        : Final de string
# NOTA: Este patrón es SIMPLE. Un email válido según RFC 5322 es mucho más complejo.
#       Pero para propósitos de negocio, este es suficiente.
PATRON_EMAIL: Pattern = re.compile(
    r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
)

# PATRÓN TELÉFONO (Formatos flexibles de número telefónico)
# Ejemplo válidos: "5551234567", "555-123-4567", "(555) 123-4567", "+52 555 1234567"
# Explicación del regex:
#   ^                : Inicio de string
#   [0-9\-\+\s\()]  : Caracteres permitidos:
#                      0-9: Dígitos
#                      \-: Guión (escapado porque - es especial en [])
#                      \+: Signo más para código de país (escapado)
#                      \s: Espacios en blanco
#                      \(): Paréntesis para formato (555) 123-4567
#   {10,20}         : Longitud: 10-20 caracteres (validamos dígitos por separado)
#   $               : Final de string
# NOTA: Validamos longitud de caracteres aquí, pero dígitos por separado en la función.
PATRON_TELEFONO: Pattern = re.compile(r'^[0-9\-\+\s\(\)]{10,20}$')


def validar_nombre(nombre: str) -> bool:
    """
    Valida que el nombre sea válido.

    ¿REGLAS DE VALIDACIÓN?
    1. Debe ser string (no None, no int, etc).
    2. Debe tener 3+ caracteres (después de strip).
    3. NO puede contener números (Juan123 es inválido).
    4. Debe contener solo letras, espacios, guiones, puntos (y acentos para español).

    ¿GUARD CLAUSES?
    - Primero verificamos tipo (isinstance).
    - Si falla, retornamos False inmediatamente.
    - Esto es más eficiente que if-else anidados profundos.
    - Patrón: Verificar condiciones de error PRIMERO.

    ¿STACK DE VALIDACIONES?
    - Si cada validación falla, retornamos False.
    - Permiten debuggear: ¿qué exactamente falló?
    - En producción, podrías retornar (bool, str) con mensaje de error.

    Args:
        nombre (str): Nombre a validar.

    Returns:
        bool: True si el nombre es válido, False en caso contrario.

    Ejemplo:
        validar_nombre("Juan García")      # True
        validar_nombre("Jo")                # False (muy corto)
        validar_nombre("Juan123")           # False (contiene números)
        validar_nombre("José María López")  # True (acentos OK)
        validar_nombre(None)                # False (no es string)
    """
    # GUARD CLAUSE 1: Verificar tipo
    # Si no es string, retornar False inmediatamente
    if not isinstance(nombre, str):
        return False

    # Eliminar espacios al inicio y final
    # Esto permite "  Juan  " → "Juan" (válido)
    nombre = nombre.strip()

    # GUARD CLAUSE 2: Verificar longitud mínima
    # Nombres muy cortos ("Jo", "Ma") son inválidos para personas reales
    if len(nombre) < 3:
        return False

    # GUARD CLAUSE 3: Verificar que NO contiene números
    # Método: any() retorna True si ALGÚN carácter es dígito
    # Ejemplo: any(char.isdigit() for char in "Juan123") → True
    if any(char.isdigit() for char in nombre):
        return False

    # VALIDACIÓN FINAL: Verificar formato con regex
    # Permitir: letras latinas, acentos españoles, espacios, guiones, puntos
    # Explicación del regex:
    #   [a-zA-ZáéíóúÁÉÍÓÚñÑ\s\-\.]
    #   a-z: minúsculas
    #   A-Z: mayúsculas
    #   áéíóúÁÉÍÓÚ: acentos (tildas)
    #   ñÑ: letra ñ (México)
    #   \s: espacios en blanco
    #   \-: guión (escapado porque - es especial en [])
    #   \.: punto (escapado porque . es especial en regex)
    if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s\-\.]+$', nombre):
        return False

    return True


def validar_rfc(rfc: str) -> bool:
    """
    Valida que el RFC sea válido (formato mexicano).

    ¿QUÉ ES RFC?
    - Registro Federal de Contribuyentes (México).
    - Identificador fiscal único, como un "SSN" en EE.UU.
    - Asignado por autoridades fiscales mexicanas.

    ¿FORMATO?
    - 12 caracteres: RFC sin homoclave (viejo, raro).
    - 13 caracteres: RFC con homoclave (estándar actual).
    - Estructura: 3-4 letras + 6 dígitos + 0-3 caracteres verificadores.

    ¿EJEMPLOS?
    - ABC123456XYZ (13 chars - estándar)
    - ABC123456XY0 (13 chars - con homoclave)
    - ABC123456AB (12 chars - sin homoclave)

    ¿VALIDACIÓN?
    1. Verificar tipo (string).
    2. Convertir a mayúsculas (RFC es insensible a caso).
    3. Aplicar PATRON_RFC compilado.
    4. Verificar longitud es 12 o 13.

    Args:
        rfc (str): RFC a validar.

    Returns:
        bool: True si el RFC es válido, False en caso contrario.

    Ejemplo:
        validar_rfc("ABC123456XYZ")  # True
        validar_rfc("abc123456xyz")  # True (se convierte a mayúscula)
        validar_rfc("ABC12345")      # False (muy corto)
        validar_rfc("ABC-123-456-XYZ")  # False (contiene guiones inválidos)
    """
    # GUARD CLAUSE: Verificar tipo
    if not isinstance(rfc, str):
        return False

    # Normalizar: strip() elimina espacios, upper() convierte a mayúsculas
    # RFC es case-insensitive: "abc123456xyz" = "ABC123456XYZ"
    rfc = rfc.strip().upper()

    # Validar contra patrón compilado
    # PATRON_RFC ya está compilado a nivel de módulo (performance)
    if not PATRON_RFC.match(rfc):
        return False

    # Verificar longitud exacta: RFC tiene 12 o 13 caracteres
    # El patrón valida estructura, pero la longitud es crítica
    if len(rfc) not in [12, 13]:
        return False

    return True


def validar_email(email: str) -> bool:
    """
    Valida que el email sea válido (formato básico).

    ¿LIMITACIÓN?
    - Email válido según RFC 5322 es MUY complejo (regex de 6KB+).
    - Usamos regex SIMPLE que cubre 99% de casos reales.
    - Si necesitas validación estricta RFC 5322, usa biblioteca `email-validator`.

    ¿REGLAS?
    1. Debe ser string.
    2. Debe contener exactamente 1 @ (separador usuario-dominio).
    3. Debe contener 1+ punto (.) en el dominio (extensión).
    4. Máximo 254 caracteres (estándar RFC 5321).
    5. Formato: usuario@dominio.extensión.

    ¿EJEMPLOS VÁLIDOS?
    - usuario@ejemplo.com
    - juan.garcia@empresa.co.mx
    - info+soporte@dominio.org

    ¿EJEMPLOS INVÁLIDOS?
    - usuarioejemplo.com (no tiene @)
    - usuario@ejemplo (no tiene extensión)
    - usuario@@ejemplo.com (dos @)
    - usuario@.com (no tiene dominio)

    Args:
        email (str): Email a validar.

    Returns:
        bool: True si el email es válido, False en caso contrario.

    Ejemplo:
        validar_email("juan@ejemplo.com")  # True
        validar_email("JUAN@EJEMPLO.COM")  # True (se normaliza a minúscula)
        validar_email("juan@ejemplo")      # False (falta extensión)
        validar_email("juanAejemplo.com")  # False (falta @)
    """
    # GUARD CLAUSE: Verificar tipo
    if not isinstance(email, str):
        return False

    # Normalizar: strip() elimina espacios, lower() convierte a minúsculas
    # Email es case-insensitive: "Juan@Ejemplo.com" = "juan@ejemplo.com"
    email = email.strip().lower()

    # Verificar longitud máxima (RFC 5321)
    # La mayoría de servidores de email soportan 254 caracteres máximo
    # Previene abuso (listas muy largas de direcciones, etc)
    if len(email) > 254:
        return False

    # Validar contra patrón compilado
    # PATRON_EMAIL ya está compilado a nivel de módulo
    if not PATRON_EMAIL.match(email):
        return False

    return True


def validar_telefono(telefono: str) -> bool:
    """
    Valida que el teléfono sea válido.

    ¿FLEXIBILIDAD?
    - Acepta múltiples formatos: "5551234567", "555-123-4567", "(555) 123-4567", "+52 555 1234567"
    - Esto es importante porque usuarios escriben teléfonos de diferentes maneras.
    - Validación es sobre CANTIDAD de dígitos, no formato exacto.

    ¿REGLAS?
    1. Debe ser string.
    2. Debe contener 10+ dígitos (teléfono mexicano estándar).
    3. Puede contener caracteres de formato: -, +, (), espacios.
    4. Longitud total (con formato): 10-20 caracteres.

    ¿EJEMPLOS VÁLIDOS?
    - 5551234567 (10 dígitos sin formato)
    - 555-123-4567 (con guiones)
    - (555) 123-4567 (con paréntesis)
    - +52 555 1234567 (con código de país)
    - +52 (55) 1234-5678 (formato mixto)

    ¿EJEMPLOS INVÁLIDOS?
    - 555123 (solo 6 dígitos)
    - ABC1234567 (contiene letras)
    - (555) 123 (incompleto)

    ¿POR QUÉ VALIDAR DÍGITOS POR SEPARADO?
    - Usuario podría escribir "(555) 123-4567" (12 chars, pero 10 dígitos).
    - Si validamos solo longitud total, rechazaríamos formatos válidos.
    - Mejor: Contar DÍGITOS por separado, validar eso.

    Args:
        telefono (str): Teléfono a validar.

    Returns:
        bool: True si el teléfono es válido, False en caso contrario.

    Ejemplo:
        validar_telefono("5551234567")          # True
        validar_telefono("555-123-4567")        # True
        validar_telefono("(555) 123-4567")      # True
        validar_telefono("+52 555 1234567")     # True
        validar_telefono("555123")              # False (muy pocos dígitos)
        validar_telefono(5551234567)            # False (no es string)
    """
    # GUARD CLAUSE: Verificar tipo
    if not isinstance(telefono, str):
        return False

    # Eliminar espacios al inicio y final
    telefono = telefono.strip()

    # Extraer SOLO los dígitos del teléfono
    # Esto permite validar la cantidad de dígitos sin importar formato
    # Ejemplo: "(555) 123-4567" → digitos = "5551234567" (10 dígitos)
    digitos = ''.join(char for char in telefono if char.isdigit())

    # Verificar que hay al menos 10 dígitos (teléfono mexicano mínimo)
    # México usa: 10 dígitos (área: 2-3, número: 7-8)
    if len(digitos) < 10:
        return False

    # Validar contra patrón compilado
    # PATRON_TELEFONO verifica caracteres permitidos y longitud total
    if not PATRON_TELEFONO.match(telefono):
        return False

    return True


def validar_estado(estado: str) -> bool:
    """
    Valida que el estado sea uno de los valores permitidos.

    ¿ENUMERACIÓN?
    - Estado es una "enumeración": conjunto finito de valores válidos.
    - Similar a enum en otros lenguajes (Enum en Python).
    - Aquí usamos lista simple para didáctica.

    ¿VALORES PERMITIDOS?
    - "activo": Cliente activo, puede hacer transacciones.
    - "inactivo": Cliente desactivado, históricamente válido pero no activo.

    ¿CASE-INSENSITIVE?
    - Usuario podría escribir "ACTIVO", "Activo", "activo".
    - Normalizamos a minúscula y validamos.
    - Permite flexibilidad sin comprometer validación.

    ¿VENTAJA SOBRE ENUM?
    - List es más simple para aprender.
    - Enum en Python es más robusto para producción.
    - En futuro, si necesitas más estados, puedes usar Enum.

    Args:
        estado (str): Estado a validar.

    Returns:
        bool: True si el estado es uno de los válidos, False en caso contrario.

    Ejemplo:
        validar_estado("activo")     # True
        validar_estado("INACTIVO")   # True (se normaliza)
        validar_estado("AcTiVo")     # True (case-insensitive)
        validar_estado("pendiente")  # False (no es válido)
        validar_estado("activ")      # False (incompleto)
        validar_estado(123)          # False (no es string)
    """
    # GUARD CLAUSE: Verificar tipo
    if not isinstance(estado, str):
        return False

    # Normalizar: strip() elimina espacios, lower() convierte a minúsculas
    estado = estado.strip().lower()

    # Definir estados válidos
    # Esta lista define el "contrato" de qué estados son permitidos
    # Si necesitas agregar "suspendido", lo haces aquí
    estados_validos = ["activo", "inactivo"]

    # Verificar si estado normalizado está en la lista de válidos
    # in operador: búsqueda O(n) en lista, O(1) en set/dict si fuera más grande
    return estado in estados_validos

"""
Pruebas unitarias para el módulo de validadores.

Este módulo contiene las pruebas para verificar que los validadores
funcionan correctamente con casos válidos e inválidos.

ESTRATEGIA DE TESTING:
- CASOS VÁLIDOS: Input correcto → Retorna True.
- CASOS INVÁLIDOS: Input incorrecto → Retorna False.
- EDGE CASES: Límites, caracteres especiales, tipos equivocados.
- INTERNACIONALIZACIÓN: Caracteres acentuados, ñ, etc.

¿POR QUÉ TESTEAR VALIDADORES EXHAUSTIVAMENTE?
- Validadores son la "puerta" de entrada del sistema.
- Datos inválidos que pasen → Corrupción de datos en el futuro.
- Mejor rechazar temprano (FAIL-FAST).
"""

from src.validators.validators import (
    validar_nombre, validar_rfc, validar_email,
    validar_telefono, validar_estado
)


class TestValidarNombre:
    """
    Pruebas para la función validar_nombre.

    CASOS CUBIERTOS:
    - Nombre válido (3+ chars, letras y espacios).
    - Nombre con tildes/acentos (mexicanos: José, María).
    - Nombre muy corto (< 3 chars).
    - Nombre con números (inválido).
    - Nombre vacío.
    - Tipo no-string.
    """

    def test_nombre_valido(self):
        """Prueba con un nombre válido (caso normal)."""
        assert validar_nombre("Juan García") is True

    def test_nombre_con_tildes(self):
        """
        Prueba con un nombre que contiene tildes.

        ¿POR QUÉ IMPORTANTE?
        - INTERNACIONALIZACIÓN: México tiene nombres con acentos.
        - Sin este test, validador podría rechazar "José" (válido en español).
        - Confirma que regex incluye caracteres españoles.
        """
        assert validar_nombre("José María López") is True

    def test_nombre_muy_corto(self):
        """Prueba con un nombre muy corto (boundary case)."""
        assert validar_nombre("Jo") is False

    def test_nombre_con_numeros(self):
        """Prueba con un nombre que contiene números (inválido)."""
        assert validar_nombre("Juan123") is False

    def test_nombre_vacio(self):
        """Prueba con un nombre vacío (edge case)."""
        assert validar_nombre("") is False

    def test_nombre_no_string(self):
        """Prueba con un nombre que no es string (type safety)."""
        assert validar_nombre(123) is False


class TestValidarRFC:
    """
    Pruebas para la función validar_rfc.

    RFC (Registro Federal de Contribuyentes) mexicano:
    - Identificador fiscal único (como SSN en EE.UU.).
    - Formato: 3-4 letras + 6 dígitos + 0-3 alfanuméricos.
    - Emitido por autoridades mexicanas (SAT).

    CASOS CUBIERTOS:
    - RFC de 13 caracteres (estándar con homoclave).
    - RFC de 12 caracteres (sin homoclave, viejo).
    - Case-insensitive (mayúscula/minúscula).
    - Boundary cases: muy corto, con espacios.
    - Type safety: no-string.
    """

    def test_rfc_valido(self):
        """Prueba con un RFC válido (13 chars con homoclave)."""
        assert validar_rfc("ABC123456XYZ") is True

    def test_rfc_valido_sin_verificador(self):
        """Prueba con un RFC válido de 12 caracteres (sin homoclave)."""
        assert validar_rfc("ABC123456XY0") is True

    def test_rfc_minusculas(self):
        """Prueba con RFC en minúsculas (case-insensitive)."""
        assert validar_rfc("abc123456xyz") is True

    def test_rfc_muy_corto(self):
        """Prueba con RFC muy corto (boundary case)."""
        assert validar_rfc("ABC12345") is False

    def test_rfc_con_espacios(self):
        """Prueba con RFC que tiene espacios (inválido)."""
        assert validar_rfc("ABC 123 456 XYZ") is False

    def test_rfc_no_string(self):
        """Prueba con RFC que no es string (type safety)."""
        assert validar_rfc(123456) is False


class TestValidarEmail:
    """Pruebas para la función validar_email."""

    def test_email_valido(self):
        """Prueba con un email válido."""
        assert validar_email("usuario@ejemplo.com") is True

    def test_email_con_puntos(self):
        """Prueba con email que contiene puntos."""
        assert validar_email("usuario.nombre@ejemplo.co.mx") is True

    def test_email_sin_arroba(self):
        """Prueba con email sin arroba."""
        assert validar_email("usuarioejemplo.com") is False

    def test_email_sin_dominio(self):
        """Prueba con email sin dominio completo."""
        assert validar_email("usuario@ejemplo") is False

    def test_email_vacio(self):
        """Prueba con email vacío."""
        assert validar_email("") is False

    def test_email_no_string(self):
        """Prueba con email que no es string."""
        assert validar_email(12345) is False


class TestValidarTelefono:
    """Pruebas para la función validar_telefono."""

    def test_telefono_valido(self):
        """Prueba con un teléfono válido."""
        assert validar_telefono("5551234567") is True

    def test_telefono_con_guiones(self):
        """Prueba con teléfono con guiones."""
        assert validar_telefono("555-123-4567") is True

    def test_telefono_con_parentesis(self):
        """Prueba con teléfono con paréntesis."""
        assert validar_telefono("(555) 123-4567") is True

    def test_telefono_con_codigo_pais(self):
        """Prueba con teléfono con código de país."""
        assert validar_telefono("+52 555 1234567") is True

    def test_telefono_muy_corto(self):
        """Prueba con teléfono muy corto."""
        assert validar_telefono("555123") is False

    def test_telefono_vacio(self):
        """Prueba con teléfono vacío."""
        assert validar_telefono("") is False

    def test_telefono_no_string(self):
        """Prueba con teléfono que no es string."""
        assert validar_telefono(5551234567) is False


class TestValidarEstado:
    """Pruebas para la función validar_estado."""

    def test_estado_activo(self):
        """Prueba con estado activo."""
        assert validar_estado("activo") is True

    def test_estado_inactivo(self):
        """Prueba con estado inactivo."""
        assert validar_estado("inactivo") is True

    def test_estado_mayusculas(self):
        """Prueba con estado en mayúsculas."""
        assert validar_estado("ACTIVO") is True

    def test_estado_mixto(self):
        """Prueba con estado en mayúsculas y minúsculas mixtas."""
        assert validar_estado("AcTiVo") is True

    def test_estado_invalido(self):
        """Prueba con estado inválido."""
        assert validar_estado("pendiente") is False

    def test_estado_vacio(self):
        """Prueba con estado vacío."""
        assert validar_estado("") is False

    def test_estado_no_string(self):
        """Prueba con estado que no es string."""
        assert validar_estado(123) is False

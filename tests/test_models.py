"""
Pruebas unitarias para el módulo de modelos.

Este módulo contiene las pruebas para verificar que los modelos
Cliente y EntidadBase funcionan correctamente.

CONCEPTOS DE TESTING:
- PRUEBAS UNITARIAS: Testear unidades pequeñas (funciones, métodos) aisladas.
- PYTEST: Framework de testing que hace las pruebas fáciles de escribir.
- COBERTURA: Idealmente, cada línea de código debería tener una prueba.
- CASOS VÁLIDOS E INVÁLIDOS: Testear tanto inputs válidos como errores.

PATRONES:
- Arrange: Preparar datos de prueba.
- Act: Ejecutar el código a testear.
- Assert: Verificar que los resultados son correctos.
"""

import pytest
from datetime import datetime
from src.models.cliente import Cliente
from src.models.base import EntidadBase


class TestCliente:
    """Pruebas para la clase Cliente."""

    def test_crear_cliente_valido(self):
        """
        Prueba crear un cliente con datos válidos.

        ¿QUÉ SE TESTEA?
        - Un Cliente se puede crear con todos los datos válidos.
        - Todos los atributos se asignan correctamente.
        - El objeto tiene un ID generado.

        PATRÓN AAA:
        - Arrange: Crear datos de prueba.
        - Act: Crear instancia de Cliente.
        - Assert: Verificar que los atributos son correctos.

        ¿DATOS VÁLIDOS?
        - Nombre: "Juan García" (3+ chars, sin números).
        - RFC: "ABC123456XYZ" (formato válido, 13 chars).
        - Email: "juan@ejemplo.com" (formato válido).
        - Teléfono: "5551234567" (10 dígitos).
        - Estado: "activo" (valor permitido).
        """
        # ARRANGE: Crear cliente con datos válidos
        cliente = Cliente(
            nombre="Juan García",
            rfc="ABC123456XYZ",
            email="juan@ejemplo.com",
            telefono="5551234567",
            estado="activo"
        )

        # ASSERT: Verificar que los atributos se asignaron correctamente
        assert cliente.nombre == "Juan García"
        assert cliente.rfc == "ABC123456XYZ"
        assert cliente.email == "juan@ejemplo.com"
        assert cliente.telefono == "5551234567"
        assert cliente.estado == "activo"
        assert cliente.id is not None  # Debe haber ID generado

    def test_cliente_con_estado_por_defecto(self):
        """Prueba que el estado por defecto es 'activo'."""
        cliente = Cliente(
            nombre="María López",
            rfc="XYZ987654ABC",
            email="maria@ejemplo.com",
            telefono="5559876543"
        )

        assert cliente.estado == "activo"

    def test_cliente_nombre_invalido(self):
        """
        Prueba que se lanza excepción con nombre inválido.

        ¿POR QUÉ ESTE TEST?
        - VALIDACIÓN FAIL-FAST: El error debe ocurrir en __init__(), no después.
        - No queremos Clientes con nombre inválido en el sistema.

        ¿PYTEST.RAISES()?
        - Verifica que se LANZA una excepción de tipo esperado.
        - Si NO se lanza, el test FALLA.
        - Si se lanza con tipo diferente, el test FALLA.

        EJEMPLO:
        - Con pytest.raises(ValueError): Esperamos ValueError.
        - Crear Cliente con nombre="Jo" (solo 2 chars, inválido).
        - __init__() llama a validar(), que lanza ValueError.
        - Test PASA porque ValueError fue lanzada como se esperaba.
        """
        # TEST: Que ValueError es lanzado cuando nombre es muy corto
        with pytest.raises(ValueError):
            Cliente(
                nombre="Jo",  # Inválido: solo 2 caracteres (mínimo 3)
                rfc="ABC123456XYZ",
                email="juan@ejemplo.com",
                telefono="5551234567"
            )

    def test_cliente_rfc_invalido(self):
        """Prueba que se lanza excepción con RFC inválido."""
        with pytest.raises(ValueError):
            Cliente(
                nombre="Juan García",
                rfc="123",
                email="juan@ejemplo.com",
                telefono="5551234567"
            )

    def test_cliente_email_invalido(self):
        """Prueba que se lanza excepción con email inválido."""
        with pytest.raises(ValueError):
            Cliente(
                nombre="Juan García",
                rfc="ABC123456XYZ",
                email="email_invalido",
                telefono="5551234567"
            )

    def test_cliente_telefono_invalido(self):
        """Prueba que se lanza excepción con teléfono inválido."""
        with pytest.raises(ValueError):
            Cliente(
                nombre="Juan García",
                rfc="ABC123456XYZ",
                email="juan@ejemplo.com",
                telefono="123"
            )

    def test_cliente_a_diccionario(self):
        """
        Prueba la conversión de cliente a diccionario (serialización).

        ¿POR QUÉ ESTE TEST?
        - ROUNDTRIP: Cliente → Diccionario → Cliente (persisten datos).
        - JSON no entiende objetos, necesita dicts.
        - Si a_diccionario() está roto, la persistencia también lo está.

        ¿QUÉ SE VERIFICA?
        - Todos los atributos están en el diccionario.
        - Fechas están incluidas (para auditoría).
        - Tipo de retorno es dict (aunque assert no lo verifica).

        PATRÓN:
        - Arrange: Crear cliente.
        - Act: Convertir a diccionario.
        - Assert: Verificar que todos los campos están presentes y correctos.
        """
        # ARRANGE: Crear cliente
        cliente = Cliente(
            nombre="Juan García",
            rfc="ABC123456XYZ",
            email="juan@ejemplo.com",
            telefono="5551234567"
        )

        # ACT: Convertir a diccionario
        diccionario = cliente.a_diccionario()

        # ASSERT: Verificar que todos los campos están en el diccionario
        assert diccionario["nombre"] == "Juan García"
        assert diccionario["rfc"] == "ABC123456XYZ"
        assert diccionario["email"] == "juan@ejemplo.com"
        assert diccionario["telefono"] == "5551234567"
        assert diccionario["estado"] == "activo"
        # Verificar que fechas están presentes (son críticas para auditoría)
        assert "fecha_creacion" in diccionario
        assert "fecha_modificacion" in diccionario

    def test_cliente_desde_diccionario(self):
        """
        Prueba la creación de cliente desde diccionario (deserialización).

        ¿FACTORY PATTERN?
        - desde_diccionario() es un "factory method" (constructor alternativo).
        - Permite crear Cliente desde dict (típicamente cargado de JSON).
        - Sin esto, tendrías que hacer: dict → atributos manuales → Cliente.

        ¿ROUNDTRIP?
        - a_diccionario() serializa Cliente a dict.
        - desde_diccionario() deserializa dict a Cliente.
        - Juntos, permiten: Cliente → JSON → dict → Cliente.

        ¿POR QUÉ IMPORTANTE EN DEVOPS?
        - Datos persisten entre ejecuciones de la aplicación.
        - Primera ejecución: crea datos en memoria.
        - Segunda ejecución: carga datos desde JSON (usa desde_diccionario()).
        """
        # ARRANGE: Crear diccionario (simulando datos de JSON)
        datos = {
            "nombre": "Juan García",
            "rfc": "ABC123456XYZ",
            "email": "juan@ejemplo.com",
            "telefono": "5551234567",
            "estado": "activo"
        }

        # ACT: Crear cliente desde diccionario
        cliente = Cliente.desde_diccionario(datos)

        # ASSERT: Verificar que los atributos se asignaron correctamente
        assert cliente.nombre == datos["nombre"]
        assert cliente.rfc == datos["rfc"]
        assert cliente.email == datos["email"]
        assert cliente.telefono == datos["telefono"]

    def test_cliente_igualdad(self):
        """Prueba la comparación de igualdad entre clientes."""
        cliente1 = Cliente(
            nombre="Juan García",
            rfc="ABC123456XYZ",
            email="juan@ejemplo.com",
            telefono="5551234567"
        )

        cliente2 = Cliente(
            nombre="Otro nombre",
            rfc="XYZ987654ABC",
            email="otro@ejemplo.com",
            telefono="5559876543"
        )

        # Asignar el mismo ID para la prueba
        cliente2.id = cliente1.id

        assert cliente1 == cliente2

    def test_cliente_fechas_creacion_modificacion(self):
        """Prueba que las fechas de creación y modificación se registran."""
        antes = datetime.now()
        cliente = Cliente(
            nombre="Juan García",
            rfc="ABC123456XYZ",
            email="juan@ejemplo.com",
            telefono="5551234567"
        )
        despues = datetime.now()

        assert antes <= cliente.fecha_creacion <= despues
        assert antes <= cliente.fecha_modificacion <= despues

    def test_cliente_actualizar_fecha_modificacion(self):
        """Prueba la actualización de fecha de modificación."""
        cliente = Cliente(
            nombre="Juan García",
            rfc="ABC123456XYZ",
            email="juan@ejemplo.com",
            telefono="5551234567"
        )

        fecha_original = cliente.fecha_modificacion

        cliente.actualizar_fecha_modificacion()

        assert cliente.fecha_modificacion >= fecha_original

    def test_cliente_str(self):
        """Prueba la representación en cadena del cliente."""
        cliente = Cliente(
            nombre="Juan García",
            rfc="ABC123456XYZ",
            email="juan@ejemplo.com",
            telefono="5551234567"
        )

        str_cliente = str(cliente)

        assert "Cliente" in str_cliente
        assert cliente.nombre in str_cliente
        assert cliente.rfc in str_cliente


class TestEntidadBase:
    """
    Pruebas para la clase abstracta EntidadBase.

    ¿POR QUÉ TESTEAR LA CLASE ABSTRACTA?
    - Verificar que ABC (Abstract Base Class) realmente funciona.
    - Verificar que métodos abstractos fuerzan implementación en subclases.
    - Verificar comportamiento heredado (ID, fechas).
    """

    def test_no_puede_instanciar_directamente(self):
        """
        Prueba que no se puede instanciar EntidadBase directamente.

        ¿POR QUÉ ES IMPORTANTE?
        - ABC debe prevenir instanciación directa.
        - Si pudieras hacer EntidadBase(), el diseño estaría roto.
        - Este test verifica que el contrato se mantiene.

        ¿CÓMO FUNCIONA?
        - Intentar instanciar EntidadBase() lanza TypeError.
        - TypeError es lo que pytest.raises(TypeError) espera.
        - Test PASA porque el error ocurrió como se esperaba.
        """
        # TEST: Intentar instanciar clase abstracta debe fallar
        with pytest.raises(TypeError):
            EntidadBase()

    def test_entidad_tiene_id_unico(self):
        """
        Prueba que cada entidad tiene un ID único.

        ¿POR QUÉ?
        - EntidadBase._contador_id genera IDs secuenciales únicos.
        - Cada instancia debe tener ID diferente.
        - Si dos instancias tienen mismo ID, habría corrupción de datos.

        ¿PATRÓN?
        - Crear dos Cliente (ambos heredan de EntidadBase).
        - Verificar que sus IDs son diferentes.
        - El contador se incrementa con cada instancia.

        NOTA:
        - Este test modifica el estado global (_contador_id).
        - En tests complejos, podrías necesitar reset entre tests (use fixtures).
        """
        # ARRANGE: Crear dos clientes
        cliente1 = Cliente(
            nombre="Juan García",
            rfc="ABC123456XYZ",
            email="juan@ejemplo.com",
            telefono="5551234567"
        )

        cliente2 = Cliente(
            nombre="María López",
            rfc="XYZ987654ABC",
            email="maria@ejemplo.com",
            telefono="5559876543"
        )

        # ASSERT: Verificar que tienen IDs diferentes
        assert cliente1.id != cliente2.id

"""
Pruebas unitarias para el módulo de servicios.

Este módulo contiene las pruebas para verificar que el servicio
ClienteService funciona correctamente en operaciones CRUD.

CONCEPTOS:
- FIXTURES PYTEST: Reutilizable setup/teardown para tests.
- AISLAMIENTO: Cada test usa su propio archivo temporal (sin contaminar otros).
- PERSISTENCIA: Testear que datos se guardan y cargan correctamente.
"""

import pytest
import os
import tempfile
from src.models.cliente import Cliente
from src.services.cliente_service import ClienteService


@pytest.fixture
def archivo_temporal():
    """
    Fixture pytest que proporciona un archivo temporal para pruebas.

    ¿POR QUÉ FIXTURE?
    - setup/teardown automático: crear y borrar archivo.
    - Reutilizable: todos los tests pueden usarla.
    - AISLAMIENTO: Cada test tiene su propio archivo (no interfieren).

    ¿CÓMO FUNCIONA?
    1. tempfile.mkstemp() crea archivo temporal (único, no colisiona).
    2. os.close(fd) cierra descriptor de archivo.
    3. yield ruta: Proporciona ruta al test.
    4. Test ejecuta... (pueden usar la ruta).
    5. Cleanup: os.remove(ruta) borra archivo después.

    ¿POR QUÉ IMPORTANTE?
    - Tests no dejan archivos "sucios" en disco.
    - Cada test es independiente (puede ejecutarse en cualquier orden).
    - DevOps: Tests pueden ejecutarse en paralelo sin conflictos.

    Yields:
        str: Ruta del archivo temporal (ej: "/tmp/test_clientes_abc123.json").
    """
    # Crear archivo temporal
    # mkstemp retorna (fd, ruta) donde fd es file descriptor
    fd, ruta = tempfile.mkstemp(suffix='.json', prefix='test_clientes_')

    # Cerrar descriptor (no necesitamos mantener abierto)
    os.close(fd)

    # YIELD: Proporcionar ruta al test
    yield ruta

    # CLEANUP: Borrar archivo después de que el test termine
    if os.path.exists(ruta):
        os.remove(ruta)


@pytest.fixture
def servicio(archivo_temporal):
    """
    Fixture pytest que proporciona una instancia de ClienteService.

    ¿COMPOSICIÓN DE FIXTURES?
    - Esta fixture DEPENDE de archivo_temporal (parámetro).
    - Pytest automáticamente inyecta archivo_temporal.
    - Encadena fixtures: archivo_temporal → servicio.

    ¿VENTAJA?
    - Cada test obtiene ClienteService con archivo temporal.
    - Datos no persisten entre tests (archivo borrado cada vez).
    - Tests son AISLADOS (no interfieren).

    Args:
        archivo_temporal: Ruta del archivo temporal (de otra fixture).

    Yields:
        ClienteService: Instancia del servicio con archivo temporal.
    """
    # Crear servicio con archivo temporal
    # Cada test obtiene su propia instancia + archivo único
    yield ClienteService(ruta_archivo=archivo_temporal)


@pytest.fixture
def cliente_ejemplo():
    """
    Fixture pytest que proporciona un cliente de ejemplo válido.

    ¿POR QUÉ?
    - Reutilizable: Muchos tests necesitan un cliente válido.
    - SIN fixture: Tendrías que crear el mismo Cliente en cada test (duplicado).
    - CON fixture: Define UNA VEZ, úsalo en todos los tests.

    ¿NO DEPENDE DE OTRAS FIXTURES?
    - No recibe parámetros, es "raíz" (no depende de nada).
    - Simple: Solo retorna un objeto Cliente.
    - CUIDADO: Cada test obtiene UNA INSTANCIA (no copia).
      Si test 1 modifica cliente_ejemplo, test 2 lo ve modificado.
      En la práctica, cada test obtiene instancia nueva porque
      pytest "reset" entre tests (o podrías usar scope="function").

    Returns:
        Cliente: Cliente de ejemplo válido (todos los campos válidos).
    """
    # Retornar cliente válido reutilizable
    return Cliente(
        nombre="Juan García",
        rfc="ABC123456XYZ",
        email="juan@ejemplo.com",
        telefono="5551234567"
    )


class TestClienteService:
    """Pruebas para la clase ClienteService."""

    def test_crear_servicio(self, servicio):
        """Prueba la creación de una instancia de ClienteService."""
        assert servicio is not None
        assert servicio.ruta_archivo is not None

    def test_agregar_cliente(self, servicio, cliente_ejemplo):
        """Prueba agregar un cliente."""
        servicio.agregar_cliente(cliente_ejemplo)

        assert len(servicio.obtener_todos()) == 1
        assert servicio.obtener_todos()[0] == cliente_ejemplo

    def test_agregar_cliente_duplicado_rfc(self, servicio, cliente_ejemplo):
        """
        Prueba que no se puede agregar un cliente con RFC duplicado.

        ¿REGLA DE NEGOCIO?
        - RFC es identificador único (México).
        - No puede haber dos clientes con mismo RFC.
        - Esta es una RESTRICCIÓN (constraint) de negocio.

        ¿POR QUÉ IMPORTANTE TESTEAR?
        - Si fallaría agregar duplicado, habría datos corruptos.
        - Prueba que agregar_cliente() valida RFC único ANTES de agregar.

        PATRÓN:
        1. Agregar cliente original (debe funcionar).
        2. Intentar agregar cliente con mismo RFC (debe fallar).
        3. pytest.raises() verifica que ValueError fue lanzado.
        """
        # ACT 1: Agregar cliente original
        servicio.agregar_cliente(cliente_ejemplo)

        # ARRANGE: Crear cliente duplicado (mismo RFC, diferente datos)
        cliente_duplicado = Cliente(
            nombre="Otro nombre",
            rfc="ABC123456XYZ",  # MISMO RFC que cliente_ejemplo
            email="otro@ejemplo.com",
            telefono="5559876543"
        )

        # ACT 2: Intentar agregar duplicado
        # ASSERT: Debe lanzar ValueError (RFC duplicado)
        with pytest.raises(ValueError):
            servicio.agregar_cliente(cliente_duplicado)

    def test_obtener_por_id(self, servicio, cliente_ejemplo):
        """Prueba obtener un cliente por ID."""
        servicio.agregar_cliente(cliente_ejemplo)

        cliente_recuperado = servicio.obtener_por_id(cliente_ejemplo.id)

        assert cliente_recuperado is not None
        assert cliente_recuperado == cliente_ejemplo

    def test_obtener_por_id_inexistente(self, servicio):
        """Prueba obtener un cliente con ID inexistente."""
        cliente = servicio.obtener_por_id("9999")

        assert cliente is None

    def test_obtener_por_rfc(self, servicio, cliente_ejemplo):
        """Prueba obtener un cliente por RFC."""
        servicio.agregar_cliente(cliente_ejemplo)

        cliente_recuperado = servicio.obtener_por_rfc("ABC123456XYZ")

        assert cliente_recuperado is not None
        assert cliente_recuperado.rfc == "ABC123456XYZ"

    def test_obtener_por_rfc_minusculas(self, servicio, cliente_ejemplo):
        """Prueba obtener un cliente por RFC en minúsculas."""
        servicio.agregar_cliente(cliente_ejemplo)

        cliente_recuperado = servicio.obtener_por_rfc("abc123456xyz")

        assert cliente_recuperado is not None

    def test_obtener_por_nombre(self, servicio):
        """Prueba obtener clientes por nombre."""
        cliente1 = Cliente(
            nombre="Juan García",
            rfc="ABC123456XYZ",
            email="juan@ejemplo.com",
            telefono="5551234567"
        )

        cliente2 = Cliente(
            nombre="Juan López",
            rfc="XYZ987654ABC",
            email="juan2@ejemplo.com",
            telefono="5559876543"
        )

        cliente3 = Cliente(
            nombre="María González",
            rfc="DEF456789UVW",
            email="maria@ejemplo.com",
            telefono="5555555555"
        )

        servicio.agregar_cliente(cliente1)
        servicio.agregar_cliente(cliente2)
        servicio.agregar_cliente(cliente3)

        resultados = servicio.obtener_por_nombre("Juan")

        assert len(resultados) == 2

    def test_obtener_todos(self, servicio):
        """Prueba obtener todos los clientes."""
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

        servicio.agregar_cliente(cliente1)
        servicio.agregar_cliente(cliente2)

        todos = servicio.obtener_todos()

        assert len(todos) == 2

    def test_modificar_cliente(self, servicio, cliente_ejemplo):
        """Prueba modificar un cliente."""
        servicio.agregar_cliente(cliente_ejemplo)

        datos_actualizados = {
            "nombre": "Juan García López",
            "email": "juan.nuevo@ejemplo.com"
        }

        cliente_modificado = servicio.modificar_cliente(
            cliente_ejemplo.id, datos_actualizados
        )

        assert cliente_modificado is not None
        assert cliente_modificado.nombre == "Juan García López"
        assert cliente_modificado.email == "juan.nuevo@ejemplo.com"

    def test_modificar_cliente_inexistente(self, servicio):
        """Prueba modificar un cliente inexistente."""
        resultado = servicio.modificar_cliente("9999", {"nombre": "Nuevo"})

        assert resultado is None

    def test_modificar_cliente_rfc_duplicado(self, servicio):
        """Prueba que no se puede asignar RFC duplicado al modificar."""
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

        servicio.agregar_cliente(cliente1)
        servicio.agregar_cliente(cliente2)

        with pytest.raises(ValueError):
            servicio.modificar_cliente(cliente1.id, {"rfc": "XYZ987654ABC"})

    def test_eliminar_cliente(self, servicio, cliente_ejemplo):
        """Prueba eliminar un cliente."""
        servicio.agregar_cliente(cliente_ejemplo)

        assert len(servicio.obtener_todos()) == 1

        resultado = servicio.eliminar_cliente(cliente_ejemplo.id)

        assert resultado is True
        assert len(servicio.obtener_todos()) == 0

    def test_eliminar_cliente_inexistente(self, servicio):
        """Prueba eliminar un cliente inexistente."""
        resultado = servicio.eliminar_cliente("9999")

        assert resultado is False

    def test_obtener_clientes_activos(self, servicio):
        """Prueba obtener solo clientes activos."""
        cliente1 = Cliente(
            nombre="Juan García",
            rfc="ABC123456XYZ",
            email="juan@ejemplo.com",
            telefono="5551234567",
            estado="activo"
        )

        cliente2 = Cliente(
            nombre="María López",
            rfc="XYZ987654ABC",
            email="maria@ejemplo.com",
            telefono="5559876543",
            estado="inactivo"
        )

        servicio.agregar_cliente(cliente1)
        servicio.agregar_cliente(cliente2)

        activos = servicio.obtener_clientes_activos()

        assert len(activos) == 1
        assert activos[0].nombre == "Juan García"

    def test_contar_clientes(self, servicio):
        """Prueba contar el número de clientes."""
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

        servicio.agregar_cliente(cliente1)
        servicio.agregar_cliente(cliente2)

        assert servicio.contar_clientes() == 2

    def test_persistencia_datos(self, archivo_temporal):
        """
        Prueba que los datos se persisten en archivo JSON.

        ¿POR QUÉ ES CRÍTICO?
        - Aplicación debe SOBREVIVIR a reinicios.
        - Primera ejecución: agregar cliente, guardar a JSON.
        - Segunda ejecución: cargar cliente desde JSON, datos intactos.
        - SIN persistencia: datos se pierden al cerrar app.

        PATRÓN:
        1. Crear servicio1, agregar cliente.
        2. Crear servicio2 NUEVO, carga datos desde MISMO archivo.
        3. Verificar que servicio2 ve los datos agregados por servicio1.
        4. Esto simula: Ejecución 1 → guardar, Ejecución 2 → cargar.

        DEVOPS:
        - Persistencia es crítica en producción.
        - Sin este test, podrías perder datos sin saberlo.
        - Incluir en suite de tests automáticos (CI/CD).
        """
        # ACT 1: Crear servicio, agregar cliente
        servicio1 = ClienteService(ruta_archivo=archivo_temporal)

        # ARRANGE: Crear cliente
        cliente = Cliente(
            nombre="Juan García",
            rfc="ABC123456XYZ",
            email="juan@ejemplo.com",
            telefono="5551234567"
        )

        # ACT 1 (cont): Agregar cliente (guardará a JSON)
        servicio1.agregar_cliente(cliente)

        # ACT 2: Crear NUEVO servicio (cargará desde MISMO archivo)
        # Simula: Segunda ejecución de la app
        servicio2 = ClienteService(ruta_archivo=archivo_temporal)

        # ASSERT: Verificar que servicio2 cargó los datos de servicio1
        assert len(servicio2.obtener_todos()) == 1
        assert servicio2.obtener_todos()[0].nombre == "Juan García"

    def test_limpiar_archivo(self, servicio, cliente_ejemplo):
        """Prueba limpiar el archivo de datos."""
        servicio.agregar_cliente(cliente_ejemplo)

        assert len(servicio.obtener_todos()) == 1

        servicio.limpiar_archivo()

        assert len(servicio.obtener_todos()) == 0

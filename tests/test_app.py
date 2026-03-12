"""
Tests para la aplicación Flask.
Utilizamos pytest con el test client de Flask.
"""

import json
import os
import tempfile
import pytest
from app.main import crear_app
from app.models import Cliente


@pytest.fixture
def app():
    """
    Fixture que crea una aplicación Flask para las pruebas.
    Usa un archivo temporal para los datos.
    """
    # Crear un archivo temporal para la base de datos de pruebas
    db_fd, db_path = tempfile.mkstemp()

    app = crear_app()

    # Configurar para usar el archivo temporal
    Cliente.DATA_FILE = db_path

    yield app

    # Limpiar después de las pruebas
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """
    Fixture que proporciona un cliente de prueba para la aplicación.
    """
    return app.test_client()


class TestHealth:
    """Tests para el endpoint de health check."""

    def test_health_check(self, client):
        """
        Verifica que el endpoint /health retorna status ok.
        """
        response = client.get('/health')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'ok'


class TestCrearCliente:
    """Tests para crear clientes."""

    def test_crear_cliente_valido(self, client):
        """
        Crea un cliente con datos válidos.
        """
        datos = {
            'nombre': 'Juan Pérez',
            'email': 'juan@example.com',
            'rfc': 'ABCD123456XYZ',
            'telefono': '5551234567'
        }

        response = client.post('/api/clientes',
                               data=json.dumps(datos),
                               content_type='application/json')

        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['nombre'] == 'Juan Pérez'
        assert data['email'] == 'juan@example.com'
        assert data['id'] == 1

    def test_crear_cliente_rfc_invalido(self, client):
        """
        Intenta crear un cliente con RFC inválido.
        """
        datos = {
            'nombre': 'Juan Pérez',
            'email': 'juan@example.com',
            'rfc': 'INVALIDO',
            'telefono': '5551234567'
        }

        response = client.post('/api/clientes',
                               data=json.dumps(datos),
                               content_type='application/json')

        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'RFC inválido' in data['error']

    def test_crear_cliente_email_invalido(self, client):
        """
        Intenta crear un cliente con email inválido.
        """
        datos = {
            'nombre': 'Juan Pérez',
            'email': 'email-invalido',
            'rfc': 'ABCD123456XYZ',
            'telefono': '5551234567'
        }

        response = client.post('/api/clientes',
                               data=json.dumps(datos),
                               content_type='application/json')

        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'Email inválido' in data['error']

    def test_crear_cliente_campos_faltantes(self, client):
        """
        Intenta crear un cliente sin enviar todos los campos.
        """
        datos = {
            'nombre': 'Juan Pérez',
            'email': 'juan@example.com'
        }

        response = client.post('/api/clientes',
                               data=json.dumps(datos),
                               content_type='application/json')

        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'Faltan campos requeridos' in data['error']


class TestListarClientes:
    """Tests para listar clientes."""

    def test_listar_clientes_vacio(self, client):
        """
        Lista clientes cuando no hay ninguno.
        """
        response = client.get('/api/clientes')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data == []

    def test_listar_clientes_con_datos(self, client):
        """
        Lista clientes después de crear algunos.
        """
        # Crear dos clientes
        cliente1 = {
            'nombre': 'Juan Pérez',
            'email': 'juan@example.com',
            'rfc': 'ABCD123456XYZ',
            'telefono': '5551234567'
        }

        cliente2 = {
            'nombre': 'María García',
            'email': 'maria@example.com',
            'rfc': 'DEFG654321ABC',
            'telefono': '5559876543'
        }

        client.post(
            '/api/clientes',
            data=json.dumps(cliente1),
            content_type='application/json')
        client.post(
            '/api/clientes',
            data=json.dumps(cliente2),
            content_type='application/json')

        # Listar
        response = client.get('/api/clientes')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) == 2
        assert data[0]['nombre'] == 'Juan Pérez'
        assert data[1]['nombre'] == 'María García'


class TestObtenerCliente:
    """Tests para obtener un cliente específico."""

    def test_obtener_cliente_existente(self, client):
        """
        Obtiene un cliente que existe.
        """
        # Crear un cliente
        datos = {
            'nombre': 'Juan Pérez',
            'email': 'juan@example.com',
            'rfc': 'ABCD123456XYZ',
            'telefono': '5551234567'
        }

        client.post(
            '/api/clientes',
            data=json.dumps(datos),
            content_type='application/json')

        # Obtener el cliente
        response = client.get('/api/clientes/1')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['id'] == 1
        assert data['nombre'] == 'Juan Pérez'

    def test_obtener_cliente_no_existente(self, client):
        """
        Intenta obtener un cliente que no existe.
        """
        response = client.get('/api/clientes/999')

        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'no encontrado' in data['error']


class TestEliminarCliente:
    """Tests para eliminar clientes."""

    def test_eliminar_cliente_existente(self, client):
        """
        Elimina un cliente que existe.
        """
        # Crear un cliente
        datos = {
            'nombre': 'Juan Pérez',
            'email': 'juan@example.com',
            'rfc': 'ABCD123456XYZ',
            'telefono': '5551234567'
        }

        client.post(
            '/api/clientes',
            data=json.dumps(datos),
            content_type='application/json')

        # Eliminar el cliente
        response = client.delete('/api/clientes/1')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'exitosamente' in data['mensaje']

        # Verificar que fue eliminado
        response = client.get('/api/clientes/1')
        assert response.status_code == 404

    def test_eliminar_cliente_no_existente(self, client):
        """
        Intenta eliminar un cliente que no existe.
        """
        response = client.delete('/api/clientes/999')

        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'no encontrado' in data['error']

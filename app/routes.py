"""
Rutas de la aplicación Flask.
Define los endpoints CRUD para la gestión de clientes.
"""

from flask import Blueprint, request, jsonify
from app.models import Cliente
from app.validators import validar_rfc, validar_email

# Crear blueprint para las rutas
api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/clientes', methods=['GET'])
def listar_clientes():
    """
    GET /api/clientes
    Retorna la lista de todos los clientes.
    """
    clientes = Cliente.obtener_todos()
    return jsonify(clientes), 200


@api_bp.route('/clientes', methods=['POST'])
def crear_cliente():
    """
    POST /api/clientes
    Crea un nuevo cliente.

    Body esperado:
    {
        "nombre": "Juan Pérez",
        "email": "juan@example.com",
        "rfc": "ABCD123456XYZ",
        "telefono": "5551234567"
    }
    """
    datos = request.get_json()

    # Validar que se recibieron todos los campos
    campos_requeridos = ['nombre', 'email', 'rfc', 'telefono']
    if not datos or not all(campo in datos for campo in campos_requeridos):
        return jsonify({'error': 'Faltan campos requeridos'}), 400

    nombre = datos.get('nombre', '').strip()
    email = datos.get('email', '').strip()
    rfc = datos.get('rfc', '').strip()
    telefono = datos.get('telefono', '').strip()

    # Validar que los campos no estén vacíos
    if not all([nombre, email, rfc, telefono]):
        return jsonify({'error': 'Los campos no pueden estar vacíos'}), 400

    # Validar RFC
    if not validar_rfc(rfc):
        return jsonify({'error': 'RFC inválido. Formato: 4 letras + 6 dígitos + 3 alfanuméricos'}), 400

    # Validar email
    if not validar_email(email):
        return jsonify({'error': 'Email inválido'}), 400

    # Crear el cliente
    cliente = Cliente.crear(nombre, email, rfc, telefono)

    return jsonify(cliente), 201


@api_bp.route('/clientes/<int:cliente_id>', methods=['GET'])
def obtener_cliente(cliente_id):
    """
    GET /api/clientes/<id>
    Retorna un cliente específico por su ID.
    """
    cliente = Cliente.obtener_por_id(cliente_id)

    if cliente is None:
        return jsonify({'error': 'Cliente no encontrado'}), 404

    return jsonify(cliente), 200


@api_bp.route('/clientes/<int:cliente_id>', methods=['DELETE'])
def eliminar_cliente(cliente_id):
    """
    DELETE /api/clientes/<id>
    Elimina un cliente específico por su ID.
    """
    eliminado = Cliente.eliminar(cliente_id)

    if not eliminado:
        return jsonify({'error': 'Cliente no encontrado'}), 404

    return jsonify({'mensaje': 'Cliente eliminado exitosamente'}), 200

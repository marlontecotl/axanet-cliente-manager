"""
Aplicación principal Flask.
Punto de entrada de la aplicación.
"""

from flask import Flask, jsonify
from app.routes import api_bp


def crear_app():
    """
    Factory function para crear la aplicación Flask.
    """
    app = Flask(__name__)

    # Registrar blueprints
    app.register_blueprint(api_bp)

    # Endpoint de health check
    @app.route('/health', methods=['GET'])
    def health():
        """
        GET /health
        Verifica que la aplicación está funcionando.
        """
        return jsonify({'status': 'ok'}), 200

    # Manejo de errores 404
    @app.errorhandler(404)
    def no_encontrado(error):
        """
        Maneja peticiones a rutas que no existen.
        """
        return jsonify({'error': 'Ruta no encontrada'}), 404

    # Manejo de errores 500
    @app.errorhandler(500)
    def error_interno(error):
        """
        Maneja errores internos del servidor.
        """
        return jsonify({'error': 'Error interno del servidor'}), 500

    return app


# Crear la aplicación
app = crear_app()


if __name__ == '__main__':
    # Ejecutar en modo desarrollo
    # Para producción, usar gunicorn u otro WSGI server
    app.run(debug=True, host='0.0.0.0', port=5000)

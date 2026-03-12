"""
Módulo de modelos para la aplicación.
Utilizamos un modelo simple basado en diccionarios (sin ORM).
"""

import json
import os
from datetime import datetime


class Cliente:
    """
    Modelo de Cliente.
    Almacena datos en un archivo JSON para persistencia simple.
    """

    # Ruta del archivo de datos
    DATA_FILE = 'data/clientes.json'

    @classmethod
    def _obtener_proximo_id(cls):
        """
        Obtiene el próximo ID disponible.
        """
        clientes = cls._cargar_datos()
        if not clientes:
            return 1
        return max(c['id'] for c in clientes) + 1

    @classmethod
    def _cargar_datos(cls):
        """
        Carga todos los clientes del archivo JSON.
        Si el archivo no existe, retorna una lista vacía.
        """
        if not os.path.exists(cls.DATA_FILE):
            return []

        try:
            with open(cls.DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    @classmethod
    def _guardar_datos(cls, clientes):
        """
        Guarda todos los clientes en el archivo JSON.
        """
        # Asegura que el directorio exista
        os.makedirs(os.path.dirname(cls.DATA_FILE), exist_ok=True)

        with open(cls.DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(clientes, f, indent=2, ensure_ascii=False)

    @classmethod
    def crear(cls, nombre, email, rfc, telefono):
        """
        Crea un nuevo cliente y lo guarda en el archivo.
        Retorna el cliente creado con su ID.
        """
        cliente = {
            'id': cls._obtener_proximo_id(),
            'nombre': nombre,
            'email': email,
            'rfc': rfc.upper(),
            'telefono': telefono,
            'creado_en': datetime.now().isoformat()
        }

        clientes = cls._cargar_datos()
        clientes.append(cliente)
        cls._guardar_datos(clientes)

        return cliente

    @classmethod
    def obtener_todos(cls):
        """
        Obtiene todos los clientes.
        """
        return cls._cargar_datos()

    @classmethod
    def obtener_por_id(cls, cliente_id):
        """
        Obtiene un cliente específico por su ID.
        Retorna None si no lo encuentra.
        """
        clientes = cls._cargar_datos()
        for cliente in clientes:
            if cliente['id'] == cliente_id:
                return cliente
        return None

    @classmethod
    def eliminar(cls, cliente_id):
        """
        Elimina un cliente por su ID.
        Retorna True si fue eliminado, False si no existía.
        """
        clientes = cls._cargar_datos()

        for i, cliente in enumerate(clientes):
            if cliente['id'] == cliente_id:
                del clientes[i]
                cls._guardar_datos(clientes)
                return True

        return False

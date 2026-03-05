"""
Módulo del modelo Cliente.

Este módulo contiene la clase Cliente que representa a los clientes
de AXANET y hereda de EntidadBase.

CONCEPTOS FUNDAMENTALES APLICADOS:
- Herencia (IS-A): Cliente ES-UN tipo de EntidadBase.
- Reutilización de código: Heredamos ID, fechas y métodos de EntidadBase.
- Polimorfismo: Implementamos validar() y a_diccionario() específico para Cliente.
"""

from typing import Dict, Any
from .base import EntidadBase


class Cliente(EntidadBase):
    """
    Clase que representa un cliente de AXANET.

    Hereda de EntidadBase y agrega atributos específicos de clientes
    como nombre, RFC, email, teléfono y estado.

    ¿POR QUÉ HEREDA DE ENTIDADBASE?
    - Reutilización: No necesitamos reimplementar ID, fechas, __str__, __repr__.
    - Consistencia: Todos los clientes se comportan igual respecto a ID y auditoría.
    - Escalabilidad: Si agregamos Proveedor, Empleado, etc., todos usan la base.
    - Mantenimiento: Cambios en EntidadBase benefician a todas las subclases.

    RELACIÓN IS-A (ES-UN):
    - Un Cliente IS-A EntidadBase.
    - Un Cliente tiene TODO lo que tiene una EntidadBase + sus atributos propios.
    - Análogo: "Un Auto IS-A Vehículo" (el auto hereda llantas, motor, etc.).

    Attributes:
        nombre (str): Nombre del cliente (validado: 3+ caracteres, sin números).
        rfc (str): RFC del cliente (Registro Federal de Contribuyentes - México).
                   Formato: 3-4 letras + 6 dígitos + 0-3 caracteres alfanuméricos.
        email (str): Correo electrónico del cliente (validado con regex).
        telefono (str): Número de teléfono del cliente (10+ dígitos).
        estado (str): Estado del cliente ("activo" o "inactivo").
    """

    def __init__(self, nombre: str, rfc: str, email: str,
                 telefono: str, estado: str = "activo"):
        """
        Inicializa una nueva instancia de Cliente.

        ¿ORDEN DE OPERACIONES?
        1. super().__init__() - PRIMERO: Inicializa EntidadBase (genera ID, fechas).
        2. Asignar atributos específicos del Cliente.
        3. Llamar a validar() - ÚLTIMO: Verifica datos antes de usar el objeto.

        ¿POR QUÉ LLAMAR SUPER().__INIT__()?
        - EntidadBase.__init__() genera el ID único y las fechas.
        - SIN esto, no tendríamos id, fecha_creacion, fecha_modificacion.
        - Es OBLIGATORIO llamarlo antes de acceder a estos atributos.
        - Análogo: Construir los cimientos ANTES de levantar las paredes.

        ¿POR QUÉ VALIDAR AL FINAL?
        - PATRÓN "FAIL-FAST": Detectar errores INMEDIATAMENTE.
        - Si alguien intenta crear un Cliente con RFC inválido, falla en __init__.
        - Es mejor fallar al crear el objeto que permitir datos inválidos.
        - Previene estados inconsistentes (Cliente con RFC="123" nunca debería existir).

        Args:
            nombre (str): Nombre del cliente (ej: "Juan García López").
            rfc (str): RFC del cliente (ej: "ABC123456XYZ").
            email (str): Correo electrónico del cliente (ej: "juan@ejemplo.com").
            telefono (str): Número de teléfono del cliente (ej: "5551234567").
            estado (str): Estado del cliente. Por defecto "activo".
                         Valores válidos: "activo", "inactivo".

        Raises:
            ValueError: Si alguno de los parámetros no cumple validación.
                       El mensaje de error incluye el campo y valor inválido.

        Ejemplo:
            cliente = Cliente(
                nombre="María González",
                rfc="MGO123456XYZ",
                email="maria@axanet.com",
                telefono="5551234567",
                estado="activo"
            )
        """
        # PASO 1: Inicializar la clase base (genera ID, fechas)
        super().__init__()

        # PASO 2: Asignar atributos específicos de Cliente
        self.nombre = nombre
        self.rfc = rfc
        self.email = email
        self.telefono = telefono
        self.estado = estado

        # PASO 3: Validar datos (falla rápido si hay problemas)
        self.validar()

    def validar(self) -> bool:
        """
        Valida los datos del cliente.

        ¿CÓMO FUNCIONA?
        1. Importa funciones de validación del módulo validators.
        2. Llama a cada validador para cada atributo.
        3. Si alguna validación falla, lanza ValueError.
        4. Si todas pasan, retorna True.

        ¿POR QUÉ LAS IMPORTACIONES ESTÁN ADENTRO?
        - PREVENCIÓN DE IMPORTACIONES CIRCULARES.
        - Si importáramos en el top del archivo, tendríamos:
          - base.py importa cliente.py
          - cliente.py importa validators.py
          - validators podría importar cliente.py → CICLO INFINITO.
        - Importar dentro del método evita esto (se importan solo cuando se necesitan).
        - Técnica común en Python para romper ciclos de dependencia.

        ¿PATRÓN DE VALIDACIÓN?
        - Cada campo tiene su propia función de validación (SRP).
        - Las validaciones son CENTRALIZADAS en el módulo validators.
        - Los cambios en reglas de validación se hacen en un solo lugar.
        - Reutilizable: main.py también usa estas validaciones en la CLI.

        Returns:
            bool: True si el cliente es válido.

        Raises:
            ValueError: Si algún campo no cumple las reglas de validación.
                       El mensaje incluye qué campo falló y el valor inválido.

        Ejemplo:
            try:
                cliente = Cliente("Jo", "ABC123456XYZ", "j@e.com", "555123")
            except ValueError as e:
                print(f"Error: {e}")  # Output: "Error: Nombre inválido: Jo"
        """
        # Importar funciones de validación (dentro del método, no en top)
        from ..validators.validators import (validar_nombre, validar_rfc,
                                             validar_email, validar_telefono,
                                             validar_estado)

        # Validar nombre
        if not validar_nombre(self.nombre):
            raise ValueError(f"Nombre inválido: {self.nombre}")

        # Validar RFC
        if not validar_rfc(self.rfc):
            raise ValueError(f"RFC inválido: {self.rfc}")

        # Validar email
        if not validar_email(self.email):
            raise ValueError(f"Email inválido: {self.email}")

        # Validar teléfono
        if not validar_telefono(self.telefono):
            raise ValueError(f"Teléfono inválido: {self.telefono}")

        # Validar estado
        if not validar_estado(self.estado):
            raise ValueError(f"Estado inválido: {self.estado}")

        return True

    def a_diccionario(self) -> Dict[str, Any]:
        """
        Convierte el cliente a un diccionario (serialización).

        ¿POR QUÉ ES IMPORTANTE?
        - JSON no entiende objetos Python, solo dicts.
        - ClienteService usa esto para guardar datos a archivo JSON.
        - Permite intercambio de datos con APIs (REST, etc).
        - Facilita conversión a CSV, XML, u otros formatos.

        ¿CONTENIDO DEL DICCIONARIO?
        - Todos los atributos de Cliente (nombre, rfc, email, telefono, estado).
        - Heredados de EntidadBase (id, fecha_creacion, fecha_modificacion).
        - Las fechas se convierten a ISO 8601 (formato estándar para JSON).

        ¿POR QUÉ ISOFORMAT()?
        - datetime.isoformat() genera strings como "2024-01-15T10:30:45.123456".
        - Formato ISO 8601 es estándar internacional (legible, parseable).
        - JSON puede almacenar strings de fecha; luego se reconvierten a datetime.

        Returns:
            Dict[str, Any]: Diccionario con todos los datos del cliente.

        Ejemplo:
            cliente = Cliente("Juan", "ABC123456XYZ", "j@e.com", "555123")
            dic = cliente.a_diccionario()
            # dic = {
            #     "id": "1",
            #     "nombre": "Juan",
            #     "rfc": "ABC123456XYZ",
            #     "email": "j@e.com",
            #     "telefono": "555123",
            #     "estado": "activo",
            #     "fecha_creacion": "2024-01-15T10:30:45.123456",
            #     "fecha_modificacion": "2024-01-15T10:30:45.123456"
            # }
        """
        return {
            "id": self.id,
            "nombre": self.nombre,
            "rfc": self.rfc,
            "email": self.email,
            "telefono": self.telefono,
            "estado": self.estado,
            # Convertir datetime a ISO 8601 string (JSON-compatible)
            "fecha_creacion": self.fecha_creacion.isoformat(),
            "fecha_modificacion": self.fecha_modificacion.isoformat()
        }

    @classmethod
    def desde_diccionario(cls, datos: Dict[str, Any]) -> "Cliente":
        """
        Crea una instancia de Cliente a partir de un diccionario (deserialización).

        ¿POR QUÉ ES UN CLASSMETHOD?
        - PATRÓN "FACTORY": Método que construye objetos de forma especial.
        - Recibe cls (la clase) como primer argumento, no self (la instancia).
        - Permite crear instancias de maneras alternativas.
        - Similar a constructores parametrizados en otros lenguajes.

        ¿CÓMO FUNCIONA?
        1. Toma un diccionario (típicamente cargado desde JSON).
        2. Extrae los valores necesarios.
        3. Llama al __init__() con esos valores.
        4. Si el diccionario tiene "id", PRESERVA el ID original.

        ¿POR QUÉ PRESERVAR EL ID?
        - Cuando cargamos datos desde archivo, queremos mantener IDs antiguos.
        - SIN esto, cada cliente cargado tendría un nuevo ID único.
        - Los datos históricos pierden sus identidades.
        - Es crítico para persistencia: si guardamos cliente id=5, al recargar
          debe ser id=5 de nuevo, no id=6.

        Args:
            datos (Dict[str, Any]): Diccionario con los datos del cliente.
                                   Típicamente: {"nombre": "...", "rfc": "...", ...}

        Returns:
            Cliente: Nueva instancia de Cliente con los datos del diccionario.

        Raises:
            KeyError: Si faltan campos requeridos (nombre, rfc, email, telefono).
            ValueError: Si los datos no pasan validación.

        Ejemplo:
            # Cargar cliente desde JSON
            datos = {
                "id": "5",
                "nombre": "Juan García",
                "rfc": "ABC123456XYZ",
                "email": "juan@ejemplo.com",
                "telefono": "5551234567",
                "estado": "activo"
            }
            cliente = Cliente.desde_diccionario(datos)
            print(cliente.id)  # Output: "5" (ID preservado)
        """
        # Crear instancia con datos del diccionario
        cliente = cls(
            nombre=datos["nombre"],
            rfc=datos["rfc"],
            email=datos["email"],
            telefono=datos["telefono"],
            # estado tiene valor por defecto, pero puede ser sobrescrito
            estado=datos.get("estado", "activo")
        )

        # PASO CRÍTICO: Preservar ID original si existe en el diccionario
        # Sin esto, cada carga obtendría un nuevo ID (contador incrementado).
        if "id" in datos:
            cliente.id = datos["id"]

        return cliente

    def __str__(self) -> str:
        """
        Representación en cadena del cliente (legible).

        ¿POR QUÉ OVERRIDE?
        - La clase base muestra solo "Cliente(id=1)".
        - Aquí mostramos más información útil: nombre, RFC.
        - print(cliente) es más informativo: "Cliente(id=1, nombre=Juan, rfc=ABC123456XYZ)".

        Returns:
            str: Representación en cadena del cliente.

        Ejemplo:
            cliente = Cliente("Juan", "ABC123456XYZ", "j@e.com", "555123")
            print(cliente)
            # Output: Cliente(id=1, nombre=Juan, rfc=ABC123456XYZ)
        """
        return f"Cliente(id={self.id}, nombre={self.nombre}, rfc={self.rfc})"

    def __eq__(self, other) -> bool:
        """
        Compara dos clientes por su ID (igualdad).

        ¿POR QUÉ COMPARAR SOLO POR ID?
        - El ID es lo que define la IDENTIDAD de un cliente.
        - Dos clientes con el mismo ID son el MISMO cliente (aunque otros datos cambien).
        - NO comparamos por nombre/RFC/email porque:
          - Un cliente puede cambiar su nombre pero es la misma persona (mismo ID).
          - Datos pueden estar desactualizados en diferentes copias.
          - Solo el ID garantiza identidad única.

        ¿PATRÓN?
        - Primero verificamos isinstance() para seguridad de tipo.
        - Luego comparamos el atributo diferenciador (id).
        - Es una GUARD CLAUSE (verificación temprana de condición).

        Args:
            other: Otro objeto a comparar (puede ser cualquier tipo).

        Returns:
            bool: True si ambos son Cliente con el mismo ID, False en caso contrario.

        Ejemplo:
            cliente1 = Cliente("Juan", "ABC123456XYZ", "j@e.com", "555123")
            cliente2 = Cliente("María", "XYZ987654ABC", "m@e.com", "555456")

            cliente1.id = "10"
            cliente2.id = "10"

            print(cliente1 == cliente2)  # True (mismo ID)
            print(cliente1 == "Juan")     # False (no es Cliente)
        """
        # GUARD CLAUSE: Verificar tipo antes de comparar
        if not isinstance(other, Cliente):
            return False

        # Comparar por ID (lo que define identidad)
        return self.id == other.id

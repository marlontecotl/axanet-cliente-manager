"""
Módulo del servicio de Cliente.

Este módulo contiene la clase ClienteService que proporciona operaciones
CRUD para la gestión de clientes con persistencia en archivos JSON.

ARQUITECTURA Y PATRONES:
- PATRÓN REPOSITORY: Separa lógica de persistencia del modelo.
- PRINCIPIO SRP (Single Responsibility): ClienteService solo maneja operaciones CRUD.
- PATRÓN FACADE: Proporciona interfaz simplificada para trabajar con clientes.
- VALIDACIÓN EN CAPAS: El modelo valida datos, el servicio valida reglas de negocio.
"""

import json
import os
from typing import List, Optional, Dict, Any
from ..models.cliente import Cliente


class ClienteService:
    """
    Servicio CRUD para la gestión de clientes.

    Proporciona métodos para agregar, consultar, actualizar y eliminar
    clientes con persistencia en archivo JSON.

    ¿POR QUÉ SEPARAR SERVICIO DE MODELO?
    - PRINCIPIO SRP (Single Responsibility Principle):
      - Cliente: Representa UN cliente, valida sus datos.
      - ClienteService: Maneja COLECCIONES de clientes, persistencia, búsquedas.
    - MANTENIBILIDAD: Cambios en formato JSON NO afectan la clase Cliente.
    - TESTABILIDAD: Podemos mockear el servicio sin tocar el modelo.
    - REUTILIZACIÓN: Otros servicios pueden usar Cliente (emails, reportes, etc).

    ¿PERSISTENCIA EN SERVICIO, NO EN MODELO?
    - El modelo Cliente NO debe "saber" cómo guardarse a JSON.
    - El modelo es PURO (solo datos y validación).
    - El servicio es SUCIO (maneja archivos, I/O).
    - Analogía: Un cliente no sabe cómo llenar su propio formulario en el registro.
      El recepcionista (servicio) es quien lo hace.

    ¿PATRÓN REPOSITORY?
    - ClienteService es un "Repository" (almacén de datos).
    - Abstrae cómo se almacenan los datos (podrían ser JSON, SQL, MongoDB).
    - El código que usa ClienteService no importa DÓNDE están los datos.
    - Si mañana cambias de JSON a SQL, solo ClienteService cambia.

    Attributes:
        ruta_archivo (str): Ruta del archivo JSON donde se almacenan los datos.
                           Por defecto: "data/clientes.json".
        clientes (List[Cliente]): Lista en memoria de clientes cargados desde archivo.
                                 Se sincroniza con archivo en cada operación CRUD.
    """

    def __init__(self, ruta_archivo: str = "data/clientes.json"):
        """
        Inicializa el servicio de clientes.

        ¿PASOS DE INICIALIZACIÓN?
        1. Almacenar ruta del archivo.
        2. Inicializar lista vacía de clientes.
        3. Asegurar que el directorio existe (crear si no existe).
        4. Cargar clientes desde archivo (si existe).

        ¿POR QUÉ ESTE ORDEN?
        - Necesitamos ruta_archivo ANTES de crear el directorio.
        - Necesitamos el directorio ANTES de cargar el archivo.
        - Es una secuencia lógica de dependencias.

        Args:
            ruta_archivo (str): Ruta del archivo JSON.
                              Por defecto 'data/clientes.json'.
                              Ejemplo: "/var/data/clientes.json", "clientes.json"
        """
        self.ruta_archivo = ruta_archivo
        self.clientes: List[Cliente] = []  # Lista en memoria (caché)
        self._asegurar_directorio()  # Crear dir si no existe
        self.cargar_clientes()  # Cargar datos persistidos

    def _asegurar_directorio(self) -> None:
        """
        Asegura que el directorio del archivo existe.

        ¿POR QUÉ ES IMPORTANTE?
        - Si la ruta es "data/clientes.json", el directorio "data" debe existir.
        - Sin esto, os.open(ruta) falla con FileNotFoundError.
        - Este método crea el directorio automáticamente si no existe.
        - ROBUSTEZ: La aplicación no falla si el directorio no existe.

        ¿CÓMO FUNCIONA?
        1. os.path.dirname() extrae la parte del directorio de la ruta.
           Ejemplo: "data/clientes.json" → "data"
        2. Verificar si directorio NO está vacío (porque "" sería directorio actual).
        3. Si no existe, os.makedirs() lo crea (también crea padres si necesario).

        ¿BUENA PRÁCTICA DEVOPS?
        - Aplicaciones robustas no fallan por directorios faltantes.
        - Preparar el entorno es parte de la inicialización.
        - En CI/CD, esto evita pasos manuales de creación de directorios.

        Ejemplo:
            servicio = ClienteService("data/clientes.json")
            # Si "data/" no existe, se crea automáticamente.
        """
        # Extraer componente de directorio de la ruta
        directorio = os.path.dirname(self.ruta_archivo)

        # Verificar que directorio no está vacío Y que no existe
        if directorio and not os.path.exists(directorio):
            # Crear directorio (create parents if needed)
            os.makedirs(directorio)

    def cargar_clientes(self) -> None:
        """
        Carga los clientes desde el archivo JSON a memoria.

        ¿CÓMO FUNCIONA?
        1. Verificar si el archivo existe.
        2. Si existe, leerlo y parsearlo como JSON.
        3. Convertir cada dict a objeto Cliente usando desde_diccionario().
        4. Si no existe, inicializar lista vacía (primera ejecución).

        ¿ENCODING='UTF-8'?
        - UTF-8 es codificación universal que soporta caracteres internacionales.
        - RFC mexicano, nombres con tildes (José, María), ñ (MAÑANA).
        - SIN especificar, Python podría usar encoding local (problemático en producción).
        - BUENA PRÁCTICA: Siempre especificar encoding explícitamente.

        ¿POR QUÉ CONTENIDO.STRIP()?
        - .strip() elimina espacios/saltos de línea al inicio/fin.
        - Un archivo vacío después de strip() es '' (vacío, no error).
        - Previene json.JSONDecodeError con archivos vacíos.

        ¿MANEJO DE EXCEPCIONES?
        - json.JSONDecodeError: JSON inválido en archivo.
        - KeyError: Faltan campos requeridos en diccionario.
        - ValueError: Datos que no pasan validación de Cliente.
        - Todas se propagan como Exception genérica (el servicio falla ruidosamente).

        ¿PATRÓN?
        - EAGER LOADING: Cargar todos los datos en __init__().
        - Alternativa: LAZY LOADING (cargar cuando se necesita).
        - Elegimos eager por simplicidad, pero JSON cache se sincroniza siempre.

        Raises:
            Exception: Si hay error al leer o parsear el archivo.

        Ejemplo:
            # Primera ejecución (archivo no existe)
            servicio = ClienteService("nuevos_datos.json")
            print(servicio.clientes)  # []

            # Agregar cliente
            cliente = Cliente("Juan", "ABC123456XYZ", "j@e.com", "555123")
            servicio.agregar_cliente(cliente)
            # Archivo guardado

            # Cargar nuevamente
            servicio2 = ClienteService("nuevos_datos.json")
            print(servicio2.clientes)  # [Cliente(Juan)]
        """
        if os.path.exists(self.ruta_archivo):
            try:
                # Abrir archivo con encoding UTF-8 (soporte internacional)
                with open(self.ruta_archivo, 'r', encoding='utf-8') as f:
                    # Leer contenido y eliminar espacios/saltos de línea
                    contenido = f.read().strip()

                    # Caso especial: archivo vacío (primera ejecución)
                    if not contenido:
                        self.clientes = []
                    else:
                        # Parsear JSON a lista de dicts
                        datos = json.loads(contenido)

                        # Convertir cada dict a objeto Cliente
                        # List comprehension más limpio que for loop
                        self.clientes = [
                            Cliente.desde_diccionario(cliente_dict)
                            for cliente_dict in datos
                        ]
            except (json.JSONDecodeError, KeyError, ValueError) as e:
                # Propagar error con contexto útil
                raise Exception(
                    f"Error al cargar clientes desde {self.ruta_archivo}: {str(e)}"
                )
        else:
            # Archivo no existe (primera ejecución): lista vacía
            self.clientes = []

    def guardar_clientes(self) -> None:
        """
        Guarda los clientes en el archivo JSON (serialización).

        ¿CUÁNDO SE LLAMA?
        - Después de agregar cliente.
        - Después de modificar cliente.
        - Después de eliminar cliente.
        - Cada cambio se persiste inmediatamente (Write-Through pattern).

        ¿PASOS?
        1. Asegurar que el directorio existe (por si fue eliminado).
        2. Abrir archivo en modo ESCRITURA ('w').
        3. Convertir todos los objetos Cliente a dicts.
        4. Usar json.dump() para serializar a archivo.

        ¿ENSURE_ASCII=FALSE?
        - ensure_ascii=True: Convierte caracteres no-ASCII a \\uXXXX (ilegible).
          Ejemplo: José → Jos\\u00e9
        - ensure_ascii=False: Preserva caracteres Unicode directamente (legible).
          Ejemplo: José → José (tal cual)
        - BUENA PRÁCTICA: Usar False para datos internacionales (México).

        ¿INDENT=2?
        - Formatea JSON con indentación de 2 espacios.
        - Sin indentación sería: [{"id":"1","nombre":"Juan"}]
        - Con indentación es legible para debugging:
          [
            {
              "id": "1",
              "nombre": "Juan"
            }
          ]

        ¿WRITE-THROUGH PATTERN?
        - Cada cambio se escribe al archivo inmediatamente.
        - Alternativa: Write-Back (cambios en memoria, escribir al cerrar).
        - Write-Through es más seguro (menos riesgo de pérdida de datos).
        - En producción: Base de datos con transactions proporciona aún más seguridad.

        Raises:
            IOError: Si hay problema escribiendo al archivo (permisos, disco lleno).

        Ejemplo:
            cliente = Cliente("Juan", "ABC123456XYZ", "j@e.com", "555123")
            servicio.agregar_cliente(cliente)  # Esto llama a guardar_clientes()
            # Archivo ahora contiene: [{"id": "1", "nombre": "Juan", ...}]
        """
        try:
            # Asegurar que el directorio existe (por si fue eliminado entre operaciones)
            self._asegurar_directorio()

            # Abrir archivo en modo ESCRITURA (crea si no existe, trunca si existe)
            with open(self.ruta_archivo, 'w', encoding='utf-8') as f:
                # Convertir todos los Cliente a dicts
                datos = [cliente.a_diccionario() for cliente in self.clientes]

                # Serializar a JSON con formato legible
                # ensure_ascii=False: Preserva caracteres acentuados (José, México)
                # indent=2: Indentación para legibilidad
                json.dump(datos, f, ensure_ascii=False, indent=2)
        except IOError as e:
            # Propagar error con contexto
            raise IOError(
                f"Error al guardar clientes en {self.ruta_archivo}: {str(e)}"
            )

    def agregar_cliente(self, cliente: Cliente) -> None:
        """
        Agrega un nuevo cliente.

        ¿VALIDACIONES?
        1. Verificar que es un objeto Cliente (type check).
        2. Verificar que no existe cliente con mismo RFC (regla de negocio).
        3. Si pasa ambas, agregar y guardar.

        ¿POR QUÉ VALIDAR RFC ÚNICO?
        - RFC es identificador fiscal único en México.
        - No puede haber dos clientes con mismo RFC (regla de negocio AXANET).
        - El modelo no sabe de otros clientes (su responsabilidad es menor).
        - El servicio es quien valida "reglas de negocio" (restricciones globales).

        ¿PATRÓN?
        - VALIDACIÓN EN CAPAS:
          - Modelo: Valida que RFC tiene formato correcto (ej: 12-13 chars).
          - Servicio: Valida que RFC es único en la colección.
        - Ambas capas son necesarias para consistencia de datos.

        ¿POR QUÉ TYPE CHECK?
        - Podrías pasar un dict por error.
        - isinstance() verifica que es realmente un Cliente.
        - FAIL-FAST: Error claro inmediatamente, no más adelante.

        Args:
            cliente (Cliente): Objeto Cliente a agregar.

        Raises:
            TypeError: Si el argumento no es una instancia de Cliente.
            ValueError: Si ya existe un cliente con el mismo RFC.

        Ejemplo:
            cliente1 = Cliente("Juan", "ABC123456XYZ", "j@e.com", "555123")
            servicio.agregar_cliente(cliente1)  # OK, agregado

            cliente2 = Cliente("María", "ABC123456XYZ", "m@e.com", "555456")
            servicio.agregar_cliente(cliente2)  # ValueError: RFC duplicado
        """
        # VALIDACIÓN 1: Verificar tipo
        if not isinstance(cliente, Cliente):
            raise TypeError("El argumento debe ser una instancia de Cliente")

        # VALIDACIÓN 2: Verificar RFC único (regla de negocio AXANET)
        # obtener_por_rfc retorna Cliente si existe, None si no
        if self.obtener_por_rfc(cliente.rfc):
            raise ValueError(
                f"Ya existe un cliente con RFC {cliente.rfc}"
            )

        # Si pasó ambas validaciones, agregar a lista en memoria
        self.clientes.append(cliente)

        # Persistir cambios a archivo
        self.guardar_clientes()

    def obtener_todos(self) -> List[Cliente]:
        """
        Obtiene todos los clientes.

        ¿POR QUÉ RETORNAR UNA COPIA?
        - PROGRAMACIÓN DEFENSIVA: Prevenir que el usuario modifique la lista interna.
        - Sin .copy(): Si alguien hace `lista = servicio.obtener_todos(); lista.clear()`
          estaría borrando los datos internos SIN guardar.
        - Con .copy(): El usuario obtiene una copia que puede modificar sin riesgo.

        ¿ANALOGÍA?
        - Es como dar una fotocopia de un archivo, no el archivo original.
        - Si escriben en la copia, el original no se afecta.
        - Si necesitan modificar, deben usar los métodos del servicio (add, remove, etc).

        Returns:
            List[Cliente]: Copia de la lista de clientes.

        Ejemplo:
            servicio.agregar_cliente(cliente1)
            todos = servicio.obtener_todos()
            todos.clear()  # Borra la copia
            print(servicio.contar_clientes())  # Aún 1 (original intacto)
        """
        # .copy() retorna una copia superficial de la lista
        # Los objetos Cliente dentro siguen siendo los mismos, pero la lista es nueva
        return self.clientes.copy()

    def obtener_por_id(self, cliente_id: str) -> Optional[Cliente]:
        """
        Obtiene un cliente por su ID.

        Args:
            cliente_id (str): ID del cliente a buscar.

        Returns:
            Optional[Cliente]: El cliente encontrado o None.
        """
        for cliente in self.clientes:
            if cliente.id == cliente_id:
                return cliente
        return None

    def obtener_por_rfc(self, rfc: str) -> Optional[Cliente]:
        """
        Obtiene un cliente por su RFC.

        Args:
            rfc (str): RFC del cliente a buscar.

        Returns:
            Optional[Cliente]: El cliente encontrado o None.
        """
        rfc = rfc.strip().upper()
        for cliente in self.clientes:
            if cliente.rfc.upper() == rfc:
                return cliente
        return None

    def obtener_por_nombre(self, nombre: str) -> List[Cliente]:
        """
        Obtiene clientes que contienen el nombre especificado.

        Args:
            nombre (str): Nombre o parte del nombre a buscar.

        Returns:
            List[Cliente]: Lista de clientes que coinciden con la búsqueda.
        """
        nombre_lower = nombre.lower().strip()
        resultados = [
            cliente for cliente in self.clientes
            if nombre_lower in cliente.nombre.lower()
        ]
        return resultados

    def modificar_cliente(self, cliente_id: str, datos: Dict[str, Any]) -> Optional[Cliente]:
        """
        Modifica los datos de un cliente existente.

        ¿PASOS?
        1. Obtener cliente por ID.
        2. Si no existe, retornar None (no error, solo ausencia).
        3. Si intenta cambiar RFC, verificar que es único (excepto el suyo).
        4. Aplicar cambios a los atributos.
        5. Validar el cliente modificado (FAIL-FAST si datos inválidos).
        6. Actualizar fecha_modificacion.
        7. Persistir cambios a archivo.

        ¿POR QUÉ VERIFICAR RFC ANTES?
        - Si cambias RFC de cliente 1 a RFC de cliente 2, violarías constrainto.
        - Pero permitir que un cliente mantenga su propio RFC.
        - Validar ANTES de aplicar: si falla, cliente no se modifica (transaccionalidad).

        ¿POR QUÉ VALIDAR DESPUÉS?
        - El usuario podría cambiar RFC a algo malformado ("123").
        - Cliente.validar() verifica formato de RFC, email, etc.
        - INTEGRIDAD DE DATOS: No permitir estados inválidos.

        ¿VALIDACIÓN EN DOS PUNTOS?
        - RFC ÚNICO: Verificado en nivel de servicio (regla de negocio global).
        - FORMATO RFC: Verificado en nivel de modelo (validación de estructura).
        - Ejemplo: RFC="ABC123456XYZ" en el sistema, alguien intenta cambiar a "ABC123456XYZ"
          (su propio RFC): Pasa first check (es único, el cliente actual).
          Pasa second check (formato válido).

        Args:
            cliente_id (str): ID del cliente a modificar.
            datos (Dict[str, Any]): Diccionario con los datos a actualizar.
                                   Ejemplo: {"nombre": "Juan Nueva", "email": "nuevo@e.com"}
                                   SOLO incluir campos a cambiar, otros quedan igual.

        Returns:
            Optional[Cliente]: El cliente modificado con los cambios aplicados.
                             Retorna None si el cliente con cliente_id no existe.

        Raises:
            ValueError: Si los datos no son válidos o violan reglas de negocio.

        Ejemplo:
            # Cliente original
            cliente = Cliente("Juan", "ABC123456XYZ", "j@e.com", "555123")
            servicio.agregar_cliente(cliente)

            # Modificar
            datos_nuevos = {"email": "nuevo@e.com", "telefono": "5555555555"}
            cliente_mod = servicio.modificar_cliente(cliente.id, datos_nuevos)

            print(cliente_mod.email)  # "nuevo@e.com"
            print(cliente_mod.telefono)  # "5555555555"
            print(cliente_mod.nombre)  # "Juan" (sin cambios)
        """
        # PASO 1: Obtener cliente existente
        cliente = self.obtener_por_id(cliente_id)

        # PASO 2: Si no existe, retornar None (patrón de ausencia)
        if not cliente:
            return None

        # PASO 3: Si intenta cambiar RFC, validar unicidad (excepto su propio RFC)
        if "rfc" in datos:
            otro_cliente = self.obtener_por_rfc(datos["rfc"])
            # Permite si no existe OTRO cliente con ese RFC,
            # o si OTRO es el mismo cliente (mismo ID)
            if otro_cliente and otro_cliente.id != cliente_id:
                raise ValueError(
                    f"Ya existe otro cliente con RFC {datos['rfc']}"
                )

        # PASO 4: Aplicar cambios (solo los campos especificados)
        # Este patrón permite actualizaciones parciales (no todos los campos)
        if "nombre" in datos:
            cliente.nombre = datos["nombre"]
        if "rfc" in datos:
            cliente.rfc = datos["rfc"]
        if "email" in datos:
            cliente.email = datos["email"]
        if "telefono" in datos:
            cliente.telefono = datos["telefono"]
        if "estado" in datos:
            cliente.estado = datos["estado"]

        # PASO 5: Validar cliente modificado (FAIL-FAST si datos inválidos)
        # Si validar() lanza excepción, cliente NO se guarda, cambios perdidos en memoria
        cliente.validar()

        # PASO 6: Actualizar fecha de última modificación
        cliente.actualizar_fecha_modificacion()

        # PASO 7: Persistir cambios a archivo
        self.guardar_clientes()

        return cliente

    def eliminar_cliente(self, cliente_id: str) -> bool:
        """
        Elimina un cliente por su ID.

        ¿PATRÓN DE RETORNO?
        - Retorna bool en lugar de None.
        - True: Cliente fue encontrado y eliminado.
        - False: Cliente no existía (no hubo error, solo ausencia).
        - Permite al llamador saber si realmente se eliminó algo.

        ¿PASOS?
        1. Obtener cliente por ID.
        2. Si no existe, retornar False.
        3. Si existe, eliminarlo de la lista en memoria.
        4. Persistir cambios a archivo.
        5. Retornar True.

        Args:
            cliente_id (str): ID del cliente a eliminar.

        Returns:
            bool: True si se eliminó, False si no se encontró.

        Ejemplo:
            cliente = Cliente("Juan", "ABC123456XYZ", "j@e.com", "555123")
            servicio.agregar_cliente(cliente)

            resultado = servicio.eliminar_cliente(cliente.id)
            print(resultado)  # True

            resultado = servicio.eliminar_cliente("999")
            print(resultado)  # False (no existía)
        """
        # Obtener cliente existente
        cliente = self.obtener_por_id(cliente_id)

        # Si no existe, retornar False (no error)
        if not cliente:
            return False

        # Eliminar de la lista en memoria
        self.clientes.remove(cliente)

        # Persistir cambios a archivo
        self.guardar_clientes()

        return True

    def obtener_clientes_activos(self) -> List[Cliente]:
        """
        Obtiene todos los clientes con estado activo.

        Returns:
            List[Cliente]: Lista de clientes activos.
        """
        return [
            cliente for cliente in self.clientes
            if cliente.estado == "activo"
        ]

    def contar_clientes(self) -> int:
        """
        Cuenta el total de clientes.

        Returns:
            int: Número total de clientes.
        """
        return len(self.clientes)

    def limpiar_archivo(self) -> None:
        """Limpia el archivo de clientes (elimina todos los datos)."""
        self.clientes = []
        self.guardar_clientes()

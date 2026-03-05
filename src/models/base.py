"""
Módulo de clase base para todas las entidades del sistema.

Este módulo contiene la clase abstracta EntidadBase que proporciona
funcionamiento común a todas las entidades del dominio.

CONCEPTOS CLAVE:
- ABC (Abstract Base Class): Permite definir clases que NO pueden ser instanciadas
  directamente, solo sus subclases pueden serlo. Esto es útil para definir contratos
  que las subclases DEBEN cumplir.
- Métodos abstractos: Fuerzan a las subclases a implementarlos. Sin su implementación,
  la subclase también será abstracta y no podrá instanciarse.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, Any


class EntidadBase(ABC):
    """
    Clase base abstracta para todas las entidades del sistema.

    Proporciona atributos y métodos comunes como ID, fechas de creación
    y modificación, y serialización a diccionario.

    ¿POR QUÉ USAMOS ABC?
    - Establece un contrato: Cualquier clase que herede de EntidadBase DEBE implementar
      los métodos abstractos (validar y a_diccionario).
    - Previene instanciación incorrecta: No podemos hacer EntidadBase() directamente,
      solo podemos crear instancias de subclases concretas como Cliente.
    - Define la interfaz común: Cualquier código que trabaje con EntidadBase sabe
      que puede llamar a validar() y a_diccionario() en todas las subclases.
    - Análogo del mundo real: Es como tener un "contrato" que dice "toda entidad en
      el sistema debe poder validarse y convertirse a diccionario".

    Attributes:
        id (str): Identificador único de la entidad (secuencial).
        fecha_creacion (datetime): Fecha y hora de creación (para auditoría).
        fecha_modificacion (datetime): Fecha y hora de última modificación (para rastreo de cambios).
    """

    # CONTADOR DE IDS A NIVEL DE CLASE (clase, no instancia)
    # Explicación: _contador_id es una variable compartida por TODAS las instancias.
    # Cada vez que se crea una entidad, incrementamos este contador para obtener un ID único.
    # Iniciamos en 0 para que el primer ID sea 1.
    # NOTA: El prefijo _ indica que es "privado" (convención, Python no lo fuerza).
    _contador_id = 0

    def __init__(self):
        """
        Inicializa una nueva entidad base.

        PASOS QUE OCURREN:
        1. Incrementa el contador de IDs (suma 1 al contador de clase)
        2. Asigna el nuevo ID a esta instancia (como string)
        3. Registra la fecha/hora actual como fecha de creación
        4. Registra la fecha/hora actual como fecha de modificación

        ¿POR QUÉ IDS SECUENCIALES EN VEZ DE UUIDs?
        - Secuenciales (1, 2, 3...): Más simple, fácil de leer/debuggear, menor espacio.
        - UUIDs (alfanuméricos largos): Únicos globalmente, mejor para sistemas distribuidos.
        - En esta solución usamos secuenciales por simplicidad educativa.
        - En producción, podrías cambiar a UUID si necesitas escalabilidad distribuida.

        ¿POR QUÉ RASTREAR FECHAS?
        - fecha_creacion: Auditoría (¿cuándo se registró este cliente?).
        - fecha_modificacion: Rastreo de cambios (¿cuándo fue actualizado?).
        - Útil para compliance regulatorio (cumplimiento normativo).
        - Permite detección de fraude (cambios sospechosos).
        """
        # Incrementar el contador compartido y asignar ID único a esta instancia
        EntidadBase._contador_id += 1
        self.id = str(EntidadBase._contador_id)  # Convertir a string para consistencia

        # Registrar el momento exacto de creación
        self.fecha_creacion = datetime.now()

        # Inicialmente, fecha_modificacion es igual a fecha_creacion
        # Se actualizará solo cuando se modifique la entidad
        self.fecha_modificacion = datetime.now()

    @abstractmethod
    def validar(self) -> bool:
        """
        Valida los datos de la entidad.

        ¿POR QUÉ ES ABSTRACTO?
        - Cada tipo de entidad tiene reglas de validación diferentes.
        - Cliente necesita validar RFC, nombre, email, etc.
        - No podemos crear una validación genérica en la clase base.
        - Forzamos a las subclases a implementar SU PROPIA validación.

        ¿PATRÓN "FAIL-FAST"?
        - Las subclases deben lanzar ValueError INMEDIATAMENTE si hay datos inválidos.
        - No es mejor permitir datos inválidos y fallar después.
        - Prevenir datos malos desde el inicio evita bugs en cascada.

        Debe ser implementado por las subclases para proporcionar
        validación específica de cada entidad.

        Returns:
            bool: True si la entidad es válida, False en caso contrario.

        Raises:
            ValueError: Si la entidad no es válida (la subclase decide cuándo).
        """
        pass  # Las subclases implementarán esto

    @abstractmethod
    def a_diccionario(self) -> Dict[str, Any]:
        """
        Convierte la entidad a un diccionario.

        ¿POR QUÉ ESTE MÉTODO?
        - Los diccionarios se pueden serializar a JSON fácilmente.
        - Permite persistencia (guardar datos en archivos).
        - Permite intercambio de datos con APIs/servicios.
        - Facilita la serialización de objetos Python a formato transportable.

        ¿DICT[STR, ANY]?
        - Dict: Es un diccionario (clave-valor).
        - str: Las claves siempre son strings (ej: "nombre", "rfc").
        - Any: Los valores pueden ser cualquier tipo (str, int, datetime, etc).
        - Estos son TYPE HINTS (sugerencias de tipo, Python no los fuerza).

        Debe ser implementado por las subclases para proporcionar
        una representación en diccionario específica de cada entidad.

        Returns:
            Dict[str, Any]: Representación en diccionario de la entidad.
        """
        pass  # Las subclases implementarán esto

    def actualizar_fecha_modificacion(self) -> None:
        """
        Actualiza la fecha de modificación al momento actual.

        ¿CUÁNDO USARLO?
        - Después de modificar cualquier atributo de la entidad.
        - Permite saber exactamente cuándo fue cambiada.
        - En ClienteService.modificar_cliente(), se llama después de cambios.

        ¿POR QUÉ NO ES AUTOMÁTICO?
        - Python no detecta automáticamente cambios en atributos.
        - Podrías usar __setattr__, pero es complejo.
        - Es más simple que el servicio llame explícitamente a este método.
        """
        self.fecha_modificacion = datetime.now()

    def __str__(self) -> str:
        """
        Representación en cadena de la entidad (legible para humanos).

        ¿POR QUÉ __STR__?
        - Se invoca cuando haces print(cliente) o str(cliente).
        - Debe ser legible y útil para debugging.
        - Ejemplo: "Cliente(id=1)"

        ¿DIFERENCIA __STR__ vs __REPR__?
        - __str__: Para usuarios (legible, conciso). Ejemplo: "Cliente(id=1)"
        - __repr__: Para desarrolladores (detallado, útil para debugging).
        - Aquí usamos la misma implementación para ambos (más simple).

        Returns:
            str: Representación en cadena de la entidad.
        """
        # Usamos self.__class__.__name__ para obtener el nombre de la clase actual.
        # Esto permite que subclases como Cliente muestren "Cliente" automáticamente.
        return f"{self.__class__.__name__}(id={self.id})"

    def __repr__(self) -> str:
        """
        Representación técnica de la entidad (para desarrolladores).

        ¿POR QUÉ __REPR__?
        - Se invoca cuando evalúas la entidad en el intérprete.
        - Útil para logging y debugging.
        - Idealmente, debería poder copiar-pegar el output para recrear el objeto.
        - Aquí simplemente delegamos a __str__ para consistencia.

        Returns:
            str: Representación técnica de la entidad.
        """
        return self.__str__()

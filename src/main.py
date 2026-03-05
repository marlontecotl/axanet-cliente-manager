"""
Módulo principal de la aplicación.

Interfaz de línea de comandos (CLI) para la gestión de clientes AXANET.
Proporciona un menú interactivo para realizar operaciones CRUD.

ARQUITECTURA:
- SEPARACIÓN DE CAPAS:
  - Modelo (Cliente): Datos y validación de datos.
  - Servicio (ClienteService): Persistencia y lógica CRUD.
  - Validadores: Funciones de validación reutilizables.
  - UI/CLI (AplicacionGestionClientes): Presentación e interacción con usuario.

- PATRÓN MVC-LIKE:
  - Model: Cliente, ClienteService.
  - View: AplicacionGestionClientes (display, input).
  - Control: Métodos que orquestan operaciones (agregar, modificar, eliminar).

- DEVOPS:
  - Fácil de testear (capas desacopladas).
  - Fácil de reemplazar UI (CLI → Web API con FastAPI).
  - Fácil de documentar (responsabilidades claras).
"""

import os
import sys
from typing import Optional, Dict
from models.cliente import Cliente
from services.cliente_service import ClienteService
from validators.validators import (
    validar_nombre, validar_rfc, validar_email,
    validar_telefono, validar_estado
)


class AplicacionGestionClientes:
    """
    Aplicación de gestión de clientes con interfaz CLI.

    Proporciona un menú interactivo para agregar, listar, buscar,
    modificar y eliminar clientes.

    ¿POR QUÉ SEPARAR UI DE LÓGICA?
    - Principio SRP: UI solo maneja presentación, no lógica de datos.
    - Testabilidad: Podemos testear ClienteService sin UI.
    - Reusabilidad: Mismo servicio puede usarse en Web UI, API REST, etc.
    - Mantenimiento: Cambios en CLI no afectan al servicio.

    ¿CLI (COMMAND LINE INTERFACE)?
    - Interfaz de línea de comandos: Usuario interactúa por teclado/terminal.
    - Alternativas: Web UI (Flask/FastAPI), Mobile app, API REST.
    - CLI es excelente para MVPs (Minimum Viable Product) y prototipos.

    Attributes:
        servicio (ClienteService): Servicio de gestión de clientes.
                                  Contiene toda la lógica de CRUD y persistencia.
    """

    def __init__(self):
        """
        Inicializa la aplicación.

        ¿PASOS?
        1. Crear instancia de ClienteService.
        2. Servicio automáticamente carga datos persistidos (desde JSON).
        3. Aplicación lista para ejecutar.

        RESPONSABILIDADES:
        - ClienteService maneja datos (CRUD, persistencia).
        - AplicacionGestionClientes maneja UI (mostrar menú, solicitar input).
        """
        self.servicio = ClienteService()

    def limpiar_pantalla(self) -> None:
        """Limpia la pantalla de la consola."""
        os.system('clear' if os.name == 'posix' else 'cls')

    def mostrar_encabezado(self) -> None:
        """Muestra el encabezado de la aplicación."""
        self.limpiar_pantalla()
        print("=" * 60)
        print("  SISTEMA DE GESTIÓN DE CLIENTES - AXANET")
        print("=" * 60)

    def mostrar_menu_principal(self) -> None:
        """Muestra el menú principal."""
        print("\n¿Qué deseas hacer?")
        print("-" * 60)
        print("1. Agregar cliente")
        print("2. Listar clientes")
        print("3. Buscar cliente")
        print("4. Modificar cliente")
        print("5. Eliminar cliente")
        print("6. Salir")
        print("-" * 60)

    def obtener_opcion(self) -> str:
        """
        Obtiene la opción del usuario.

        Returns:
            str: Opción seleccionada por el usuario.
        """
        return input("Selecciona una opción (1-6): ").strip()

    def solicitar_datos_cliente(self) -> Optional[Cliente]:
        """
        Solicita al usuario los datos de un nuevo cliente.

        Returns:
            Optional[Cliente]: Objeto Cliente creado o None si hay error.
        """
        print("\n" + "-" * 60)
        print("INGRESA LOS DATOS DEL CLIENTE")
        print("-" * 60)

        try:
            nombre = input("Nombre: ").strip()
            if not validar_nombre(nombre):
                print("Error: El nombre debe tener al menos 3 caracteres "
                      "y solo contener letras.")
                return None

            rfc = input("RFC: ").strip().upper()
            if not validar_rfc(rfc):
                print("Error: El RFC debe tener al menos 12 caracteres "
                      "válidos (ej: ABC123456XYZ).")
                return None

            email = input("Email: ").strip()
            if not validar_email(email):
                print("Error: El email no tiene un formato válido.")
                return None

            telefono = input("Teléfono: ").strip()
            if not validar_telefono(telefono):
                print("Error: El teléfono debe tener al menos 10 dígitos.")
                return None

            cliente = Cliente(
                nombre=nombre,
                rfc=rfc,
                email=email,
                telefono=telefono,
                estado="activo"
            )

            return cliente

        except ValueError as e:
            print(f"Error de validación: {str(e)}")
            return None

    def agregar_cliente(self) -> None:
        """Agrega un nuevo cliente."""
        self.mostrar_encabezado()

        cliente = self.solicitar_datos_cliente()

        if cliente is None:
            input("\nPresiona Enter para continuar...")
            return

        try:
            self.servicio.agregar_cliente(cliente)
            print("\n✓ Cliente agregado exitosamente.")
            print(f"  ID: {cliente.id}")
            print(f"  Nombre: {cliente.nombre}")
            print(f"  RFC: {cliente.rfc}")
        except ValueError as e:
            print(f"\n✗ Error: {str(e)}")

        input("\nPresiona Enter para continuar...")

    def listar_clientes(self) -> None:
        """Lista todos los clientes."""
        self.mostrar_encabezado()

        clientes = self.servicio.obtener_todos()

        if not clientes:
            print("\nNo hay clientes registrados.")
        else:
            print(f"\nTotal de clientes: {len(clientes)}")
            print("-" * 60)

            for cliente in clientes:
                self._mostrar_cliente(cliente)

        input("\nPresiona Enter para continuar...")

    def _mostrar_cliente(self, cliente: Cliente) -> None:
        """
        Muestra los datos de un cliente formateado.

        ¿POR QUÉ MÉTODO PRIVADO (PREFIJO _)?
        - Indica que NO es para llamar externamente.
        - Solo se usa internamente en AplicacionGestionClientes.
        - Reduce "ruido" de métodos públicos.
        - Convención Python (no fuerza, solo indicación).

        ¿FORMATTING?
        - Presenta datos de forma legible al usuario.
        - Incluye ID, nombre, RFC, email, teléfono, estado, fecha.
        - Línea separadora para claridad visual.

        Args:
            cliente (Cliente): Cliente a mostrar.
        """
        # Mostrar cada atributo en una línea
        print(f"\nID: {cliente.id}")
        print(f"Nombre: {cliente.nombre}")
        print(f"RFC: {cliente.rfc}")
        print(f"Email: {cliente.email}")
        print(f"Teléfono: {cliente.telefono}")
        print(f"Estado: {cliente.estado}")
        # Convertir datetime a formato legible (YYYY-MM-DD HH:MM:SS)
        print(f"Creado: {cliente.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 60)

    def buscar_cliente(self) -> None:
        """Busca un cliente."""
        self.mostrar_encabezado()

        print("\nOpciones de búsqueda:")
        print("1. Por ID")
        print("2. Por RFC")
        print("3. Por nombre")

        opcion = input("Selecciona opción (1-3): ").strip()

        cliente = None
        clientes = []

        try:
            if opcion == "1":
                cliente_id = input("Ingresa el ID: ").strip()
                cliente = self.servicio.obtener_por_id(cliente_id)

            elif opcion == "2":
                rfc = input("Ingresa el RFC: ").strip()
                cliente = self.servicio.obtener_por_rfc(rfc)

            elif opcion == "3":
                nombre = input("Ingresa el nombre (o parte del nombre): ").strip()
                clientes = self.servicio.obtener_por_nombre(nombre)

            else:
                print("Opción inválida.")
                input("\nPresiona Enter para continuar...")
                return

            if cliente:
                print("\n✓ Cliente encontrado:")
                self._mostrar_cliente(cliente)
            elif clientes:
                print(f"\n✓ Se encontraron {len(clientes)} cliente(s):")
                for c in clientes:
                    self._mostrar_cliente(c)
            else:
                print("\n✗ No se encontraron resultados.")

        except Exception as e:
            print(f"Error en la búsqueda: {str(e)}")

        input("\nPresiona Enter para continuar...")

    def _solicitar_datos_modificacion(self) -> Dict[str, str]:
        """
        Solicita los datos a modificar de un cliente.

        Returns:
            Dict[str, str]: Diccionario con los datos a actualizar.
        """
        datos = {}

        self._actualizar_campo(datos, "nombre", "Nuevo nombre: ",
                               validar_nombre)
        self._actualizar_campo(datos, "rfc", "Nuevo RFC: ",
                               validar_rfc, convertir=str.upper)
        self._actualizar_campo(datos, "email", "Nuevo email: ",
                               validar_email)
        self._actualizar_campo(datos, "telefono", "Nuevo teléfono: ",
                               validar_telefono)

        print("\nEstado (activo/inactivo):")
        self._actualizar_campo(datos, "estado", "Nuevo estado: ",
                               validar_estado, convertir=str.lower)

        return datos

    def _actualizar_campo(self, datos: Dict, campo: str, prompt: str,
                          validador, convertir=str.strip) -> None:
        """
        Solicita y valida un campo para modificar.

        Args:
            datos (Dict): Diccionario donde almacenar el dato.
            campo (str): Nombre del campo.
            prompt (str): Mensaje a mostrar.
            validador: Función de validación.
            convertir: Función de conversión (por defecto strip).
        """
        valor = input(prompt).strip()
        valor = convertir(valor) if valor else ""

        if valor and validador(valor):
            datos[campo] = valor
        elif valor:
            print(f"✗ {campo.capitalize()} inválido. No se modificará.")

    def modificar_cliente(self) -> None:
        """Modifica un cliente existente."""
        self.mostrar_encabezado()

        cliente_id = input("Ingresa el ID del cliente a modificar: ").strip()
        cliente = self.servicio.obtener_por_id(cliente_id)

        if not cliente:
            print("✗ No se encontró un cliente con ese ID.")
            input("\nPresiona Enter para continuar...")
            return

        print("\n✓ Cliente encontrado:")
        self._mostrar_cliente(cliente)

        print("\nDatos a modificar (deja en blanco para no cambiar):")
        print("-" * 60)

        datos_actualizados = self._solicitar_datos_modificacion()

        if not datos_actualizados:
            print("\n✗ No se proporcionaron datos para actualizar.")
            input("\nPresiona Enter para continuar...")
            return

        try:
            cliente_actualizado = self.servicio.modificar_cliente(
                cliente_id, datos_actualizados
            )
            if cliente_actualizado:
                print("\n✓ Cliente modificado exitosamente:")
                self._mostrar_cliente(cliente_actualizado)
            else:
                print("✗ Error al modificar el cliente.")
        except ValueError as e:
            print(f"\n✗ Error: {str(e)}")

        input("\nPresiona Enter para continuar...")

    def eliminar_cliente(self) -> None:
        """Elimina un cliente."""
        self.mostrar_encabezado()

        cliente_id = input("Ingresa el ID del cliente a eliminar: ").strip()
        cliente = self.servicio.obtener_por_id(cliente_id)

        if not cliente:
            print("✗ No se encontró un cliente con ese ID.")
            input("\nPresiona Enter para continuar...")
            return

        print("\n✓ Cliente a eliminar:")
        self._mostrar_cliente(cliente)

        confirmacion = input(
            "¿Estás seguro de que deseas eliminar este cliente? (s/n): "
        ).strip().lower()

        if confirmacion == "s":
            if self.servicio.eliminar_cliente(cliente_id):
                print("\n✓ Cliente eliminado exitosamente.")
            else:
                print("✗ Error al eliminar el cliente.")
        else:
            print("\n✗ Operación cancelada.")

        input("\nPresiona Enter para continuar...")

    def ejecutar(self) -> None:
        """
        Ejecuta el bucle principal de la aplicación.

        ¿EVENT LOOP?
        - while True: Bucle infinito hasta que usuario selecciona "Salir".
        - Patrón común en UI (CLI, GUI, juegos, servidores).
        - Cada iteración: mostrar menú, obtener opción, ejecutar acción.

        ¿POR QUÉ WHILE TRUE?
        - El programa debe mantener la UI activa.
        - Sin el bucle, saldría después del primer comando.
        - Con el bucle, el usuario puede hacer múltiples operaciones.

        ¿FLUJO?
        1. Mostrar encabezado (pantalla limpia, título).
        2. Mostrar opciones de menú.
        3. Solicitar opción al usuario.
        4. Ejecutar acción basada en opción.
        5. Volver al inicio del bucle (paso 1).

        ¿ALTERNATIVA: MÁQUINA DE ESTADOS?
        - Podrías implementar como State Machine.
        - Para aplicación simple, while True es suficiente.
        - En aplicaciones complejas, patrones más sofisticados son mejores.
        """
        # BUCLE PRINCIPAL (event loop)
        while True:
            # Mostrar encabezado (limpia pantalla, muestra título)
            self.mostrar_encabezado()

            # Mostrar opciones de menú
            self.mostrar_menu_principal()

            # Obtener opción del usuario
            opcion = self.obtener_opcion()

            # DISPATCHER: Ejecutar acción basada en opción
            if opcion == "1":
                self.agregar_cliente()
            elif opcion == "2":
                self.listar_clientes()
            elif opcion == "3":
                self.buscar_cliente()
            elif opcion == "4":
                self.modificar_cliente()
            elif opcion == "5":
                self.eliminar_cliente()
            elif opcion == "6":
                # Salir de la aplicación
                self.mostrar_encabezado()
                print("\n¡Hasta luego!")
                sys.exit(0)  # Exit code 0 = éxito
            else:
                # Opción no reconocida
                print("\n✗ Opción inválida. Intenta de nuevo.")
                input("\nPresiona Enter para continuar...")


def main():
    """
    Punto de entrada principal de la aplicación.

    ¿MANEJO DE EXCEPCIONES?
    - try/except: Captura errores no esperados.
    - KeyboardInterrupt: Usuario presiona Ctrl+C (salida limpia).
    - Exception genérica: Cualquier otro error fatal.

    ¿EXIT CODES?
    - sys.exit(0): Éxito, programa finalizó correctamente.
    - sys.exit(1): Error, algo salió mal.
    - En DevOps/CI-CD, estos códigos indican al sistema si falló o no.

    ¿MANEJO DE CTRL+C?
    - Sin try/except: Ctrl+C mostraría traceback (feo).
    - Con KeyboardInterrupt: Despedida amable "Aplicación interrumpida...".
    - Mejor experiencia de usuario.

    ANALOGÍA:
    - main() es el "director" de la orquesta.
    - Coordina creación y ejecución de la aplicación.
    - Maneja excepciones para salida limpia sin importar qué suceda.
    """
    try:
        # Crear instancia de la aplicación
        app = AplicacionGestionClientes()

        # Ejecutar el bucle principal (event loop)
        app.ejecutar()

    except KeyboardInterrupt:
        # Usuario presionó Ctrl+C (interrupción por teclado)
        # Salida amable en lugar de traceback
        print("\n\n✗ Aplicación interrumpida por el usuario.")
        sys.exit(0)  # Exit code 0 = salida normal (por usuario)

    except Exception as e:
        # Cualquier otro error no esperado
        # Mostrar mensaje de error y exit code 1
        print(f"\n✗ Error fatal: {str(e)}")
        sys.exit(1)  # Exit code 1 = error


# PUNTO DE ENTRADA
# ¿POR QUÉ if __name__ == "__main__"?
# - __name__ es "main" cuando ejecutas el script directamente.
# - __name__ es "main" si importas el módulo desde otro (cuando se ejecuta import).
# - Esto permite que el módulo sea reutilizable sin ejecutar main() al importar.
# - BUENA PRÁCTICA: Siempre usa if __name__ == "__main__" para entry point.
#
# DEVOPS:
# - En CI/CD, se ejecuta python src/main.py.
# - Exit code indica si tuvo éxito (0) o error (1).
# - El pipeline puede actuar basado en el exit code.
if __name__ == "__main__":
    main()

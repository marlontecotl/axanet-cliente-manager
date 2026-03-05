# Sistema de Gestión de Clientes AXANET

Sistema de gestión de clientes desarrollado en Python utilizando programación orientada a objetos (OOP) con arquitectura de servicios. Esta aplicación implementa operaciones CRUD completas para la administración de clientes de AXANET.

## Descripción del Proyecto

Esta es una solución completa para la **Actividad II** del curso DevOps que demuestra:

- **Programación en Python**: Aplicación robusta con OOP, validación de datos y manejo de excepciones
- **Persistencia de Datos**: Almacenamiento en archivos JSON
- **Pruebas Unitarias**: Cobertura >70% con pytest
- **Control de Versiones**: Estructura GitFlow con ramas (main, develop, feature/*, release/*)
- **Automatización CI/CD**: 3 workflows GitHub Actions (Testing, Lint, Deploy)
- **Documentación**: Código completamente documentado con docstrings en español

## Estructura del Proyecto

```
Actividad_II_Ejemplo/
├── README.md                          # Este archivo
├── requirements.txt                   # Dependencias del proyecto
├── .gitignore                         # Archivos ignorados por Git
│
├── src/                              # Código fuente de la aplicación
│   ├── __init__.py                   # Inicializador del paquete
│   ├── main.py                       # Interfaz CLI principal
│   │
│   ├── models/                       # Modelos de datos
│   │   ├── __init__.py
│   │   ├── base.py                   # Clase abstracta EntidadBase
│   │   └── cliente.py                # Clase Cliente (herencia)
│   │
│   ├── services/                     # Servicios de negocio
│   │   ├── __init__.py
│   │   └── cliente_service.py        # Servicio CRUD de Cliente
│   │
│   └── validators/                   # Funciones de validación
│       ├── __init__.py
│       └── validators.py             # RFC, email, teléfono, etc.
│
├── tests/                            # Pruebas unitarias (71% cobertura)
│   ├── __init__.py
│   ├── test_models.py                # Pruebas de modelos
│   ├── test_services.py              # Pruebas de servicios
│   └── test_validators.py            # Pruebas de validadores
│
├── data/                             # Almacenamiento de datos JSON
│   └── .gitkeep                      # Marcador de directorio
│
└── .github/
    └── workflows/                    # GitHub Actions Workflows
        ├── testing.yml               # Workflow de pruebas
        ├── lint.yml                  # Workflow de control de calidad
        └── deploy.yml                # Workflow de deployment
```

## Características Principales

### 1. Programación Orientada a Objetos (OOP)

- **Herencia**: `Cliente` hereda de `EntidadBase` (clase abstracta)
- **Encapsulación**: Atributos privados y métodos públicos bien definidos
- **Polimorfismo**: Métodos abstractos implementados en subclases
- **Validación**: Métodos `validar()` con manejo de excepciones

### 2. Modelos de Datos

#### EntidadBase (Clase Abstracta)
```python
- Proporciona ID único secuencial
- Fechas de creación y modificación
- Métodos abstractos: validar(), a_diccionario()
- Actualización automática de fechas
```

#### Cliente (Hereda de EntidadBase)
```python
Atributos:
- nombre: Nombre del cliente (validación: mín 3 caracteres, sin números)
- rfc: Registro Federal de Contribuyentes (patrón RFC válido)
- email: Correo electrónico (validación de formato)
- telefono: Número de teléfono (mín 10 dígitos)
- estado: "activo" o "inactivo"

Métodos:
- validar(): Valida todos los campos
- a_diccionario(): Serializa a diccionario
- desde_diccionario(): Crea instancia desde diccionario
```

### 3. Servicio ClienteService

Implementa operaciones CRUD completas:

```python
# Crear
agregar_cliente(cliente: Cliente) -> None

# Leer
obtener_todos() -> List[Cliente]
obtener_por_id(id: str) -> Optional[Cliente]
obtener_por_rfc(rfc: str) -> Optional[Cliente]
obtener_por_nombre(nombre: str) -> List[Cliente]
obtener_clientes_activos() -> List[Cliente]

# Actualizar
modificar_cliente(id: str, datos: Dict) -> Optional[Cliente]

# Eliminar
eliminar_cliente(id: str) -> bool

# Utilidades
contar_clientes() -> int
guardar_clientes() -> None
cargar_clientes() -> None
```

### 4. Validadores

Módulo completo de validación con patrones regex:

- `validar_nombre()`: Mínimo 3 caracteres, solo letras y espacios
- `validar_rfc()`: Formato RFC mexicano (12-13 caracteres)
- `validar_email()`: Validación de dirección de correo
- `validar_telefono()`: Mínimo 10 dígitos con formatos variados
- `validar_estado()`: "activo" o "inactivo"

### 5. Interfaz de Línea de Comandos (CLI)

Menú interactivo con las siguientes opciones:

```
1. Agregar cliente
2. Listar clientes
3. Buscar cliente (por ID, RFC o nombre)
4. Modificar cliente
5. Eliminar cliente
6. Salir
```

### 6. Persistencia de Datos

- Almacenamiento en archivos JSON (`data/clientes.json`)
- Carga automática al iniciar la aplicación
- Guardado automático después de cada operación
- Serialización/deserialización completa

### 7. Pruebas Unitarias

**Cobertura: 71%** (supera el requisito mínimo de 70%)

Módulos de prueba:
- `test_validators.py`: 16 pruebas (validadores)
- `test_models.py`: 12 pruebas (modelos Cliente y EntidadBase)
- `test_services.py`: 18 pruebas (operaciones CRUD)

Total: **46 pruebas** con pytest

### 8. GitHub Actions Workflows

#### 1. **testing.yml** - Pruebas Automáticas
- Se ejecuta en push y pull requests
- Prueba en Python 3.9, 3.10, 3.11
- Ejecuta pytest con cobertura
- Sube reportes a Codecov

#### 2. **lint.yml** - Control de Calidad
- Análisis con flake8
- Verificación de docstrings
- Verificación de complejidad ciclomática
- Validación de líneas máximo 127 caracteres

#### 3. **deploy.yml** - Deployment
- Se ejecuta solo en push a main
- Ejecuta tests completos
- Verifica código
- Crea artefacto de build
- Sube artifact a GitHub Actions

### 9. Estructura GitFlow

```
main          <- Código en producción (releases)
├── release/* <- Ramas de release (con versionado)
│
develop       <- Rama de desarrollo
├── feature/* <- Nuevas funcionalidades
```

## Requisitos

- Python 3.9+
- pip (gestor de paquetes)
- Git

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/usuario/axanet-cliente-manager.git
cd axanet-cliente-manager
```

### 2. Crear entorno virtual (recomendado)

```bash
# En Linux/macOS
python3 -m venv venv
source venv/bin/activate

# En Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

## Uso

### Ejecutar la Aplicación

```bash
python src/main.py
```

Se abrirá un menú interactivo:

```
============================================================
  SISTEMA DE GESTIÓN DE CLIENTES - AXANET
============================================================

¿Qué deseas hacer?
------------------------------------------------------------
1. Agregar cliente
2. Listar clientes
3. Buscar cliente
4. Modificar cliente
5. Eliminar cliente
6. Salir
------------------------------------------------------------
```

### Ejemplo de Uso

```bash
# 1. Agregar cliente
Selecciona una opción (1-6): 1

INGRESA LOS DATOS DEL CLIENTE
Nombre: Juan García López
RFC: ABC123456XYZ
Email: juan@ejemplo.com
Teléfono: 5551234567

✓ Cliente agregado exitosamente.
  ID: 1
  Nombre: Juan García López
  RFC: ABC123456XYZ

# 2. Listar clientes
Selecciona una opción (1-6): 2

Total de clientes: 1
------------------------------------------------------------

ID: 1
Nombre: Juan García López
RFC: ABC123456XYZ
Email: juan@ejemplo.com
Teléfono: 5551234567
Estado: activo
Creado: 2024-03-04 15:30:45
```

### Ejecutar Pruebas

```bash
# Ejecutar todas las pruebas
pytest tests/ -v

# Ejecutar con cobertura
pytest tests/ --cov=src --cov-report=html

# Ejecutar un archivo específico
pytest tests/test_models.py -v

# Ejecutar una prueba específica
pytest tests/test_models.py::TestCliente::test_crear_cliente_valido -v
```

### Verificar Calidad de Código

```bash
# Ejecutar flake8
flake8 src tests --max-line-length=127

# Ver complejidad ciclomática
flake8 src tests --max-complexity=10
```

## Datos de Ejemplo

El sistema incluye validación de datos. Ejemplos válidos:

```python
# Cliente válido
cliente = Cliente(
    nombre="María González López",
    rfc="XYZ987654ABC",
    email="maria@ejemplo.com",
    telefono="5559876543"
)

# Los siguientes causarán error:
# - Nombre: "Jo" (muy corto)
# - RFC: "123" (formato inválido)
# - Email: "email_invalido" (sin @)
# - Teléfono: "123" (menos de 10 dígitos)
```

## Entregables de la Actividad

### 1. Programa Python (30 pts) ✓
- [x] OOP con clases, herencia, validación
- [x] Operaciones CRUD completas
- [x] Manejo de excepciones
- [x] Persistencia JSON
- [x] 46 pruebas unitarias (71% cobertura)
- [x] Documentación con docstrings en español

### 2. GitHub Repository (30 pts) ✓
- [x] Repositorio público en GitHub
- [x] Estructura GitFlow (main, develop, feature/*, release/*)
- [x] 3 workflows GitHub Actions:
  - [x] testing.yml (pruebas automáticas)
  - [x] lint.yml (verificación de calidad)
  - [x] deploy.yml (deployment)

### 3. Video (20 pts) - Por grabar
- Presentación del proyecto
- Demostración de funcionalidades
- Ejecución de pruebas y workflows
- Explicación de arquitectura

### 4. Documento Word (20 pts) - Por crear
- Explicación técnica de la solución
- Diagrama de arquitectura
- Manual de usuario
- Conclusiones

## Tecnologías Utilizadas

- **Python 3.9+**: Lenguaje de programación
- **pytest**: Framework de pruebas unitarias
- **pytest-cov**: Cobertura de pruebas
- **flake8**: Verificación de estilo de código
- **JSON**: Almacenamiento de datos
- **GitHub Actions**: Automatización CI/CD

## Calidad de Código

- Código 100% documentado con docstrings en español
- Cumple con PEP 8 (verificado con flake8)
- Complejidad ciclomática <10
- Cobertura de pruebas: 71% (>70% requerido)
- Validación exhaustiva de entrada

## Métricas del Proyecto

- **Líneas de código**: ~1,200
- **Número de clases**: 3 (EntidadBase, Cliente, ClienteService)
- **Número de métodos**: 28
- **Número de validadores**: 5
- **Número de pruebas**: 46
- **Cobertura de pruebas**: 71%
- **Número de workflows**: 3

## Notas de Desarrollo

### Convenciones de Código

- Nombres en español para comentarios y docstrings
- Nombres en inglés para código (estándar Python)
- Separación clara entre modelos, servicios y validadores
- Uso de type hints en todas las funciones

### Mejoras Futuras

- Base de datos (SQLite o PostgreSQL) en lugar de JSON
- Autenticación de usuarios
- API REST con FastAPI
- Interfaz web con Flask/Django
- Logs persistentes
- Caché de datos

## Autor

Desarrollado como solución de la **Actividad II del Curso DevOps**.

## Licencia

Este proyecto está disponible bajo licencia MIT.

## Contacto y Soporte

Para preguntas o problemas:
1. Abrir un issue en GitHub
2. Revisar la documentación del código
3. Ejecutar las pruebas unitarias para verificar funcionamiento

---

**Última actualización**: Marzo 2024
**Estado del Proyecto**: ✓ Completado y Funcional

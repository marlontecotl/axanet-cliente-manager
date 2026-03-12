# Proyecto Final Fase 2: Gestión de Clientes DevOps

Aplicación Flask simple para la gestión de clientes con almacenamiento en JSON, tests automatizados y pipeline de CI/CD en GitHub Actions.

## Descripción

Esta es una solución simplificada del Proyecto Final Fase 2 del curso DevOps. Implementa:
- API REST básica con Flask (CRUD de clientes)
- Almacenamiento persistente en archivo JSON
- Validación de RFC y email
- Tests automatizados con pytest
- CI Pipeline con GitHub Actions
- Docker para containerización

## Estructura del proyecto

```
Proyecto_Fase2_Ejemplo/
├── app/                    # Código principal de la aplicación
│   ├── __init__.py
│   ├── main.py             # Aplicación Flask principal
│   ├── models.py           # Modelo Cliente
│   ├── routes.py           # Rutas API
│   └── validators.py       # Validadores RFC y email
├── tests/                  # Tests unitarios
│   ├── __init__.py
│   └── test_app.py         # Tests con pytest
├── data/                   # Almacenamiento de datos
│   └── clientes.json       # Base de datos JSON
├── .github/workflows/      # GitHub Actions
│   └── ci.yml              # Pipeline CI
├── docs/                   # Documentación
│   └── infraestructura.md  # Guía de infraestructura AWS
├── Dockerfile              # Configuración Docker
├── requirements.txt        # Dependencias Python
├── .flake8                 # Configuración flake8
├── .gitignore              # Archivos a ignorar en git
└── README.md               # Este archivo
```

## Requisitos

- Python 3.8+
- pip
- git
- Docker (opcional, para containerización)

## Instalación

### 1. Clonar el repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd Proyecto_Fase2_Ejemplo
```

### 2. Crear un entorno virtual

```bash
# En Linux/Mac
python -m venv venv
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

### Ejecutar la aplicación

```bash
# Opción 1: Con Flask (desarrollo)
export FLASK_APP=app.main
flask run

# Opción 2: Directamente con Python
python -m app.main
```

La aplicación estará disponible en `http://localhost:5000`

### Verificar que funciona

```bash
# Health check
curl http://localhost:5000/health

# Listar clientes
curl http://localhost:5000/api/clientes
```

### Ejecutar tests

```bash
# Ejecutar todos los tests
pytest tests/

# Ejecutar con detalle y cobertura
pytest tests/ -v --cov=app
```

### Verificar código con flake8

```bash
flake8 app tests
```

## Endpoints de la API

### Health Check
- **GET** `/health`
  - Respuesta: `{"status": "ok"}`

### Listar Clientes
- **GET** `/api/clientes`
  - Retorna lista de todos los clientes

### Crear Cliente
- **POST** `/api/clientes`
  - Body:
    ```json
    {
      "nombre": "Juan Pérez",
      "email": "juan@example.com",
      "rfc": "ABCD123456XYZ",
      "telefono": "5551234567"
    }
    ```
  - Validaciones:
    - RFC: 4 letras + 6 dígitos + 3 caracteres alfanuméricos
    - Email: formato válido de email

### Obtener Cliente
- **GET** `/api/clientes/<id>`
  - Retorna datos de un cliente específico

### Eliminar Cliente
- **DELETE** `/api/clientes/<id>`
  - Elimina un cliente específico

## Ejemplos de uso

### Crear un cliente

```bash
curl -X POST http://localhost:5000/api/clientes \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Pedro López",
    "email": "pedro@example.com",
    "rfc": "LOPX850615ABC",
    "telefono": "5555555555"
  }'
```

### Obtener todos los clientes

```bash
curl http://localhost:5000/api/clientes
```

### Obtener un cliente específico

```bash
curl http://localhost:5000/api/clientes/1
```

### Eliminar un cliente

```bash
curl -X DELETE http://localhost:5000/api/clientes/1
```

## Docker

### Construir la imagen

```bash
docker build -t gestion-clientes:latest .
```

### Ejecutar el contenedor

```bash
docker run -p 5000:5000 \
  -v $(pwd)/data:/app/data \
  gestion-clientes:latest
```

La aplicación estará disponible en `http://localhost:5000`

## Pipeline CI/CD

El proyecto incluye un GitHub Actions workflow que:
1. Ejecuta flake8 para verificar el código
2. Ejecuta los tests con pytest
3. Se ejecuta automáticamente en cada push a main o develop

Ver `.github/workflows/ci.yml` para más detalles.

## Validaciones

### RFC
- Formato: 4 letras + 6 dígitos + 3 caracteres alfanuméricos
- Ejemplo válido: `ABCD123456XYZ`

### Email
- Debe ser un email válido con formato estándar
- Ejemplo válido: `usuario@dominio.com`

## Estructura de datos (Cliente)

```json
{
  "id": 1,
  "nombre": "Juan Pérez García",
  "email": "juan@example.com",
  "rfc": "PEGJ760512QRX",
  "telefono": "5551234567",
  "creado_en": "2024-01-15T10:30:00"
}
```

## Desarrollo y contribuciones

### Agregar un nuevo endpoint

1. Crear la función en `app/routes.py`
2. Agregar tests en `tests/test_app.py`
3. Ejecutar `pytest` para verificar
4. Ejecutar `flake8` para verificar el código

### Agregar nuevas validaciones

1. Agregar validador en `app/validators.py`
2. Usar el validador en `app/routes.py`
3. Agregar tests para la validación

## Infraestructura

Ver `docs/infraestructura.md` para instrucciones de despliegue en AWS EC2.

## Licencia

Este proyecto es de código abierto y disponible bajo licencia MIT.

## Soporte

Para preguntas o problemas:
1. Revisar los tests en `tests/test_app.py`
2. Consultar la documentación en `docs/`
3. Revisar los logs de GitHub Actions

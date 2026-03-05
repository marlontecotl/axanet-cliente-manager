"""
Módulo de pruebas unitarias para la aplicación.

¿QUÉ ES UN PAQUETE DE TESTS?
- Directorio que contiene todas las pruebas unitarias.
- Una __init__.py hace que tests/ sea "importable" (aunque rara vez importamos tests).

¿ESTRUCTURA COMÚN?
tests/
  __init__.py           ← Este archivo (generalmente vacío o con comentarios)
  test_models.py        ← Pruebas para src/models/
  test_services.py      ← Pruebas para src/services/
  test_validators.py    ← Pruebas para src/validators/
  conftest.py           ← (opcional) Configuración compartida de pytest

¿POR QUÉ __INIT__.PY AUNQUE NO IMPORTEMOS TESTS?
- PYTEST DESCUBRE TESTS: Busca archivos test_*.py y *_test.py.
- NO NECESITA __INIT__.PY: Pytest es flexible, puede descubrir sin __init__.py.
- BUENA PRÁCTICA: Tener __init__.py es consistente con el resto del proyecto.

¿PYTEST VS UNITTEST?
- UNITTEST: Estándar de Python, más verbose (heredas de TestCase).
- PYTEST: Más moderno, assertions simples, fixtures poderosas.
- Este proyecto usa PYTEST (más legible para students).

¿COBERTURA?
- Idealmente, cada línea de código tiene un test.
- Herramientas: pytest-cov, coverage.py.
- En CI/CD: Hacer fallar el build si cobertura < 80%.

DEVOPS EN TESTING:
- Pruebas automáticas en cada commit (pre-commit hooks).
- Pruebas en CI/CD pipeline (GitHub Actions, GitLab CI, etc).
- Reportes de cobertura publicados.
- Pruebas deben ejecutarse en < 30 segundos (feedback rápido).
"""

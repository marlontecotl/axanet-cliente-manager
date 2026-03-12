# Dockerfile para la aplicación de gestión de clientes
# Imagen base: Python 3.11 slim (más pequeña que la estándar)
FROM python:3.11-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar archivo de dependencias
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY . .

# Crear directorio para datos
RUN mkdir -p data

# Exponer el puerto en el que la aplicación escucha
EXPOSE 5000

# Comando para ejecutar la aplicación
# En producción, se recomienda usar gunicorn en lugar de flask run
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]

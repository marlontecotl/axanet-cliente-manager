# Documentación de Infraestructura AWS

Guía para desplegar la aplicación de gestión de clientes en AWS EC2.

## Arquitectura

La aplicación se desplegará en una instancia EC2 t2.micro ejecutando la aplicación Flask en un contenedor Docker.

```
┌─────────────────────────────────────┐
│         Cliente HTTP                │
└────────────────┬────────────────────┘
                 │
                 │ Puerto 80/443
                 │
┌────────────────▼────────────────────┐
│      AWS Security Group              │
│  - Inbound: 22 (SSH), 80, 443       │
│  - Outbound: All                     │
└────────────────┬────────────────────┘
                 │
┌────────────────▼────────────────────┐
│   EC2 Instance (t2.micro)           │
│   - Ubuntu 22.04 LTS                │
│   - Docker instalado                │
│   - Docker Compose instalado        │
└────────────────┬────────────────────┘
                 │
┌────────────────▼────────────────────┐
│    Contenedor Docker (Flask)        │
│   - Puerto 5000 mapeado a 80        │
│   - Volumen: /data (persistente)    │
└─────────────────────────────────────┘
```

## Paso 1: Crear instancia EC2

### 1.1 Acceder a AWS Console
- Ir a: https://console.aws.amazon.com
- Navegar a EC2 Dashboard

### 1.2 Lanzar una nueva instancia

1. Click en "Launch instances"
2. Seleccionar imagen:
   - **AMI**: Ubuntu 22.04 LTS (Free Tier eligible)
   - **Instance Type**: t2.micro (Free Tier)

3. Configurar detalles:
   - **Network**: VPC default
   - **Subnet**: Default subnet
   - **Auto-assign Public IP**: Enable
   - **Storage**: 8 GB (default es suficiente)

4. Agregar Security Group (crear nueva):
   - **Name**: gestion-clientes-sg
   - **Inbound Rules**:
     - SSH: Puerto 22, desde tu IP (o 0.0.0.0/0 para desarrollo)
     - HTTP: Puerto 80, desde 0.0.0.0/0
     - HTTPS: Puerto 443, desde 0.0.0.0/0 (opcional)

5. Crear/seleccionar key pair:
   - **Crear nueva**: gestion-clientes-key.pem
   - Descargar y guardar en lugar seguro
   - Cambiar permisos: `chmod 400 gestion-clientes-key.pem`

6. Review y Launch

## Paso 2: Conectar a la instancia

### 2.1 Obtener la IP pública

1. En EC2 Dashboard, seleccionar la instancia
2. Copiar la dirección IPv4 pública (ej: 54.123.45.67)

### 2.2 SSH en la instancia

```bash
# En tu máquina local
ssh -i gestion-clientes-key.pem ubuntu@54.123.45.67
```

Aceptar el warning sobre autenticidad del host escribiendo `yes`.

## Paso 3: Instalar dependencias en EC2

Una vez conectado vía SSH:

```bash
# Actualizar paquetes
sudo apt update && sudo apt upgrade -y

# Instalar Docker
sudo apt install -y docker.io

# Instalar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Agregar usuario ubuntu al grupo docker (sin necesidad de sudo)
sudo usermod -aG docker ubuntu

# Reiniciar el servicio Docker
sudo systemctl start docker
sudo systemctl enable docker

# Logout y login nuevamente para que los cambios de grupo sean efectivos
exit
ssh -i gestion-clientes-key.pem ubuntu@54.123.45.67
```

## Paso 4: Descargar y ejecutar la aplicación

### 4.1 Clonar el repositorio

```bash
# Ir al home
cd ~

# Clonar el repositorio
git clone <URL_DEL_REPOSITORIO>
cd Proyecto_Fase2_Ejemplo
```

### 4.2 Construir y ejecutar con Docker

```bash
# Construir la imagen Docker
docker build -t gestion-clientes:latest .

# Ejecutar el contenedor
docker run -d \
  --name gestion-clientes \
  -p 80:5000 \
  -v $(pwd)/data:/app/data \
  gestion-clientes:latest
```

Nota: `-d` ejecuta el contenedor en background.

### 4.3 Verificar que está ejecutando

```bash
# Ver contenedores ejecutando
docker ps

# Ver logs
docker logs gestion-clientes

# Probar la aplicación localmente en la instancia
curl http://localhost/health
```

## Paso 5: Probar desde tu máquina

```bash
# Usar la IP pública de la instancia
curl http://54.123.45.67/health

# Crear un cliente
curl -X POST http://54.123.45.67/api/clientes \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Test Cliente",
    "email": "test@example.com",
    "rfc": "TEST123456XYZ",
    "telefono": "5551234567"
  }'

# Listar clientes
curl http://54.123.45.67/api/clientes
```

## Paso 6: Configurar aplicación para producción (opcional)

### 6.1 Usar Nginx como proxy reverso

```bash
# Instalar Nginx
sudo apt install -y nginx

# Crear archivo de configuración
sudo cat > /etc/nginx/sites-available/gestion-clientes <<EOF
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }
}
EOF

# Habilitar la configuración
sudo ln -s /etc/nginx/sites-available/gestion-clientes /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default

# Verificar configuración
sudo nginx -t

# Reiniciar Nginx
sudo systemctl restart nginx
```

### 6.2 Usar Gunicorn para la aplicación

```bash
# Instalar Gunicorn
pip install gunicorn

# Ejecutar con Gunicorn en lugar de Flask
docker run -d \
  --name gestion-clientes \
  -p 5000:5000 \
  -v $(pwd)/data:/app/data \
  gestion-clientes:latest \
  gunicorn -w 4 -b 0.0.0.0:5000 app.main:app
```

## Monitoreo y mantenimiento

### Ver logs de la aplicación

```bash
# Logs recientes
docker logs gestion-clientes

# Logs en tiempo real
docker logs -f gestion-clientes

# Logs de los últimos 100 líneas
docker logs --tail 100 gestion-clientes
```

### Reiniciar la aplicación

```bash
# Detener el contenedor
docker stop gestion-clientes

# Remover el contenedor
docker rm gestion-clientes

# Volver a ejecutar (ver sección 4.2)
```

### Actualizar la aplicación

```bash
# Entrar al directorio
cd ~/Proyecto_Fase2_Ejemplo

# Descargar cambios del repositorio
git pull

# Reconstruir la imagen
docker build -t gestion-clientes:latest .

# Detener el contenedor anterior
docker stop gestion-clientes
docker rm gestion-clientes

# Ejecutar el nuevo contenedor (ver sección 4.2)
```

### Liberar espacio en disco

```bash
# Ver uso de disco
df -h

# Limpiar imágenes y contenedores no utilizados
docker system prune -y

# Limpiar volúmenes no utilizados
docker volume prune -y
```

## Persistencia de datos

Los datos de la aplicación se almacenan en `data/clientes.json` que está mapeado a un volumen de Docker:

```bash
# Acceder a los datos desde la instancia
cat ~/Proyecto_Fase2_Ejemplo/data/clientes.json

# Hacer backup de los datos
cp ~/Proyecto_Fase2_Ejemplo/data/clientes.json ~/clientes_backup.json

# Restaurar datos
cp ~/clientes_backup.json ~/Proyecto_Fase2_Ejemplo/data/clientes.json
docker restart gestion-clientes
```

## Costos estimados (Free Tier)

- EC2 t2.micro: Gratis (primeros 12 meses)
- Data Transfer: Gratis hasta 100GB/mes
- EBS Storage: Gratis (30GB/mes)

Después del período Free Tier: ~$10-15/mes

## Troubleshooting

### La aplicación no responde

```bash
# Verificar que el contenedor está ejecutando
docker ps | grep gestion-clientes

# Ver logs de error
docker logs gestion-clientes

# Reiniciar el contenedor
docker restart gestion-clientes
```

### Puerto 80 está en uso

```bash
# Listar procesos en puerto 80
sudo lsof -i :80

# Matar proceso si es necesario
sudo kill -9 <PID>
```

### No puedo conectarme via SSH

- Verificar que la security group permite SSH (puerto 22)
- Verificar que usas el archivo .pem correcto: `-i gestion-clientes-key.pem`
- Verificar permisos del archivo: `chmod 400 gestion-clientes-key.pem`
- Verificar la dirección IP correcta de la instancia

### Error "docker command not found"

```bash
# Desloguear y volver a loguear para que los permisos se actualicen
exit
ssh -i gestion-clientes-key.pem ubuntu@54.123.45.67
```

## Documentación adicional

- AWS EC2 Documentation: https://docs.aws.amazon.com/ec2/
- Docker Documentation: https://docs.docker.com/
- Flask Documentation: https://flask.palletsprojects.com/
- Nginx Documentation: https://nginx.org/en/docs/

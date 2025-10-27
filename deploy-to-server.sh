#!/bin/bash
# 🎓 Script de Deploy al Servidor AWS
# Sistema de Invitaciones - Universidad Panamericana

echo "🚀 Iniciando deploy al servidor AWS (3.140.201.39)"
echo "=================================================="

# Variables
SERVER="3.140.201.39"
USER="ubuntu"
PROJECT_DIR="/var/www/invitaciones"
SERVICE_NAME="invitaciones"

echo "📡 Conectando al servidor..."

# Crear script temporal para ejecutar remotamente
cat > deploy_remote.sh << 'EOF'
#!/bin/bash
set -e

echo "🔧 Configurando servidor para Sistema de Invitaciones..."

# Actualizar sistema
sudo apt update

# Instalar dependencias del sistema
sudo apt install -y python3 python3-pip python3-venv git nginx

# Crear directorio del proyecto
sudo mkdir -p /var/www/invitaciones
sudo chown ubuntu:ubuntu /var/www/invitaciones

# Ir al directorio del proyecto
cd /var/www/invitaciones

# Clonar/actualizar repositorio
if [ -d ".git" ]; then
    echo "📥 Actualizando repositorio existente..."
    git fetch origin
    git reset --hard origin/main
else
    echo "📥 Clonando repositorio limpio..."
    git clone https://github.com/correa-collab/invitaciones.git .
fi

# Instalar dependencias Python
echo "📦 Instalando dependencias..."
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Crear archivo .env para producción
echo "⚙️ Configurando variables de entorno..."
cat > .env << 'ENVEOF'
# Configuración de Producción
HOST=0.0.0.0
PORT=8000
DEBUG=False

# URLs de Producción
BASE_URL=http://registro.iux.com.mx
QR_BASE_URL=http://registro.iux.com.mx

# Configuración del Evento
EVENT_NAME="Fiesta de Finalización del Posgrado"
EVENT_DATE="Viernes 14 de noviembre de 2025"
EVENT_TIME="17:00 hrs"
EVENT_LOCATION="Ciudad Granja"
UNIVERSITY_CAMPUS="Campus Guadalajara"

# Email (configurar después)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_USER=
EMAIL_PASSWORD=
EMAIL_FROM_NAME="Universidad Panamericana"
ENVEOF

# Configurar Nginx
echo "🌐 Configurando Nginx..."
sudo tee /etc/nginx/sites-available/invitaciones << 'NGINXEOF'
server {
    listen 80;
    server_name registro.iux.com.mx 3.140.201.39;

    # Servir archivos estáticos directamente
    location /static/ {
        alias /var/www/invitaciones/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Proxy para la API
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
NGINXEOF

# Habilitar sitio
sudo ln -sf /etc/nginx/sites-available/invitaciones /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t && sudo systemctl reload nginx

# Crear servicio systemd
echo "🔧 Configurando servicio systemd..."
sudo tee /etc/systemd/system/invitaciones.service << 'SERVICEEOF'
[Unit]
Description=Sistema de Invitaciones - Universidad Panamericana
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/var/www/invitaciones
Environment=PATH=/var/www/invitaciones/.venv/bin
ExecStart=/var/www/invitaciones/.venv/bin/python backend/simple_main.py
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
SERVICEEOF

# Habilitar y iniciar servicio
sudo systemctl daemon-reload
sudo systemctl enable invitaciones
sudo systemctl restart invitaciones

# Verificar estado
echo "✅ Verificando servicios..."
sudo systemctl status nginx --no-pager -l
sudo systemctl status invitaciones --no-pager -l

echo "🎉 ¡Deploy completado!"
echo "🌐 Sitio disponible en: http://registro.iux.com.mx"
echo "🌐 También en: http://3.140.201.39"
EOF

# Hacer el script ejecutable
chmod +x deploy_remote.sh

# Subir y ejecutar en el servidor
echo "📤 Subiendo script al servidor..."
scp deploy_remote.sh ubuntu@${SERVER}:~/ || {
    echo "❌ Error: No se pudo conectar al servidor"
    echo "📋 Instrucciones manuales:"
    echo "1. Conectarse al servidor: ssh ubuntu@3.140.201.39"
    echo "2. Ejecutar los comandos del script deploy_remote.sh"
    exit 1
}

echo "🚀 Ejecutando deploy en el servidor..."
ssh ubuntu@${SERVER} 'bash ~/deploy_remote.sh'

echo "🧹 Limpiando archivos temporales..."
rm -f deploy_remote.sh

echo "=================================================="
echo "✅ ¡Deploy completado exitosamente!"
echo "🌐 Sitio disponible en:"
echo "   - http://registro.iux.com.mx"
echo "   - http://3.140.201.39"
echo "=================================================="
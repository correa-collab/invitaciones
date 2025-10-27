#!/bin/bash
# 🔧 Configuración Inicial del Servidor AWS
# Sistema de Invitaciones - Universidad Panamericana

echo "🚀 Configurando servidor AWS desde cero..."
echo "=========================================="

# Actualizar sistema
echo "📦 Actualizando sistema..."
sudo apt update && sudo apt upgrade -y

# Instalar dependencias básicas
echo "📦 Instalando dependencias del sistema..."
sudo apt install -y git nginx python3-pip python3-venv curl

# Crear directorio del proyecto
echo "📁 Creando directorio del proyecto..."
sudo mkdir -p /var/www/invitaciones
sudo chown ubuntu:ubuntu /var/www/invitaciones

# Ir al directorio
cd /var/www/invitaciones

# Clonar repositorio
echo "📥 Clonando repositorio desde GitHub..."
git clone https://github.com/correa-collab/invitaciones.git .

# Crear entorno virtual
echo "🐍 Creando entorno virtual Python..."
python3 -m venv .venv

# Activar entorno virtual
source .venv/bin/activate

# Instalar dependencias Python
echo "📦 Instalando dependencias Python..."
pip install --upgrade pip
pip install fastapi uvicorn python-dotenv email-validator

# Crear archivo de configuración de email
echo "📧 Creando configuración de email..."
cat > backend/email_config.py << 'EOF'
"""
Configuracion de email
"""

EMAIL_CONFIG = {
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "email": "correa@iux.com.mx",
    "password": "qxpc egxf nnvd lvpj",
    "enabled": True
}
EOF

# Crear directorio de datos
echo "📁 Creando directorio de datos..."
mkdir -p data

# Configurar Nginx
echo "🌐 Configurando Nginx..."
sudo tee /etc/nginx/sites-available/invitaciones << 'NGINXEOF'
server {
    listen 80;
    server_name registro.iux.com.mx 3.140.201.39;

    # Aumentar tamaño máximo de cuerpo de solicitud
    client_max_body_size 20M;

    # Servir archivos estáticos
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
        proxy_read_timeout 300s;
        proxy_connect_timeout 75s;
    }
}
NGINXEOF

# Habilitar sitio en Nginx
echo "🔗 Habilitando sitio en Nginx..."
sudo ln -sf /etc/nginx/sites-available/invitaciones /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Probar configuración de Nginx
echo "✅ Probando configuración de Nginx..."
sudo nginx -t

# Recargar Nginx
echo "🔄 Recargando Nginx..."
sudo systemctl reload nginx

# Crear servicio systemd
echo "🔧 Creando servicio systemd..."
sudo tee /etc/systemd/system/invitaciones.service << 'SERVICEEOF'
[Unit]
Description=Sistema de Invitaciones - Universidad Panamericana
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/var/www/invitaciones/backend
Environment="PATH=/var/www/invitaciones/.venv/bin"
ExecStart=/var/www/invitaciones/.venv/bin/python -m uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=3
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
SERVICEEOF

# Recargar systemd
echo "🔄 Recargando systemd..."
sudo systemctl daemon-reload

# Habilitar servicio para inicio automático
echo "✅ Habilitando servicio..."
sudo systemctl enable invitaciones

# Iniciar servicio
echo "🚀 Iniciando servicio..."
sudo systemctl start invitaciones

# Esperar un momento
sleep 3

# Verificar estado
echo ""
echo "📊 Estado de los servicios:"
echo "=========================="
sudo systemctl status nginx --no-pager -l | head -15
echo ""
sudo systemctl status invitaciones --no-pager -l | head -15

# Probar endpoint
echo ""
echo "🧪 Probando endpoint..."
curl -s http://localhost:8000/test || echo "⚠️  El servidor aún no responde"

echo ""
echo "=========================================="
echo "✅ ¡Configuración inicial completada!"
echo ""
echo "🌐 URLs disponibles:"
echo "   - http://3.140.201.39"
echo "   - http://registro.iux.com.mx"
echo ""
echo "📋 Comandos útiles:"
echo "   - Ver logs: sudo journalctl -u invitaciones -f"
echo "   - Reiniciar: sudo systemctl restart invitaciones"
echo "   - Estado: sudo systemctl status invitaciones"
echo "=========================================="

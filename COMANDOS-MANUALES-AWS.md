# 🚀 COMANDOS MANUALES - Copiar y pegar uno por uno

## ⚠️ IMPORTANTE: Ejecuta estos comandos EN EL SERVIDOR AWS

Primero, conéctate al servidor:
```bash
ssh ubuntu@3.140.201.39
```

---

## Luego ejecuta CADA COMANDO uno por uno:

### 1. Actualizar sistema
```bash
sudo apt update && sudo apt upgrade -y
```

### 2. Instalar dependencias
```bash
sudo apt install -y git nginx python3-pip python3-venv curl
```

### 3. Crear directorio del proyecto
```bash
sudo mkdir -p /var/www/invitaciones
sudo chown ubuntu:ubuntu /var/www/invitaciones
cd /var/www/invitaciones
```

### 4. Clonar repositorio
```bash
git clone https://github.com/correa-collab/invitaciones.git .
```

### 5. Crear entorno virtual
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 6. Instalar dependencias Python
```bash
pip install --upgrade pip
pip install fastapi uvicorn python-dotenv email-validator
```

### 7. Crear configuración de email
```bash
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
```

### 8. Crear directorio de datos
```bash
mkdir -p data
```

### 9. Configurar Nginx
```bash
sudo tee /etc/nginx/sites-available/invitaciones << 'NGINXEOF'
server {
    listen 80;
    server_name registro.iux.com.mx 3.140.201.39;

    client_max_body_size 20M;

    location /static/ {
        alias /var/www/invitaciones/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

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
```

### 10. Habilitar sitio en Nginx
```bash
sudo ln -sf /etc/nginx/sites-available/invitaciones /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl reload nginx
```

### 11. Crear servicio systemd
```bash
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
```

### 12. Activar e iniciar servicio
```bash
sudo systemctl daemon-reload
sudo systemctl enable invitaciones
sudo systemctl start invitaciones
```

### 13. Verificar estado
```bash
sleep 3
sudo systemctl status invitaciones
sudo systemctl status nginx
curl http://localhost:8000/test
```

---

## ✅ Si todo está bien, deberías ver:

- `● invitaciones.service` en estado **active (running)**
- `● nginx.service` en estado **active (running)**  
- `curl` debería retornar: `{"status":"ok","message":"API funcionando correctamente"}`

---

## 🌐 Prueba en tu navegador:
- http://3.140.201.39

---

## 📋 Comandos útiles después de la instalación:

### Ver logs en tiempo real:
```bash
sudo journalctl -u invitaciones -f
```

### Reiniciar servicio:
```bash
sudo systemctl restart invitaciones
```

### Ver estado:
```bash
sudo systemctl status invitaciones
```

### Actualizar código en el futuro:
```bash
cd /var/www/invitaciones
git pull origin main
source .venv/bin/activate
pip install --upgrade fastapi uvicorn python-dotenv email-validator
sudo systemctl restart invitaciones
```

---

## 🆘 Si hay errores:

### Ver logs completos:
```bash
sudo journalctl -u invitaciones -n 100 --no-pager
```

### Probar manualmente:
```bash
cd /var/www/invitaciones/backend
source ../.venv/bin/activate
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000
```

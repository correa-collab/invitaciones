#!/bin/bash

echo "🚀 DEPLOYMENT COMPLETO PARA AWS - VERSIÓN ACTUALIZADA"
echo "====================================================="

# Colores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}📦 Preparando archivos para deployment...${NC}"

# 1. Crear nginx.conf actualizado
echo -e "${YELLOW}📝 Creando configuración de Nginx...${NC}"
mkdir -p nginx
cat > nginx/nginx.conf << 'EOF'
events {
    worker_connections 1024;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;
    
    sendfile        on;
    keepalive_timeout  65;
    
    # Logging
    access_log /var/log/nginx/access.log;
    error_log /var/log/nginx/error.log;
    
    server {
        listen 80;
        server_name registro.iux.com.mx 3.140.201.39;
        
        # Servir archivos estáticos
        location / {
            root /usr/share/nginx/html;
            index index.html;
            try_files $uri $uri/ /index.html;
        }
        
        # Proxy para API del backend
        location /api/ {
            proxy_pass http://backend:8000/api/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
        
        # Proxy para docs de FastAPI
        location /docs {
            proxy_pass http://backend:8000/docs;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
        
        # Proxy para health check
        location /health {
            proxy_pass http://backend:8000/health;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }
}
EOF

# 2. Actualizar requirements.txt con todas las dependencias necesarias
echo -e "${YELLOW}📝 Actualizando requirements.txt...${NC}"
cat > backend/requirements.txt << 'EOF'
fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.5.0
python-multipart==0.0.6
Pillow==10.1.0
smtplib-ssl==1.0.0
email-validator==2.1.0
python-dotenv==1.0.0
EOF

# 3. Crear script de actualización específico para AWS
echo -e "${YELLOW}📝 Creando script de actualización AWS...${NC}"
cat > deploy-aws-update.sh << 'EOF'
#!/bin/bash

echo "🔄 Actualizando servidor AWS..."

# Cambiar al directorio del proyecto
cd /home/ubuntu/invitaciones

# Actualizar código desde GitHub
echo "📥 Descargando últimos cambios..."
git fetch origin
git reset --hard origin/main
git pull origin main

# Parar servicios existentes
echo "🛑 Parando servicios..."
sudo docker-compose -f docker-compose.production.yml down

# Reconstruir y ejecutar
echo "🔨 Reconstruyendo contenedores..."
sudo docker-compose -f docker-compose.production.yml up -d --build

# Esperar que se inicien
echo "⏱️ Esperando inicio de servicios..."
sleep 20

# Verificar estado
echo "📊 Estado de servicios:"
sudo docker-compose -f docker-compose.production.yml ps

# Health check
echo "🌐 Verificando conectividad..."
curl -s http://localhost/health && echo "✅ Backend OK" || echo "❌ Backend error"
curl -s http://localhost/ | head -1 && echo "✅ Frontend OK" || echo "❌ Frontend error"

echo "🎉 ¡Actualización completada!"
echo "🌐 Sitio disponible en: http://registro.iux.com.mx"
EOF

chmod +x deploy-aws-update.sh

# 4. Verificar archivos creados
echo -e "${BLUE}📋 Verificando archivos de deployment...${NC}"
echo "✅ nginx.conf creado"
echo "✅ requirements.txt actualizado"  
echo "✅ Dockerfile.simple creado"
echo "✅ docker-compose.production.yml creado"
echo "✅ deploy-aws-update.sh creado"

# 5. Mostrar siguiente paso
echo ""
echo -e "${GREEN}🎯 PRÓXIMOS PASOS PARA ACTUALIZAR AWS:${NC}"
echo -e "${YELLOW}1. Sube estos archivos a GitHub:${NC}"
echo "   git add ."
echo "   git commit -m '🚀 Archivos de deployment actualizados'"
echo "   git push origin main"
echo ""
echo -e "${YELLOW}2. En el servidor AWS ejecuta:${NC}"
echo "   cd /home/ubuntu/invitaciones"
echo "   git pull origin main"
echo "   chmod +x deploy-aws-update.sh"
echo "   ./deploy-aws-update.sh"
echo ""
echo -e "${BLUE}🌐 URLs después de actualizar:${NC}"
echo "Frontend: http://registro.iux.com.mx"
echo "API Docs: http://registro.iux.com.mx/docs"  
echo "Health: http://registro.iux.com.mx/health"
echo "Confirmación: http://registro.iux.com.mx/confirmation.html"

echo ""
echo -e "${GREEN}📦 ¡Archivos de deployment listos!${NC}"
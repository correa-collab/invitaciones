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

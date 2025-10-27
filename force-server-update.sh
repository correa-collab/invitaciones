#!/bin/bash

echo "🔄 VERIFICACIÓN Y ACTUALIZACIÓN ESPECÍFICA DEL SERVIDOR AWS"
echo "=========================================================="

echo "📥 Paso 1: Forzar descarga de TODA la versión más reciente de GitHub..."
cd /home/ubuntu/invitaciones
git fetch --all
git reset --hard origin/main
git clean -fd  # Eliminar archivos no rastreados
git pull origin main

echo "🔍 Paso 2: Verificar que los archivos correctos llegaron..."
echo "Verificando confirmation.html:"
if grep -q "Descargar Pase" static/confirmation.html; then
    if ! grep -q "Enviar por Correo" static/confirmation.html; then
        echo "✅ confirmation.html CORRECTO - Solo botón de descarga"
    else
        echo "❌ confirmation.html INCORRECTO - Ambos botones presentes"
    fi
else
    echo "❌ confirmation.html INCORRECTO - Falta botón de descarga"
fi

echo ""
echo "📊 Información de archivos:"
echo "static/confirmation.html - $(wc -l < static/confirmation.html) líneas"
echo "backend/simple_main.py - $(wc -l < backend/simple_main.py) líneas"

echo ""
echo "🛑 Paso 3: Parar servicios web pero mantener datos..."
sudo docker-compose stop web frontend nginx 2>/dev/null || true

echo "🧹 Paso 4: Limpiar solo cache de imágenes web..."
sudo docker image prune -f
sudo docker container prune -f

echo "🔨 Paso 5: Reconstruir solo nginx con archivos frescos..."
sudo docker run --rm --name temp-nginx -d -p 80:80 -v $(pwd)/static:/usr/share/nginx/html:ro nginx:alpine

echo "⏱️ Paso 6: Esperar y verificar..."
sleep 10

echo "🌐 Paso 7: Verificar que la página sirve archivos correctos..."
echo "Probando localhost:"
curl -s http://localhost/confirmation.html | grep "Descargar Pase" && echo "✅ ÉXITO" || echo "❌ FALLO"

echo ""
echo "📋 Paso 8: Limpiar y ejecutar configuración final..."
sudo docker stop temp-nginx 2>/dev/null || true

# Ejecutar con docker-compose simple
cat > docker-compose.simple.yml << 'EOF'
version: '3.8'
services:
  web:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./static:/usr/share/nginx/html:ro
    restart: unless-stopped
EOF

sudo docker-compose -f docker-compose.simple.yml up -d

echo ""
echo "🎉 VERIFICACIÓN FINAL:"
sleep 5
curl -s http://localhost/confirmation.html | head -20 | grep -E "(Confirmar Asistencia|Descargar Pase)" || echo "❌ Problema en verificación final"

echo ""
echo "🌐 Probar ahora:"
echo "http://registro.iux.com.mx/confirmation.html"
echo "http://3.140.201.39/confirmation.html"
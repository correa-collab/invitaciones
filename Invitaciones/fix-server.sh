#!/bin/bash

echo "🔧 Diagnosticando y reparando el servidor de invitaciones..."

# Ir al directorio del proyecto
cd /home/ubuntu/invitation-system || { echo "❌ Directorio del proyecto no encontrado"; exit 1; }

# Verificar estado de Docker
echo "📊 Verificando estado de Docker..."
docker ps -a

echo "📊 Verificando logs del backend..."
docker logs invitation-backend 2>&1 | tail -20

echo "📊 Verificando logs del frontend..."
docker logs invitation-frontend 2>&1 | tail -20

# Detener contenedores existentes
echo "🛑 Deteniendo contenedores existentes..."
docker-compose down

# Limpiar contenedores e imágenes antiguas
echo "🧹 Limpiando contenedores antiguos..."
docker system prune -f

# Verificar que el directorio de datos existe
echo "📁 Verificando directorio de datos..."
mkdir -p data
chmod 755 data

# Verificar que el archivo de RSVPs existe
echo "📄 Verificando archivo de RSVPs..."
if [ ! -f "data/rsvps.json" ]; then
    echo "[]" > data/rsvps.json
    chmod 644 data/rsvps.json
fi

# Reconstruir y ejecutar contenedores
echo "🚀 Reconstruyendo y ejecutando contenedores..."
docker-compose up --build -d

# Esperar un momento para que los servicios se inicien
echo "⏳ Esperando que los servicios se inicien..."
sleep 10

# Verificar estado final
echo "✅ Verificando estado final..."
docker ps
echo ""
echo "🌐 Verificando conectividad..."
curl -f http://localhost:8000/health || echo "❌ Backend no responde"
curl -f http://localhost:80 || echo "❌ Frontend no responde"

# Mostrar logs finales
echo "📋 Logs finales del backend:"
docker logs invitation-backend 2>&1 | tail -10

echo "📋 Logs finales del frontend:"
docker logs invitation-frontend 2>&1 | tail -10

echo "🎉 Diagnóstico y reparación completados!"
echo "🌍 La aplicación debería estar disponible en http://3.140.201.39"
#!/bin/bash

echo "🔧 SCRIPT DE REPARACIÓN - LIBERANDO PUERTO 8000"
echo "==============================================="

echo "1️⃣ Verificando qué está usando el puerto 8000..."
lsof -i :8000

echo ""
echo "2️⃣ Matando procesos que usan el puerto 8000..."
# Matar cualquier proceso usando el puerto 8000
sudo lsof -ti :8000 | xargs -r sudo kill -9

echo ""
echo "3️⃣ Parando todos los contenedores Docker..."
sudo docker-compose down

echo ""
echo "4️⃣ Limpiando contenedores y redes Docker..."
sudo docker system prune -f
sudo docker network prune -f

echo ""
echo "5️⃣ Verificando que el puerto esté libre..."
if lsof -i :8000; then
    echo "❌ Puerto 8000 aún en uso"
    echo "🔧 Intentando método más agresivo..."
    sudo fuser -k 8000/tcp
else
    echo "✅ Puerto 8000 liberado"
fi

echo ""
echo "6️⃣ Reconstruyendo y ejecutando contenedores..."
sudo docker-compose up -d --build

echo ""
echo "7️⃣ Esperando que los servicios se inicien..."
sleep 20

echo ""
echo "8️⃣ Verificando estado de los servicios..."
sudo docker-compose ps

echo ""
echo "9️⃣ Verificando conectividad..."
curl -s http://localhost/health || echo "❌ Health check falló"

echo ""
echo "🎉 Proceso completado!"
echo "🌐 Verifica: http://registro.iux.com.mx"
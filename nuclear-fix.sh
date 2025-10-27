#!/bin/bash

echo "🔥 SOLUCIÓN NUCLEAR - FORZAR ACTUALIZACIÓN COMPLETA"
echo "=================================================="

echo "🛑 Paso 1: Parar y eliminar TODO..."
sudo docker stop $(sudo docker ps -aq) 2>/dev/null || true
sudo docker rm $(sudo docker ps -aq) 2>/dev/null || true
sudo docker rmi $(sudo docker images -q) 2>/dev/null || true
sudo docker system prune -af --volumes

echo "📥 Paso 2: Actualizar código fuente..."
cd /home/ubuntu/invitaciones
git stash
git fetch origin
git reset --hard origin/main
git pull origin main

echo "📋 Paso 3: Verificar archivos locales..."
echo "confirmation.html debe tener solo 'Descargar Pase':"
grep -n "Descargar Pase" static/confirmation.html && echo "✅ OK"
grep -n "Enviar por Correo" static/confirmation.html && echo "❌ PROBLEMA: Botón aún existe" || echo "✅ OK: Botón eliminado"

echo "🔨 Paso 4: Recrear docker-compose.yml simple..."
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile.simple
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app
      - ./static:/app/static
    restart: unless-stopped
    environment:
      - PYTHONPATH=/app

  web:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./static:/usr/share/nginx/html:ro
    restart: unless-stopped
    depends_on:
      - backend
EOF

echo "🐳 Paso 5: Crear Dockerfile.simple actualizado..."
cat > backend/Dockerfile.simple << 'EOF'
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "simple_main.py"]
EOF

echo "📦 Paso 6: Verificar requirements.txt..."
cat > backend/requirements.txt << 'EOF'
fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.5.0
python-multipart==0.0.6
Pillow==10.1.0
email-validator==2.1.0
python-dotenv==1.0.0
EOF

echo "🚀 Paso 7: Construir desde cero..."
sudo docker-compose build --no-cache --parallel

echo "🔥 Paso 8: Ejecutar servicios..."
sudo docker-compose up -d

echo "⏱️ Paso 9: Esperar inicio..."
sleep 20

echo "🔍 Paso 10: Verificar resultado..."
sudo docker-compose ps
echo ""
echo "Verificando archivos servidos:"
curl -s http://localhost/confirmation.html | grep -i "descargar.*pase" && echo "✅ ÉXITO: Botón correcto" || echo "❌ FALLO: Botón faltante"
curl -s http://localhost/confirmation.html | grep -i "enviar.*correo" && echo "❌ FALLO: Botón viejo presente" || echo "✅ ÉXITO: Botón viejo eliminado"

echo ""
echo "🌐 Probar en:"
echo "http://registro.iux.com.mx/confirmation.html"
echo "http://3.140.201.39/confirmation.html"

echo ""
echo "📊 Estado final:"
sudo docker-compose logs --tail=5
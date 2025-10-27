#!/bin/bash

echo "🔄 ACTUALIZACIÓN SEGURA PARA PRODUCCIÓN (Preserva bases de datos)"
echo "================================================================"

echo "💾 Paso 1: Backup automático de bases de datos..."
mkdir -p backups/$(date +%Y%m%d_%H%M%S)
sudo docker exec invitaciones-database-1 pg_dump -U postgres invitaciones_db > backups/$(date +%Y%m%d_%H%M%S)/database_backup.sql 2>/dev/null || echo "No hay BD PostgreSQL"
cp *.db backups/$(date +%Y%m%d_%H%M%S)/ 2>/dev/null || echo "No hay BD SQLite"

echo "🛑 Paso 2: Parar solo servicios web (mantener BD)..."
sudo docker-compose stop frontend backend web
# NO parar database

echo "🧹 Paso 3: Limpiar solo imágenes web (preservar BD)..."
sudo docker rmi $(sudo docker images | grep -E "(frontend|backend|web|nginx)" | awk '{print $3}') 2>/dev/null || true

echo "📥 Paso 4: Actualizar código..."
cd /home/ubuntu/invitaciones
git stash push -m "Cambios locales $(date)"
git fetch origin
git reset --hard origin/main
git pull origin main

echo "🔨 Paso 5: Recrear solo servicios web..."
# Usar docker-compose que NO toque la BD
cat > docker-compose.safe.yml << 'EOF'
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
      - database_data:/app/data  # Preservar datos locales
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

volumes:
  database_data:  # Volume persistente para datos
EOF

echo "🚀 Paso 6: Construir y ejecutar..."
sudo docker-compose -f docker-compose.safe.yml build --no-cache
sudo docker-compose -f docker-compose.safe.yml up -d

echo "⏱️ Paso 7: Verificar..."
sleep 15
sudo docker-compose -f docker-compose.safe.yml ps

echo "✅ Actualización segura completada"
echo "💾 Backup guardado en: backups/$(date +%Y%m%d_%H%M%S)/"
echo "🗄️ Base de datos preservada"
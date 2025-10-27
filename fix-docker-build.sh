#!/bin/bash

echo "🔧 SOLUCIÓN RÁPIDA PARA ERROR DE DOCKER BUILD"
echo "============================================"

# 1. Limpiar requirements.txt problemático
echo "📝 Creando requirements.txt limpio..."
cat > backend/requirements.txt << 'EOF'
fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.5.0
python-multipart==0.0.6
Pillow==10.1.0
email-validator==2.1.0
python-dotenv==1.0.0
EOF

# 2. Limpiar Docker cache
echo "🧹 Limpiando cache de Docker..."
sudo docker system prune -f
sudo docker-compose -f docker-compose.production.yml down --rmi all 2>/dev/null || true

# 3. Rebuild paso a paso
echo "🔨 Reconstruyendo sin cache..."
sudo docker-compose -f docker-compose.production.yml build --no-cache

# 4. Ejecutar
echo "🚀 Ejecutando servicios..."
sudo docker-compose -f docker-compose.production.yml up -d

# 5. Verificar
echo "📊 Verificando estado..."
sleep 10
sudo docker-compose -f docker-compose.production.yml ps
sudo docker-compose -f docker-compose.production.yml logs backend | tail -10

echo "🎉 ¡Listo! Prueba http://registro.iux.com.mx"
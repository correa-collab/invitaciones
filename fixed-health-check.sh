#!/bin/bash

echo "🔧 COMANDO DE REPARACIÓN ACTUALIZADO - HEALTH CHECK CORREGIDO"
echo "============================================================="

cat << 'EOF'
cd /home/ubuntu/invitaciones && git pull origin main && sudo lsof -ti :8000 | xargs -r sudo kill -9 && sudo docker-compose down && sudo docker system prune -f && sudo docker network prune -f && sudo fuser -k 8000/tcp 2>/dev/null || true && sudo docker-compose up -d --build && sleep 30 && sudo docker-compose ps && sudo docker-compose logs backend --tail=10 && curl -s http://localhost/health && echo "🎉 ¡Reparación completa! Sitio: http://registro.iux.com.mx"
EOF

echo ""
echo "💡 CAMBIOS REALIZADOS:"
echo "- ✅ Instalado curl en el contenedor backend"
echo "- ✅ Mejorado health check con más tiempo de espera"
echo "- ✅ Agregado start_period de 40s para dar tiempo al inicio"
echo "- ✅ Aumentado retries a 5 para mayor estabilidad"
echo ""
echo "📋 INSTRUCCIONES:"
echo "1. Conecta al servidor: ssh ubuntu@3.140.201.39"
echo "2. Copia y pega el comando de arriba"
echo "3. Espera a que termine (puede tardar 2-3 minutos)"
echo "4. Verifica: http://registro.iux.com.mx"
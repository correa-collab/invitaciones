#!/bin/bash
# Script de una línea para copiar y pegar en el servidor AWS

echo "🚀 COMANDO DE UNA LÍNEA PARA COPIAR Y PEGAR:"
echo "============================================="

cat << 'EOF'
cd /home/ubuntu/invitaciones && sudo lsof -ti :8000 | xargs -r sudo kill -9 && sudo docker-compose down && sudo docker system prune -f && sudo docker network prune -f && sudo fuser -k 8000/tcp 2>/dev/null || true && sudo docker-compose up -d --build && sleep 20 && sudo docker-compose ps && curl -s http://localhost/health && echo "🎉 ¡Reparación completa! Sitio: http://registro.iux.com.mx"
EOF

echo ""
echo "💡 INSTRUCCIONES:"
echo "1. Conecta al servidor: ssh ubuntu@3.140.201.39"
echo "2. Copia y pega el comando de arriba"
echo "3. Espera a que termine (puede tardar 1-2 minutos)"
echo "4. Verifica: http://registro.iux.com.mx"
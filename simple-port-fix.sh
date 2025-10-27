#!/bin/bash

echo "🚀 COMANDO SIMPLE - LIBERAR PUERTOS Y REINICIAR"
echo "=============================================="

cat << 'EOF'
sudo systemctl stop nginx apache2 2>/dev/null || true && sudo pkill -f nginx && sudo pkill -f apache && sudo lsof -ti :80,:8000 | xargs -r sudo kill -9 && cd /home/ubuntu/invitaciones && sudo docker-compose down && sudo docker system prune -af && git pull origin main && sudo docker-compose up -d --build && sleep 30 && sudo docker-compose ps
EOF

echo ""
echo "💡 ESTE COMANDO MÁS SIMPLE:"
echo "- Para nginx/apache del sistema"
echo "- Mata procesos en puertos 80 y 8000"
echo "- Limpia Docker completamente"
echo "- Actualiza y reconstruye"
echo ""
echo "⚡ ÚSALO SI EL COMANDO LARGO FALLA"
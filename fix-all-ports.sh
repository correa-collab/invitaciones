#!/bin/bash

echo "🔧 COMANDO DE REPARACIÓN COMPLETA - PUERTOS 80 Y 8000"
echo "====================================================="

cat << 'EOF'
cd /home/ubuntu/invitaciones && echo "🛑 Parando servicios web..." && sudo systemctl stop nginx apache2 2>/dev/null || true && sudo systemctl stop docker 2>/dev/null || true && sudo systemctl start docker && echo "🔧 Liberando puertos 80 y 8000..." && sudo lsof -ti :80 | xargs -r sudo kill -9 && sudo lsof -ti :8000 | xargs -r sudo kill -9 && sudo fuser -k 80/tcp 8000/tcp 2>/dev/null || true && echo "🐳 Limpiando Docker..." && sudo docker-compose down && sudo docker system prune -af && sudo docker network prune -f && echo "📥 Actualizando código..." && git pull origin main && echo "🚀 Reconstruyendo aplicación..." && sudo docker-compose up -d --build && sleep 40 && echo "📊 Estado de servicios:" && sudo docker-compose ps && echo "📝 Logs del backend:" && sudo docker-compose logs backend --tail=10 && echo "📝 Logs del frontend:" && sudo docker-compose logs frontend --tail=5 && echo "🌐 Verificando conectividad..." && curl -s http://localhost/health && curl -s http://localhost/ | head -1 && echo "🎉 ¡Reparación completa! Sitio: http://registro.iux.com.mx"
EOF

echo ""
echo "💡 SOLUCIONES APLICADAS:"
echo "- 🛑 Para servicios nginx/apache que ocupan puerto 80"
echo "- 🔧 Libera puertos 80 y 8000 agresivamente"
echo "- 🐳 Limpieza completa de Docker"
echo "- 📥 Actualiza código desde GitHub"
echo "- 🚀 Reconstruye con configuración corregida"
echo "- ⏱️ Espera 40s para health checks"
echo "- 📊 Muestra diagnósticos completos"
echo ""
echo "📋 INSTRUCCIONES:"
echo "1. Conecta al servidor: ssh ubuntu@3.140.201.39"
echo "2. Copia y pega el comando de arriba"
echo "3. Espera a que termine (puede tardar 3-4 minutos)"
echo "4. Verifica: http://registro.iux.com.mx"
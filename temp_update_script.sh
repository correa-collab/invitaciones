#!/bin/bash
cd /home/ubuntu/invitaciones
echo '🔄 Actualizando código desde GitHub...'
git fetch origin
git reset --hard origin/main
git pull origin main
echo '✅ Código actualizado'

echo '🐳 Reconstruyendo contenedores Docker...'
sudo docker-compose down
sudo docker-compose up -d --build

echo '⏱️ Esperando que los servicios se inicien...'
sleep 15

echo '📊 Estado de los servicios:'
sudo docker-compose ps

echo '🌐 Verificando conectividad...'
curl -s http://localhost/health || echo '❌ Health check falló'

echo '🎉 ¡Actualización completa!'
echo '🌐 Tu sitio está disponible en: http://registro.iux.com.mx'

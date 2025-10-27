#!/bin/bash
# Script de actualización simplificado para AWS

cd /home/ubuntu/invitaciones
git fetch origin
git reset --hard origin/main
git pull origin main
sudo docker-compose down
sudo docker-compose up -d --build
sleep 15
sudo docker-compose ps
curl -s http://localhost/health
echo "🎉 Actualización completa! Sitio disponible en: http://registro.iux.com.mx"
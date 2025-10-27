#!/bin/bash

echo "🔍 DIAGNÓSTICO DEL PROBLEMA DE ARCHIVOS ESTÁTICOS"
echo "================================================"

echo "1. 📁 Verificando estructura de archivos..."
echo "Archivos en static/:"
ls -la static/
echo ""

echo "2. 📝 Verificando confirmation.html local..."
echo "Últimas líneas de confirmation.html:"
tail -5 static/confirmation.html
echo ""

echo "3. 🐳 Verificando contenedores..."
sudo docker-compose -f docker-compose.production.yml ps
echo ""

echo "4. 🌐 Verificando que nginx sirva los archivos correctos..."
echo "Dentro del contenedor frontend:"
sudo docker exec invitaciones-frontend-1 ls -la /usr/share/nginx/html/ || echo "Contenedor frontend no accesible"
echo ""

echo "5. 📄 Comparando archivos..."
echo "confirmation.html en el contenedor:"
sudo docker exec invitaciones-frontend-1 head -20 /usr/share/nginx/html/confirmation.html || echo "Archivo no accesible en contenedor"
echo ""

echo "6. 🔄 Test de conectividad..."
curl -s http://localhost/confirmation.html | head -10
echo ""

echo "🎯 POSIBLES SOLUCIONES:"
echo "A) Recrear contenedores con volume fresh"
echo "B) Verificar que docker-compose.production.yml mapee static/ correctamente"
echo "C) Forzar rebuild del frontend"

echo ""
echo "💡 Para solucionar, ejecuta:"
echo "sudo docker-compose -f docker-compose.production.yml down -v"
echo "sudo docker-compose -f docker-compose.production.yml up -d --build"
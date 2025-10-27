#!/bin/bash
# 🚀 Script Rápido de Deploy a AWS
# Sistema de Invitaciones - Universidad Panamericana

set -e

SERVER="ubuntu@3.140.201.39"
PROJECT_DIR="/var/www/invitaciones"

echo "🚀 Iniciando deployment rápido..."
echo "=================================="

# Conectar y ejecutar comandos
ssh $SERVER << 'ENDSSH'
    cd /var/www/invitaciones
    
    echo "📥 Actualizando código desde GitHub..."
    git fetch origin
    git reset --hard origin/main
    
    echo "📦 Actualizando dependencias..."
    source .venv/bin/activate
    pip install --quiet --upgrade pip
    pip install --quiet fastapi uvicorn python-dotenv email-validator
    
    echo "🔄 Reiniciando servicio..."
    sudo systemctl restart invitaciones
    
    echo "⏳ Esperando 3 segundos..."
    sleep 3
    
    echo "✅ Verificando estado..."
    sudo systemctl status invitaciones --no-pager -l | head -20
    
    echo ""
    echo "🧪 Probando endpoint..."
    curl -s http://localhost:8000/test || echo "❌ El servidor no responde"
    
    echo ""
    echo "✅ ¡Deployment completado!"
ENDSSH

echo ""
echo "=================================="
echo "🎉 ¡Actualización exitosa!"
echo "🌐 Sitio disponible en:"
echo "   - http://3.140.201.39"
echo "   - http://registro.iux.com.mx"
echo "=================================="

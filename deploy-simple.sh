#!/bin/bash

# Script simplificado para deployment al servidor AWS
# IP del servidor: 3.140.201.39

SERVER_IP="3.140.201.39"
SERVER_USER="ubuntu"
PROJECT_DIR="/home/ubuntu/invitaciones"

echo "🚀 Iniciando deployment simplificado al servidor AWS..."
echo "📍 Servidor: $SERVER_IP"

# Comprimir archivos necesarios
echo "📦 Comprimiendo archivos del proyecto..."
tar -czf invitaciones-deploy.tar.gz \
    --exclude='.venv' \
    --exclude='node_modules' \
    --exclude='__pycache__' \
    --exclude='.git' \
    backend/ static/ docker-compose-simple.yml Dockerfile.simple

echo "✅ Archivos comprimidos en invitaciones-deploy.tar.gz"
echo ""
echo "📋 PASOS PARA CONTINUAR:"
echo ""
echo "1️⃣ **Subir archivo al servidor:**"
echo "   Opción A - Con SCP (si funciona SSH):"
echo "   scp invitaciones-deploy.tar.gz ubuntu@$SERVER_IP:~/"
echo ""
echo "   Opción B - Usando AWS EC2 Instance Connect:"
echo "   - Ve a AWS Console → EC2 → Instancias"
echo "   - Conecta vía Instance Connect"
echo "   - Sube el archivo manualmente o usa wget con un link"
echo ""
echo "2️⃣ **En el servidor, ejecutar:**"
echo "   cd ~"
echo "   tar -xzf invitaciones-deploy.tar.gz"
echo "   sudo apt update"
echo "   sudo apt install -y docker.io docker-compose"
echo "   sudo docker-compose -f docker-compose-simple.yml up -d --build"
echo ""
echo "3️⃣ **Verificar:**"
echo "   sudo docker-compose -f docker-compose-simple.yml ps"
echo "   sudo docker-compose -f docker-compose-simple.yml logs"
echo ""
echo "🌐 **Una vez deployado, tu app estará en:**"
echo "   http://$SERVER_IP"
echo "   http://$SERVER_IP/admin.html"
echo "   http://$SERVER_IP/confirmation.html"

# Intentar conexión SSH automática si es posible
echo ""
echo "🔄 Intentando conexión SSH automática..."
if ssh -o ConnectTimeout=5 -o StrictHostKeyChecking=no $SERVER_USER@$SERVER_IP "echo 'SSH conectado exitosamente'"; then
    echo "✅ SSH funciona! Procediendo con deployment automático..."
    
    # Subir archivo
    echo "📤 Subiendo archivo..."
    scp -o StrictHostKeyChecking=no invitaciones-deploy.tar.gz $SERVER_USER@$SERVER_IP:~/
    
    # Ejecutar comandos en el servidor
    echo "🚀 Ejecutando deployment en el servidor..."
    ssh -o StrictHostKeyChecking=no $SERVER_USER@$SERVER_IP << 'EOF'
        echo "📂 Extrayendo archivos..."
        tar -xzf invitaciones-deploy.tar.gz
        
        echo "🐳 Instalando Docker si no existe..."
        if ! command -v docker &> /dev/null; then
            sudo apt update
            sudo apt install -y docker.io docker-compose
            sudo usermod -aG docker ubuntu
        fi
        
        echo "🛑 Parando servicios anteriores..."
        sudo docker-compose -f docker-compose-simple.yml down 2>/dev/null || true
        
        echo "🚀 Iniciando aplicación..."
        sudo docker-compose -f docker-compose-simple.yml up -d --build
        
        echo "📊 Estado de la aplicación:"
        sudo docker-compose -f docker-compose-simple.yml ps
        
        echo "✅ Deployment completado!"
EOF
    
    echo ""
    echo "🎉 ¡DEPLOYMENT EXITOSO!"
    echo "🌐 Tu aplicación está disponible en: http://$SERVER_IP"
    
else
    echo ""
    echo "⚠️  SSH no disponible. Usa el método manual descrito arriba."
    echo "💡 El archivo 'invitaciones-deploy.tar.gz' está listo para subir."
fi
#!/bin/bash

# Script para subir el proyecto al servidor AWS EC2
# IP del servidor: 3.140.201.39

SERVER_IP="3.140.201.39"
SERVER_USER="ubuntu"
PROJECT_DIR="/home/ubuntu/invitaciones"

echo "🚀 Iniciando deployment al servidor AWS..."

# Verificar conexión SSH
echo "📡 Verificando conexión al servidor..."
if ! ssh -o ConnectTimeout=10 $SERVER_USER@$SERVER_IP "echo 'Conexión exitosa'"; then
    echo "❌ Error: No se puede conectar al servidor $SERVER_IP"
    echo "Verifica:"
    echo "1. Que la instancia EC2 esté ejecutándose"
    echo "2. Que el Security Group permita SSH (puerto 22)"
    echo "3. Que tengas acceso SSH configurado"
    exit 1
fi

# Crear directorio del proyecto en el servidor
echo "📁 Creando directorio del proyecto..."
ssh $SERVER_USER@$SERVER_IP "mkdir -p $PROJECT_DIR"

# Subir archivos al servidor
echo "📤 Subiendo archivos al servidor..."
rsync -avz --exclude='node_modules' --exclude='venv' --exclude='__pycache__' --exclude='.git' \
    . $SERVER_USER@$SERVER_IP:$PROJECT_DIR/

# Configurar y ejecutar en el servidor
echo "🐳 Configurando Docker en el servidor..."
ssh $SERVER_USER@$SERVER_IP << 'EOF'
cd /home/ubuntu/invitaciones

# Verificar si Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "📦 Instalando Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker ubuntu
    rm get-docker.sh
fi

# Verificar si Docker Compose está instalado
if ! command -v docker-compose &> /dev/null; then
    echo "📦 Instalando Docker Compose..."
    sudo apt update
    sudo apt install -y docker-compose
fi

# Parar servicios anteriores si existen
echo "🛑 Parando servicios anteriores..."
sudo docker-compose down 2>/dev/null || true

# Construir y ejecutar los servicios
echo "🚀 Construyendo y ejecutando servicios..."
sudo docker-compose up -d --build

# Verificar estado de los servicios
echo "📊 Estado de los servicios:"
sudo docker-compose ps

# Verificar logs
echo "📝 Últimos logs:"
sudo docker-compose logs --tail=20

EOF

echo "✅ Deployment completado!"
echo ""
echo "🌐 Tu aplicación está disponible en:"
echo "   Frontend: http://$SERVER_IP"
echo "   API Docs: http://$SERVER_IP/api/docs"
echo "   Dashboard: http://$SERVER_IP/dashboard"
echo ""
echo "📋 Para ver logs en vivo:"
echo "   ssh $SERVER_USER@$SERVER_IP"
echo "   cd $PROJECT_DIR"
echo "   sudo docker-compose logs -f"
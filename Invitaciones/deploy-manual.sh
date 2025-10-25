#!/bin/bash

# Script alternativo usando AWS CLI para deployment
# Para usar cuando SSH directo no está disponible

echo "🚀 Script de deployment para AWS EC2"
echo "📋 Instrucciones para deployment manual:"
echo ""

echo "1️⃣ PREPARAR ARCHIVOS LOCALMENTE:"
echo "   ✅ Archivos ya preparados en: $(pwd)"
echo ""

echo "2️⃣ COPIAR AL SERVIDOR (usando AWS Console):"
echo "   🔸 Conecta a la instancia via AWS Console > EC2 > Instance Connect"
echo "   🔸 En el terminal del servidor, ejecuta:"
echo ""
echo "   # Crear directorio del proyecto"
echo "   mkdir -p ~/invitaciones"
echo "   cd ~/invitaciones"
echo ""
echo "   # Clonar desde Git (si tienes repositorio) O subir archivos manualmente"
echo ""

echo "3️⃣ COMANDOS PARA EL SERVIDOR:"
cat << 'EOF'

# ============== EJECUTAR EN EL SERVIDOR AWS ==============

# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Docker si no está instalado
if ! command -v docker &> /dev/null; then
    echo "Instalando Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker ubuntu
    newgrp docker
fi

# Instalar Docker Compose si no está instalado
if ! command -v docker-compose &> /dev/null; then
    echo "Instalando Docker Compose..."
    sudo apt install -y docker-compose
fi

# Ir al directorio del proyecto
cd ~/invitaciones

# Parar servicios anteriores (si existen)
sudo docker-compose down 2>/dev/null || true

# Construir y ejecutar servicios
sudo docker-compose up -d --build

# Verificar estado
sudo docker-compose ps

# Ver logs
sudo docker-compose logs

EOF

echo ""
echo "4️⃣ VERIFICAR DEPLOYMENT:"
echo "   🌐 Frontend: http://3.140.201.39"
echo "   🔗 API Docs: http://3.140.201.39/api/docs"
echo "   📊 Dashboard: http://3.140.201.39/dashboard"
echo ""

echo "5️⃣ COMANDOS ÚTILES PARA EL SERVIDOR:"
echo "   # Ver logs en tiempo real:"
echo "   sudo docker-compose logs -f"
echo ""
echo "   # Reiniciar servicios:"
echo "   sudo docker-compose restart"
echo ""
echo "   # Parar todo:"
echo "   sudo docker-compose down"
echo ""

# Crear un archivo zip con el proyecto para facilitar la transferencia
echo "📦 Creando archivo ZIP del proyecto..."
zip -r invitaciones-proyecto.zip . -x "node_modules/*" "venv/*" "__pycache__/*" ".git/*" "*.zip"

echo "✅ Archivo ZIP creado: invitaciones-proyecto.zip"
echo "📤 Puedes subirlo manualmente al servidor y descomprimirlo con:"
echo "   unzip invitaciones-proyecto.zip -d ~/invitaciones"
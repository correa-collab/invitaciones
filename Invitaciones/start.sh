#!/bin/bash

# Script para iniciar el proyecto de invitaciones
# Este script ayuda a ejecutar el proyecto localmente

set -e

echo "🎉 Sistema de Gestión de Invitaciones - Inicio"
echo "=============================================="
echo ""

# Función para verificar si un comando existe
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Función para iniciar con Docker Compose
start_with_docker() {
    echo "🐳 Iniciando con Docker Compose..."
    
    if ! command_exists docker; then
        echo "❌ Error: Docker no está instalado"
        echo "   Instala Docker desde: https://docs.docker.com/get-docker/"
        exit 1
    fi
    
    if ! command_exists docker-compose; then
        echo "❌ Error: Docker Compose no está instalado"
        echo "   Instala Docker Compose desde: https://docs.docker.com/compose/install/"
        exit 1
    fi
    
    echo "📦 Construyendo y ejecutando contenedores..."
    docker-compose up --build -d
    
    echo ""
    echo "✅ Aplicación iniciada con Docker!"
    echo ""
    echo "🌐 URLs disponibles:"
    echo "   - Frontend: http://localhost:3000"
    echo "   - Backend API: http://localhost:8000"
    echo "   - API Docs: http://localhost:8000/docs"
    echo ""
    echo "📝 Ver logs:"
    echo "   docker-compose logs -f"
    echo ""
    echo "🛑 Para detener:"
    echo "   docker-compose down"
}

# Función para iniciar localmente sin Docker
start_local() {
    echo "💻 Iniciando localmente (sin Docker)..."
    echo ""
    
    # Verificar Python
    if ! command_exists python3; then
        echo "❌ Error: Python 3 no está instalado"
        exit 1
    fi
    
    # Verificar Node
    if ! command_exists node; then
        echo "❌ Error: Node.js no está instalado"
        exit 1
    fi
    
    # Verificar PostgreSQL
    if ! command_exists psql; then
        echo "⚠️  Advertencia: PostgreSQL no está instalado"
        echo "   El backend necesita PostgreSQL para funcionar"
        echo "   Instala PostgreSQL o usa Docker"
        echo ""
    fi
    
    echo "📦 Instalando dependencias del backend..."
    cd backend
    if [ ! -d "venv" ]; then
        python3 -m venv venv
    fi
    source venv/bin/activate
    pip install -q -r requirements.txt
    
    echo "📦 Instalando dependencias del frontend..."
    cd ../frontend
    npm install --silent
    
    echo ""
    echo "✅ Dependencias instaladas!"
    echo ""
    echo "🚀 Para iniciar los servicios:"
    echo ""
    echo "Backend (en una terminal):"
    echo "  cd backend"
    echo "  source venv/bin/activate"
    echo "  uvicorn main:app --reload --port 8000"
    echo ""
    echo "Frontend (en otra terminal):"
    echo "  cd frontend"
    echo "  npm run dev"
    echo ""
    echo "⚠️  IMPORTANTE: Asegúrate de tener PostgreSQL ejecutándose"
    echo "   y configurar las variables de entorno en backend/.env"
}

# Mostrar opciones
echo "Selecciona cómo quieres iniciar el proyecto:"
echo ""
echo "1) Con Docker Compose (recomendado)"
echo "2) Localmente (sin Docker)"
echo "3) Solo instalar dependencias"
echo ""
read -p "Opción (1-3): " option

case $option in
    1)
        start_with_docker
        ;;
    2)
        start_local
        ;;
    3)
        echo "📦 Instalando dependencias..."
        cd backend
        if [ ! -d "venv" ]; then
            python3 -m venv venv
        fi
        source venv/bin/activate
        pip install -r requirements.txt
        cd ../frontend
        npm install
        echo "✅ Dependencias instaladas!"
        ;;
    *)
        echo "❌ Opción no válida"
        exit 1
        ;;
esac

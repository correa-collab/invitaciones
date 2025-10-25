#!/bin/bash

# Script rápido para correr el proyecto localmente (sin Docker)
# Ejecuta backend y frontend simultáneamente

set -e

echo "🚀 Iniciando proyecto de invitaciones..."

# Verificar que estamos en el directorio correcto
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ Error: Ejecuta este script desde el directorio raíz del proyecto"
    exit 1
fi

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 no está instalado"
    exit 1
fi

# Verificar Node
if ! command -v node &> /dev/null; then
    echo "❌ Error: Node.js no está instalado"
    exit 1
fi

echo "📦 Instalando dependencias si es necesario..."

# Backend
if [ ! -d "backend/venv" ]; then
    echo "  - Creando entorno virtual de Python..."
    cd backend
    python3 -m venv venv
    source venv/bin/activate
    pip install -q -r requirements.txt
    cd ..
else
    echo "  - Backend ya configurado ✓"
fi

# Frontend
if [ ! -d "frontend/node_modules" ]; then
    echo "  - Instalando dependencias de Node..."
    cd frontend
    npm install --silent
    cd ..
else
    echo "  - Frontend ya configurado ✓"
fi

echo ""
echo "✅ Dependencias listas!"
echo ""
echo "🔧 Iniciando servicios..."
echo ""

# Función para limpiar procesos al salir
cleanup() {
    echo ""
    echo "🛑 Deteniendo servicios..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null || true
    exit 0
}

trap cleanup EXIT INT TERM

# Iniciar backend en segundo plano
echo "📡 Iniciando backend en http://localhost:8000"
cd backend
source venv/bin/activate
DATABASE_URL="sqlite:///./invitaciones.db" uvicorn main:app --reload --port 8000 > ../backend.log 2>&1 &
BACKEND_PID=$!
cd ..

# Esperar a que el backend esté listo
sleep 3

# Iniciar frontend en segundo plano
echo "🌐 Iniciando frontend en http://localhost:3000"
cd frontend
npm run dev > ../frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

# Esperar a que el frontend esté listo
sleep 5

echo ""
echo "✨ ¡Proyecto iniciado exitosamente!"
echo ""
echo "🌐 URLs disponibles:"
echo "   - Frontend:  http://localhost:3000"
echo "   - Backend:   http://localhost:8000"
echo "   - API Docs:  http://localhost:8000/docs"
echo ""
echo "📝 Ver logs:"
echo "   - Backend:   tail -f backend.log"
echo "   - Frontend:  tail -f frontend.log"
echo ""
echo "⚠️  NOTA: Usando SQLite en lugar de PostgreSQL para desarrollo rápido"
echo "   Para producción, configura PostgreSQL en backend/.env"
echo ""
echo "🛑 Presiona Ctrl+C para detener los servicios"
echo ""

# Mantener el script corriendo
wait

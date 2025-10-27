#!/bin/bash
# 🎓 Script de Inicio - Sistema de Invitaciones
# Universidad Panamericana

echo "🎓 Iniciando Sistema de Invitaciones"
echo "===================================="

# Verificar que existe el entorno virtual
if [ ! -d ".venv" ]; then
    echo "❌ Error: Entorno virtual no encontrado"
    echo "   Ejecuta primero: ./install.sh"
    exit 1
fi

# Activar entorno virtual
echo "🔌 Activando entorno virtual..."
source .venv/bin/activate

# Verificar archivo .env
if [ ! -f ".env" ]; then
    echo "⚠️  Advertencia: Archivo .env no encontrado"
    echo "   Copiando configuración de ejemplo..."
    cp .env.example .env
fi

# Verificar que el puerto esté libre
PORT=8000
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null ; then
    echo "⚠️  Puerto $PORT ocupado, liberando..."
    lsof -ti:$PORT | xargs kill -9 2>/dev/null
    sleep 2
fi

echo "🚀 Iniciando servidor en puerto $PORT..."
echo "   Presiona Ctrl+C para detener"
echo "===================================="

# Iniciar servidor
python backend/simple_main.py
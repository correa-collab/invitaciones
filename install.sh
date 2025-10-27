#!/bin/bash
# 🎓 Script de Instalación - Sistema de Invitaciones
# Universidad Panamericana

echo "🎓 Instalando Sistema de Invitaciones - Universidad Panamericana"
echo "=================================================="

# Verificar Python 3.8+
echo "📋 Verificando Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 no está instalado"
    echo "   Instala Python 3.8 o superior desde: https://python.org"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✅ Python $PYTHON_VERSION detectado"

# Crear entorno virtual
echo "🔧 Creando entorno virtual..."
python3 -m venv .venv

# Activar entorno virtual
echo "🔌 Activando entorno virtual..."
source .venv/bin/activate

# Actualizar pip
echo "⬆️  Actualizando pip..."
pip install --upgrade pip

# Instalar dependencias
echo "📦 Instalando dependencias..."
pip install -r requirements.txt

# Crear archivo .env si no existe
if [ ! -f .env ]; then
    echo "⚙️  Creando archivo de configuración..."
    cp .env.example .env
    echo "📝 IMPORTANTE: Edita el archivo .env con tu configuración"
fi

echo "=================================================="
echo "✅ ¡Instalación completada!"
echo ""
echo "🚀 Para iniciar el servidor:"
echo "   source .venv/bin/activate"
echo "   python backend/simple_main.py"
echo ""
echo "🌐 Luego abre: http://localhost:8000"
echo ""
echo "📧 Para configurar email, edita el archivo .env"
echo "=================================================="
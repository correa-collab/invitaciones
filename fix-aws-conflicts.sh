#!/bin/bash

echo "🔧 Resolviendo conflictos en el servidor AWS..."
echo "============================================="

# 1. Guardar cambios locales por si acaso
echo "💾 Guardando cambios locales..."
git stash push -m "Cambios locales antes de actualización - $(date)"

# 2. Forzar actualización desde GitHub
echo "📥 Descargando versión más reciente..."
git fetch origin
git reset --hard origin/main
git pull origin main

# 3. Verificar que los archivos estén presentes
echo "📋 Verificando archivos de deployment..."
ls -la deploy-aws-update.sh || echo "❌ deploy-aws-update.sh no encontrado"
ls -la docker-compose.production.yml || echo "❌ docker-compose.production.yml no encontrado"
ls -la nginx/nginx.conf || echo "❌ nginx.conf no encontrado"

# 4. Hacer ejecutables los scripts
echo "🔧 Configurando permisos..."
chmod +x deploy-aws-update.sh 2>/dev/null || echo "⚠️ deploy-aws-update.sh no encontrado"
chmod +x *.sh 2>/dev/null

# 5. Mostrar estado
echo "📊 Estado actual:"
git status
echo ""
echo "📁 Archivos en directorio:"
ls -la | grep -E "\.(sh|yml|conf)$"

echo ""
echo "🎯 Siguiente paso:"
echo "Si deploy-aws-update.sh existe, ejecuta: ./deploy-aws-update.sh"
echo "Si no existe, ejecuta los comandos manualmente"


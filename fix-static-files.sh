#!/bin/bash

echo "🔄 SOLUCIÓN ESPECÍFICA PARA ARCHIVOS ESTÁTICOS NO ACTUALIZADOS"
echo "=============================================================="

# 1. Parar todo completamente
echo "🛑 Parando todos los servicios..."
sudo docker-compose -f docker-compose.production.yml down -v
sudo docker system prune -f

# 2. Verificar que los archivos locales estén actualizados
echo "📋 Verificando archivos locales..."
echo "Confirmando que confirmation.html tenga las últimas mejoras:"
grep -n "Enviar por Correo" static/confirmation.html && echo "❌ PROBLEMA: Botón aún existe" || echo "✅ OK: Botón eliminado"

# 3. Forzar recreación completa
echo "🔨 Reconstruyendo completamente..."
sudo docker-compose -f docker-compose.production.yml build --no-cache

# 4. Ejecutar con volumes frescos
echo "🚀 Ejecutando con mapeo fresco de archivos..."
sudo docker-compose -f docker-compose.production.yml up -d

# 5. Esperar inicio
echo "⏱️ Esperando inicio de servicios..."
sleep 15

# 6. Verificar contenido actualizado
echo "🔍 Verificando que los archivos se sirvieron correctamente..."
sudo docker-compose -f docker-compose.production.yml ps

echo "📄 Verificando confirmation.html en el servidor:"
curl -s http://localhost/confirmation.html | grep -A5 -B5 "Descargar Pase" | head -10

echo "🌐 Probando URL externa:"
curl -s http://registro.iux.com.mx/confirmation.html | grep -A5 -B5 "Descargar Pase" | head -10

echo ""
echo "🎯 URLs para probar:"
echo "http://registro.iux.com.mx/confirmation.html"  
echo "http://3.140.201.39/confirmation.html"

echo ""
echo "✅ Si ves solo 'Descargar Pase' sin 'Enviar por Correo', está funcionando!"
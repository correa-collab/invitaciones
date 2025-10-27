#!/bin/bash

echo "🔍 VERIFICACIÓN COMPLETA DE LA PÁGINA ACTUALIZADA"
echo "==============================================="

echo "1. 🌐 Verificando conectividad..."
curl -s -I http://registro.iux.com.mx | head -5

echo ""
echo "2. 📄 Verificando confirmation.html..."
echo "Buscando botón 'Enviar por Correo' (NO debe aparecer):"
curl -s http://registro.iux.com.mx/confirmation.html | grep -i "enviar.*correo" && echo "❌ PROBLEMA: Botón aún presente" || echo "✅ OK: Botón eliminado"

echo ""
echo "Buscando botón 'Descargar Pase' (SÍ debe aparecer):"
curl -s http://registro.iux.com.mx/confirmation.html | grep -i "descargar.*pase" && echo "✅ OK: Botón presente" || echo "❌ PROBLEMA: Botón faltante"

echo ""
echo "3. 📧 Verificando funcionalidad de email automático..."
echo "Buscando código de email automático:"
curl -s http://registro.iux.com.mx/confirmation.html | grep -i "send-pass-email" && echo "✅ OK: Email automático presente" || echo "❌ PROBLEMA: Email automático faltante"

echo ""
echo "4. 📋 Verificando aviso de privacidad..."
curl -s http://registro.iux.com.mx/confirmation.html | grep -i "aviso.*privacidad" && echo "✅ OK: Aviso presente" || echo "❌ PROBLEMA: Aviso faltante"

echo ""
echo "5. 🎯 Verificando endpoints del backend..."
echo "Health check:"
curl -s http://registro.iux.com.mx/health | head -3 || echo "❌ Backend no responde"

echo ""
echo "6. 📊 Resumen del estado:"
echo "================================="
if curl -s http://registro.iux.com.mx/confirmation.html | grep -q "Descargar Pase"; then
    if ! curl -s http://registro.iux.com.mx/confirmation.html | grep -q "Enviar por Correo"; then
        echo "🎉 ¡PERFECTO! La página está actualizada correctamente"
        echo "✅ Solo tiene el botón de Descargar Pase"
        echo "✅ No tiene el botón de Enviar por Correo"
    else
        echo "⚠️ PARCIAL: Página tiene ambos botones"
    fi
else
    echo "❌ PROBLEMA: Página no actualizada o no accesible"
fi

echo ""
echo "🌐 URLs para probar manualmente:"
echo "- Principal: http://registro.iux.com.mx"
echo "- Confirmación: http://registro.iux.com.mx/confirmation.html"
echo "- Health: http://registro.iux.com.mx/health"
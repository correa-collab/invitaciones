#!/usr/bin/env python3
"""
Script de prueba para verificar que el email funciona correctamente
"""

import asyncio
import sys
import os

# Agregar el directorio actual al path
sys.path.append('/Users/christian/Invitaciones/backend')

from email_service import email_service

async def test_email():
    print("🧪 Probando configuración de email...")
    print("=" * 60)
    
    # Datos de prueba
    test_email = "correa@iux.com.mx"  # Enviar a ti mismo para la prueba
    test_name = "Christian Correa (Prueba)"
    
    event_details = {
        "email": test_email,
        "attending": True,
        "companions": 1,
        "whatsapp": "+52 33 1234 5678",
        "confirmed_at": "26/10/2025 15:04"
    }
    
    try:
        print(f"📧 Enviando email de prueba a: {test_email}")
        print("⏳ Espera un momento...")
        
        result = await email_service.send_confirmation_email(
            to_email=test_email,
            guest_name=test_name,
            event_details=event_details
        )
        
        if result["success"]:
            print("✅ ¡EMAIL ENVIADO EXITOSAMENTE!")
            print(f"📬 Revisa tu bandeja de entrada: {test_email}")
            print("🎉 La configuración está funcionando correctamente")
        else:
            print("❌ Error enviando email:")
            print(f"   {result['message']}")
            
    except Exception as e:
        print(f"❌ Error en la prueba: {str(e)}")
        print("\n🔍 Posibles soluciones:")
        print("1. Verifica que el email sea correcto")
        print("2. Verifica que la contraseña de aplicación sea correcta")
        print("3. Asegúrate de que la verificación en 2 pasos esté activada")

if __name__ == "__main__":
    asyncio.run(test_email())
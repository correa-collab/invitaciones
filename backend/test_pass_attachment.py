#!/usr/bin/env python3
"""
Script de prueba para verificar la generación y adjunto de pases
"""

import asyncio
import sys
import os

# Agregar el directorio actual al path
sys.path.append('/Users/christian/Invitaciones/backend')

from email_service import email_service
from pass_generator import pass_generator

async def test_pass_attachment():
    print("🧪 Probando generación y adjunto de pase de acceso...")
    print("=" * 70)
    
    # Datos de prueba
    test_email = "correa@iux.com.mx"
    test_name = "Christian Correa"
    test_folio = "AW-TEST-001"
    
    try:
        # 1. Generar imagen del pase
        print("🎨 Generando imagen del pase...")
        pass_image = pass_generator.generate_pass_image(
            name=test_name,
            folio=test_folio,
            companions=2,
            whatsapp="+52 33 1234 5678"
        )
        
        if pass_image:
            print("✅ Imagen del pase generada exitosamente")
            print(f"📏 Tamaño del base64: {len(pass_image)} caracteres")
        else:
            print("❌ Error generando imagen del pase")
            return
        
        # 2. Preparar detalles del evento
        event_details = {
            "email": test_email,
            "attending": True,
            "companions": 2,
            "whatsapp": "+52 33 1234 5678",
            "confirmed_at": "26/10/2025 15:30"
        }
        
        # 3. Enviar email con pase adjunto
        print("📧 Enviando email con pase adjunto...")
        
        result = await email_service.send_confirmation_email(
            to_email=test_email,
            guest_name=test_name,
            event_details=event_details,
            pass_image_base64=pass_image
        )
        
        if result["success"]:
            print("✅ ¡EMAIL CON PASE ADJUNTO ENVIADO EXITOSAMENTE!")
            print(f"📬 Revisa tu bandeja: {test_email}")
            print("🎫 El pase de acceso está adjunto como archivo PNG")
            print("📱 Puedes descargarlo y usarlo en tu dispositivo")
        else:
            print("❌ Error enviando email:")
            print(f"   {result['message']}")
            
    except Exception as e:
        print(f"❌ Error en la prueba: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_pass_attachment())
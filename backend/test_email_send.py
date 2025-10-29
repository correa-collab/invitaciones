"""
Script de prueba para verificar envío de emails
"""
import asyncio
import sys
import os

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(__file__))

from email_service import email_service

async def test_email():
    """Prueba de envío de email con datos de ejemplo"""
    
    print("\n🧪 Iniciando prueba de envío de email...")
    print("-" * 60)
    
    # Datos de prueba
    test_data = {
        "to_email": "correa@iux.com.mx",
        "guest_name": "Christian Correa (PRUEBA)",
        "event_details": {
            "email": "correa@iux.com.mx",
            "attending": True,
            "companions": 2,
            "whatsapp": "+52 33 1234 5678",
            "confirmed_at": "29/10/2025 14:30"
        }
    }
    
    print(f"📧 Enviando email a: {test_data['to_email']}")
    print(f"👤 Nombre: {test_data['guest_name']}")
    print("-" * 60)
    
    # Enviar email sin adjunto (prueba básica)
    result = await email_service.send_confirmation_email(
        to_email=test_data["to_email"],
        guest_name=test_data["guest_name"],
        event_details=test_data["event_details"]
    )
    
    print("\n📋 Resultado:")
    print("-" * 60)
    if result["success"]:
        print("✅ EMAIL ENVIADO EXITOSAMENTE")
        print(f"   Mensaje: {result['message']}")
    else:
        print("❌ ERROR AL ENVIAR EMAIL")
        print(f"   Error: {result['message']}")
    
    print("-" * 60)
    return result["success"]

if __name__ == "__main__":
    success = asyncio.run(test_email())
    sys.exit(0 if success else 1)

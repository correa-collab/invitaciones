#!/usr/bin/env python3
"""
Script de configuración para el envío de correos electrónicos
Ejecutar este script para configurar las credenciales de email
"""

import os
from pathlib import Path

def setup_email_config():
    print("🔧 Configuración de Email para Sistema de Invitaciones")
    print("=" * 60)
    
    print("\n📧 OPCIÓN 1: Gmail (Recomendado para pruebas)")
    print("Para usar Gmail necesitas:")
    print("1. Ir a tu cuenta de Google")
    print("2. Seguridad > Verificación en 2 pasos (debe estar activada)")
    print("3. Seguridad > Contraseñas de aplicaciones")
    print("4. Generar una contraseña para 'Correo'")
    print("5. Usar esa contraseña de 16 caracteres aquí")
    
    print("\n📧 OPCIÓN 2: SendGrid (Recomendado para producción)")
    print("1. Crear cuenta en sendgrid.com")
    print("2. Obtener API Key")
    print("3. Configurar dominio verificado")
    
    print("\n" + "=" * 60)
    
    choice = input("\n¿Qué servicio quieres configurar? (1=Gmail, 2=SendGrid, 0=Salir): ")
    
    if choice == "1":
        setup_gmail()
    elif choice == "2":
        setup_sendgrid()
    else:
        print("👋 Configuración cancelada")
        return

def setup_gmail():
    print("\n🔐 Configuración de Gmail")
    print("-" * 30)
    
    email = input("Ingresa tu email de Gmail: ")
    
    print("\n⚠️  IMPORTANTE: No uses tu contraseña normal de Gmail")
    print("Debes usar una 'Contraseña de aplicación' generada desde tu cuenta de Google")
    print("Ejemplo: abcd efgh ijkl mnop (16 caracteres)")
    
    password = input("Ingresa tu contraseña de aplicación: ")
    
    if not email or not password:
        print("❌ Email y contraseña son requeridos")
        return
    
    # Actualizar archivo .env
    env_path = Path(__file__).parent / ".env"
    
    try:
        # Leer archivo existente
        content = ""
        if env_path.exists():
            with open(env_path, 'r') as f:
                content = f.read()
        
        # Actualizar valores
        lines = content.split('\n')
        updated_lines = []
        
        email_updated = False
        password_updated = False
        
        for line in lines:
            if line.startswith('SMTP_EMAIL='):
                updated_lines.append(f'SMTP_EMAIL={email}')
                email_updated = True
            elif line.startswith('SMTP_PASSWORD='):
                updated_lines.append(f'SMTP_PASSWORD={password}')
                password_updated = True
            elif line.startswith('EMAIL_USER='):
                updated_lines.append(f'EMAIL_USER={email}')
            elif line.startswith('EMAIL_PASSWORD='):
                updated_lines.append(f'EMAIL_PASSWORD={password}')
            else:
                updated_lines.append(line)
        
        # Agregar si no existían
        if not email_updated:
            updated_lines.append(f'SMTP_EMAIL={email}')
        if not password_updated:
            updated_lines.append(f'SMTP_PASSWORD={password}')
        
        # Escribir archivo
        with open(env_path, 'w') as f:
            f.write('\n'.join(updated_lines))
        
        print(f"\n✅ Configuración guardada en {env_path}")
        print("🚀 Ahora puedes reiniciar el servidor para aplicar los cambios")
        
        # Hacer prueba de envío
        test = input("\n¿Quieres hacer una prueba de envío? (s/n): ")
        if test.lower() == 's':
            test_email_send(email, password)
            
    except Exception as e:
        print(f"❌ Error guardando configuración: {e}")

def setup_sendgrid():
    print("\n📮 Configuración de SendGrid")
    print("-" * 30)
    print("Esta función estará disponible próximamente")
    print("Por ahora usa Gmail para las pruebas")

def test_email_send(email, password):
    print("\n🧪 Prueba de envío de correo...")
    
    test_recipient = input("Email de prueba para enviar: ")
    if not test_recipient:
        print("❌ Email requerido para la prueba")
        return
    
    try:
        import smtplib
        import ssl
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        
        # Crear mensaje de prueba
        message = MIMEMultipart("alternative")
        message["Subject"] = "🧪 Prueba - Sistema de Invitaciones"
        message["From"] = email
        message["To"] = test_recipient
        
        html_content = """
        <html>
        <body>
            <h2>🎉 ¡Prueba exitosa!</h2>
            <p>Si recibes este correo, significa que la configuración de email está funcionando correctamente.</p>
            <p><strong>Sistema de Invitaciones - Posgrado en TIC's</strong></p>
            <p><small>IUX - Software Jurídico</small></p>
        </body>
        </html>
        """
        
        html_part = MIMEText(html_content, "html")
        message.attach(html_part)
        
        # Enviar
        context = ssl.create_default_context()
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls(context=context)
            server.login(email, password)
            server.send_message(message)
        
        print("✅ ¡Email de prueba enviado exitosamente!")
        print(f"📬 Revisa la bandeja de entrada de {test_recipient}")
        
    except Exception as e:
        print(f"❌ Error en la prueba: {e}")
        print("\n🔍 Posibles soluciones:")
        print("1. Verifica que el email y contraseña sean correctos")
        print("2. Asegúrate de usar una 'contraseña de aplicación', no tu contraseña normal")
        print("3. Verifica que la verificación en 2 pasos esté activada en tu cuenta de Google")

if __name__ == "__main__":
    setup_email_config()
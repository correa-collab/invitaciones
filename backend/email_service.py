import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
from typing import Optional
import base64
from io import BytesIO
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class EmailService:
    def __init__(self):
        # Importar configuración local
        try:
            from email_config import EMAIL_CONFIG
            self.smtp_server = EMAIL_CONFIG["smtp_server"]
            self.smtp_port = EMAIL_CONFIG["smtp_port"]
            self.email = EMAIL_CONFIG["email"]
            self.password = EMAIL_CONFIG["password"]
        except ImportError:
            # Fallback a variables de entorno
            self.smtp_server = "smtp.gmail.com"
            self.smtp_port = 587
            self.email = os.getenv("SMTP_EMAIL", "tu-email@gmail.com")
            self.password = os.getenv("SMTP_PASSWORD", "tu-contraseña-de-aplicacion")
        
    async def send_confirmation_email(self, to_email: str, guest_name: str, 
                                    event_details: dict, pass_image_base64: Optional[str] = None):
        """
        Envía email de confirmación con el pase de acceso
        """
        try:
            # Crear mensaje
            message = MIMEMultipart("alternative")
            message["Subject"] = "✅ Confirmación de Asistencia - Posgrado en TIC's"
            message["From"] = self.email
            message["To"] = to_email
            
            # Crear contenido HTML
            html_content = self._create_email_html(guest_name, event_details)
            
            # Adjuntar contenido HTML
            html_part = MIMEText(html_content, "html")
            message.attach(html_part)
            
            # Adjuntar imagen del pase si está disponible
            if pass_image_base64:
                self._attach_pass_image(message, pass_image_base64, guest_name)
            
            # Enviar email
            context = ssl.create_default_context()
            # Solución para macOS - deshabilitar verificación SSL si es necesario
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.email, self.password)
                server.send_message(message)
                
            return {"success": True, "message": "Email enviado exitosamente"}
            
        except Exception as e:
            print(f"Error enviando email: {str(e)}")
            return {"success": False, "message": f"Error enviando email: {str(e)}"}
    
    def _create_email_html(self, guest_name: str, event_details: dict) -> str:
        """
        Crea el contenido HTML del email
        """
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }}
                .container {{ max-width: 600px; margin: 0 auto; background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
                .header {{ background: linear-gradient(135deg, #B8860B, #DAA520); color: white; padding: 30px; text-align: center; }}
                .content {{ padding: 30px; }}
                .confirmation-badge {{ background: #22C55E; color: white; padding: 10px 20px; border-radius: 25px; display: inline-block; margin: 20px 0; }}
                .details {{ background: #f9f9f9; padding: 20px; border-radius: 8px; margin: 20px 0; }}
                .detail-item {{ margin: 10px 0; display: flex; align-items: center; }}
                .icon {{ margin-right: 10px; font-size: 18px; }}
                .footer {{ background: #f9f9f9; padding: 20px; text-align: center; color: #666; }}
                .button {{ background: #B8860B; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; display: inline-block; margin: 10px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🎓 Posgrado en TIC's</h1>
                    <h2>¡Confirmación de Asistencia!</h2>
                </div>
                
                <div class="content">
                    <div class="confirmation-badge">
                        ✅ Tu confirmación se guardó exitosamente
                    </div>
                    
                    <p>Estimado/a <strong>{guest_name}</strong>,</p>
                    
                    <p>¡Excelente! Hemos recibido tu confirmación de asistencia para nuestro evento del Posgrado en TIC's.</p>
                    
                    <div class="details">
                        <h3>📋 Datos de tu confirmación:</h3>
                        <div class="detail-item">
                            <span class="icon">👤</span>
                            <strong>Nombre:</strong> {guest_name}
                        </div>
                        <div class="detail-item">
                            <span class="icon">📧</span>
                            <strong>Email:</strong> {event_details.get('email', 'No especificado')}
                        </div>
                        <div class="detail-item">
                            <span class="icon">✅</span>
                            <strong>Asistencia:</strong> {'SÍ ASISTIRÉ' if event_details.get('attending') else 'NO ASISTIRÉ'}
                        </div>
                        <div class="detail-item">
                            <span class="icon">👥</span>
                            <strong>Acompañantes:</strong> {event_details.get('companions', 0)}
                        </div>
                        <div class="detail-item">
                            <span class="icon">📱</span>
                            <strong>WhatsApp:</strong> {event_details.get('whatsapp', 'No especificado')}
                        </div>
                        <div class="detail-item">
                            <span class="icon">🕐</span>
                            <strong>Confirmado:</strong> {event_details.get('confirmed_at', 'Ahora')}
                        </div>
                    </div>
                    
                    <div style="background: #f0f9ff; padding: 15px; border-radius: 8px; border-left: 4px solid #3b82f6; margin: 20px 0;">
                        <p><strong>📎 PASE DE ACCESO ADJUNTO</strong></p>
                        <p>Hemos adjuntado tu pase de acceso oficial como archivo PNG a este correo.</p>
                    </div>
                    
                    <p>🎯 <strong>Información importante:</strong></p>
                    <ul>
                        <li><strong>📎 Descarga el archivo adjunto</strong> "pase_acceso_[tu_nombre].png"</li>
                        <li><strong>📱 Presenta el pase</strong> el día del evento (impreso o digital)</li>
                        <li><strong>✅ Guarda el archivo</strong> en tu dispositivo móvil para fácil acceso</li>
                        <li><strong>❓ Dudas:</strong> Contacta a la persona que te envió la invitación</li>
                    </ul>
                    
                    <p>¡Te esperamos en este importante evento del Posgrado en TIC's!</p>
                </div>
                
                <div class="footer">
                    <p><small>Sistema de invitaciones desarrollado por <strong>IUX - Software Jurídico</strong></small></p>
                    <p><small>Este es un mensaje automático, por favor no responder a este correo.</small></p>
                </div>
            </div>
        </body>
        </html>
        """
    
    def _attach_pass_image(self, message: MIMEMultipart, image_base64: str, guest_name: str):
        """
        Adjunta la imagen del pase de acceso al email
        """
        try:
            # Decodificar imagen base64
            if ',' in image_base64:
                image_data = base64.b64decode(image_base64.split(',')[1])
            else:
                image_data = base64.b64decode(image_base64)
            
            # Crear adjunto como imagen PNG
            attachment = MIMEBase('image', 'png')
            attachment.set_payload(image_data)
            encoders.encode_base64(attachment)
            
            # Nombre del archivo limpio (solo ASCII)
            import unicodedata
            # Normalizar y remover acentos
            normalized_name = unicodedata.normalize('NFKD', guest_name)
            ascii_name = normalized_name.encode('ASCII', 'ignore').decode('ASCII')
            safe_name = "".join(c for c in ascii_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
            filename = f"pase_acceso_{safe_name.replace(' ', '_')}.png"
            
            # Usar codificación RFC 2231 para nombres de archivo con caracteres especiales
            attachment.add_header(
                'Content-Disposition',
                'attachment',
                filename=('utf-8', '', filename)
            )
            
            # También agregar Content-ID para mostrar inline si es necesario
            attachment.add_header('Content-ID', '<pass_image>')
            
            message.attach(attachment)
            print(f"📎 Pase adjuntado: {filename}")
            
        except Exception as e:
            print(f"❌ Error adjuntando imagen: {str(e)}")
            # No fallar el email si el adjunto falla

# Instancia global del servicio
email_service = EmailService()
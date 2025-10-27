from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from pydantic import BaseModel, EmailStr
from typing import List, Optional
import os
import uuid
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from datetime import datetime
import base64
import io
import logging
from email_service import email_service
from pass_generator import pass_generator

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Sistema de Invitaciones - Universidad Panamericana",
    version="1.0.0",
    description="Sistema de gestión de invitaciones con colorimetría UP"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="/Users/christian/Invitaciones/static"), name="static")

# Simple data store (in production, use a real database)
invitations_db = []
confirmations_db = [
    {
        "id": 1,
        "folio": "AW-234",
        "name": "María González López", 
        "email": "maria.gonzalez@email.com",
        "phone": "+52 33 1234 5678",
        "will_attend": True,
        "guests": 2,
        "timestamp": "2025-10-20T10:30:00.000Z",
        "qr_url": "https://registro.iux.com.mx/confirmation/AW-234"
    },
    {
        "id": 2,
        "folio": "AW-235",
        "name": "Juan Carlos Pérez",
        "email": "juan.perez@email.com", 
        "phone": "+52 33 8765 4321",
        "will_attend": True,
        "guests": 1,
        "timestamp": "2025-10-21T14:15:00.000Z",
        "qr_url": "https://registro.iux.com.mx/confirmation/AW-235"
    },
    {
        "id": 3,
        "folio": "",
        "name": "Ana María Rodríguez",
        "email": "ana.rodriguez@email.com",
        "phone": "+52 33 9876 5432", 
        "will_attend": False,
        "guests": 0,
        "timestamp": "2025-10-22T09:45:00.000Z",
        "qr_url": None
    },
    {
        "id": 4,
        "folio": "AW-236", 
        "name": "Luis Fernando Sánchez",
        "email": "luis.sanchez@email.com",
        "phone": "+52 33 2468 1357",
        "will_attend": True,
        "guests": 3,
        "timestamp": "2025-10-23T16:20:00.000Z",
        "qr_url": "https://registro.iux.com.mx/confirmation/AW-236"
    }
]
events_db = [
    {
        "id": 1,
        "title": "Fiesta de Finalización del Posgrado",
        "description": "Posgrado en Derecho de las Tecnologías de la Información",
        "date": "2025-11-14",
        "time": "17:00",
        "location": "Ciudad Granja, Posgrado en TIC's"
    }
]

# Pydantic models
class InvitationCreate(BaseModel):
    event_id: int
    guest_name: str
    guest_email: EmailStr

class InvitationResponse(BaseModel):
    id: int
    event_id: int
    guest_name: str
    guest_email: str
    event_title: str

class ConfirmationCreate(BaseModel):
    name: str
    email: EmailStr
    will_attend: bool
    guests: int = 0
    phone: str
    pass_image_base64: Optional[str] = None  # Imagen del pase generada en el frontend

class ConfirmationResponse(BaseModel):
    id: int
    folio: str
    name: str
    email: str
    will_attend: bool
    guests: int
    phone: str
    timestamp: str
    qr_url: Optional[str] = None

@app.get("/", response_class=HTMLResponse)
async def root():
    return FileResponse("/Users/christian/Invitaciones/static/index.html")

@app.get("/confirmation.html", response_class=HTMLResponse)
async def confirmation_page():
    return FileResponse("/Users/christian/Invitaciones/static/confirmation.html")

@app.get("/admin.html", response_class=HTMLResponse)
async def admin_page():
    return FileResponse("/Users/christian/Invitaciones/static/admin.html")

@app.get("/dashboard.html", response_class=HTMLResponse)
async def dashboard_page():
    return HTMLResponse("""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard - Universidad Panamericana</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        'up-gold': {
                            50: '#fefdf8',
                            100: '#fdf9e9',
                            200: '#fbf0c5',
                            300: '#f8e298',
                            400: '#f4cc5a',
                            500: '#f0b429',
                            600: '#d4950f',
                            700: '#b37b0d',
                            800: '#8f5e14',
                            900: '#744f16',
                        }
                    }
                }
            }
        }
    </script>
</head>
<body class="min-h-screen bg-gradient-to-br from-up-gold-50 to-up-gold-100">
    <nav class="bg-white shadow-sm border-b border-up-gold-200">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between h-16">
                <div class="flex items-center">
                    <div class="w-10 h-10 bg-gradient-to-br from-up-gold-600 to-up-gold-700 rounded-lg flex items-center justify-center mr-3">
                        <span class="text-white font-bold text-lg">UP</span>
                    </div>
                    <h1 class="text-xl font-semibold text-up-gold-800">Dashboard</h1>
                </div>
                <div class="flex items-center space-x-4">
                    <a href="/" class="text-up-gold-700 hover:text-up-gold-800 font-medium">Inicio</a>
                    <a href="/events.html" class="text-up-gold-700 hover:text-up-gold-800 font-medium">Eventos</a>
                </div>
            </div>
        </div>
    </nav>

    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div class="px-4 py-6 sm:px-0">
            <div class="border-4 border-dashed border-up-gold-200 rounded-lg h-96 p-8">
                <div class="text-center">
                    <div class="w-24 h-24 bg-gradient-to-br from-up-gold-600 to-up-gold-700 rounded-full flex items-center justify-center mx-auto mb-6">
                        <span class="text-white font-bold text-3xl">UP</span>
                    </div>
                    <h2 class="text-3xl font-bold text-up-gold-800 mb-4">Panel de Administración</h2>
                    <p class="text-gray-600 mb-8">Gestiona tus eventos e invitaciones desde aquí</p>
                    
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-4xl mx-auto">
                        <div class="bg-white p-6 rounded-lg shadow-md border border-up-gold-200">
                            <h3 class="text-lg font-semibold text-up-gold-800 mb-2">Eventos</h3>
                            <p class="text-gray-600 mb-4">Crear y gestionar eventos</p>
                            <button onclick="loadEvents()" class="bg-gradient-to-r from-up-gold-600 to-up-gold-700 text-white px-4 py-2 rounded-md hover:from-up-gold-700 hover:to-up-gold-800 font-medium">
                                Ver Eventos
                            </button>
                        </div>
                        
                        <div class="bg-white p-6 rounded-lg shadow-md border border-up-gold-200">
                            <h3 class="text-lg font-semibold text-up-gold-800 mb-2">Invitaciones</h3>
                            <p class="text-gray-600 mb-4">Enviar y gestionar invitaciones</p>
                            <button onclick="loadInvitations()" class="bg-gradient-to-r from-up-gold-600 to-up-gold-700 text-white px-4 py-2 rounded-md hover:from-up-gold-700 hover:to-up-gold-800 font-medium">
                                Ver Invitaciones
                            </button>
                        </div>
                        
                        <div class="bg-white p-6 rounded-lg shadow-md border border-up-gold-200">
                            <h3 class="text-lg font-semibold text-up-gold-800 mb-2">Confirmaciones</h3>
                            <p class="text-gray-600 mb-4">Ver respuestas de invitados</p>
                            <button onclick="loadConfirmations()" class="bg-gradient-to-r from-up-gold-600 to-up-gold-700 text-white px-4 py-2 rounded-md hover:from-up-gold-700 hover:to-up-gold-800 font-medium">
                                Ver Confirmaciones
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </main>

    <script>
        async function loadEvents() {
            try {
                const response = await fetch('/api/events');
                const data = await response.json();
                alert('Eventos cargados: ' + JSON.stringify(data, null, 2));
            } catch (error) {
                alert('Error al cargar eventos: ' + error.message);
            }
        }

        async function loadInvitations() {
            try {
                const response = await fetch('/api/invitations');
                const data = await response.json();
                alert('Invitaciones: ' + JSON.stringify(data, null, 2));
            } catch (error) {
                alert('Error al cargar invitaciones: ' + error.message);
            }
        }

        async function loadConfirmations() {
            alert('Funcionalidad de confirmaciones en desarrollo');
        }
    </script>
</body>
</html>
    """)

@app.get("/events.html", response_class=HTMLResponse)
async def events_page():
    return HTMLResponse("""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Eventos - Universidad Panamericana</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        'up-gold': {
                            50: '#fefdf8',
                            100: '#fdf9e9',
                            200: '#fbf0c5',
                            300: '#f8e298',
                            400: '#f4cc5a',
                            500: '#f0b429',
                            600: '#d4950f',
                            700: '#b37b0d',
                            800: '#8f5e14',
                            900: '#744f16',
                        }
                    }
                }
            }
        }
    </script>
</head>
<body class="min-h-screen bg-gradient-to-br from-up-gold-50 to-up-gold-100">
    <nav class="bg-white shadow-sm border-b border-up-gold-200">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between h-16">
                <div class="flex items-center">
                    <div class="w-10 h-10 bg-gradient-to-br from-up-gold-600 to-up-gold-700 rounded-lg flex items-center justify-center mr-3">
                        <span class="text-white font-bold text-lg">UP</span>
                    </div>
                    <h1 class="text-xl font-semibold text-up-gold-800">Eventos</h1>
                </div>
                <div class="flex items-center space-x-4">
                    <a href="/" class="text-up-gold-700 hover:text-up-gold-800 font-medium">Inicio</a>
                    <a href="/dashboard.html" class="text-up-gold-700 hover:text-up-gold-800 font-medium">Dashboard</a>
                </div>
            </div>
        </div>
    </nav>

    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div class="bg-white rounded-lg shadow-lg p-6 border border-up-gold-200">
            <h2 class="text-2xl font-bold text-up-gold-800 mb-6">Gestión de Eventos</h2>
            
            <div id="events-list" class="space-y-4">
                <div class="border border-up-gold-200 rounded-lg p-4">
                    <h3 class="text-lg font-semibold text-up-gold-800">Graduación Universidad Panamericana</h3>
                    <p class="text-gray-600">Ceremonia de graduación de la clase 2025</p>
                    <p class="text-sm text-gray-500">Fecha: 15 de Diciembre, 2025</p>
                    <p class="text-sm text-gray-500">Ubicación: Auditorio Principal, Campus UP</p>
                    <div class="mt-4">
                        <button onclick="createInvitation(1)" class="bg-gradient-to-r from-up-gold-600 to-up-gold-700 text-white px-4 py-2 rounded-md hover:from-up-gold-700 hover:to-up-gold-800 font-medium mr-2">
                            Enviar Invitación
                        </button>
                        <a href="/confirmation.html" class="bg-gradient-to-r from-gray-500 to-gray-600 text-white px-4 py-2 rounded-md hover:from-gray-600 hover:to-gray-700 font-medium">
                            Ver Confirmaciones
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </main>

    <script>
        function createInvitation(eventId) {
            const name = prompt('Nombre del invitado:');
            const email = prompt('Email del invitado:');
            
            if (name && email) {
                fetch('/api/invitations', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        event_id: eventId,
                        guest_name: name,
                        guest_email: email
                    })
                })
                .then(response => response.json())
                .then(data => {
                    alert('¡Invitación creada exitosamente!\\nID: ' + data.id);
                })
                .catch(error => {
                    alert('Error al crear invitación: ' + error.message);
                });
            }
        }
    </script>
</body>
</html>
    """)

@app.get("/api/events")
async def get_events():
    return {"events": events_db}

@app.get("/api/invitations", response_model=List[InvitationResponse])
async def get_invitations():
    result = []
    for inv in invitations_db:
        event = next((e for e in events_db if e["id"] == inv["event_id"]), None)
        result.append(InvitationResponse(
            id=inv["id"],
            event_id=inv["event_id"],
            guest_name=inv["guest_name"],
            guest_email=inv["guest_email"],
            event_title=event["title"] if event else "Evento no encontrado"
        ))
    return result

@app.post("/api/invitations", response_model=InvitationResponse)
async def create_invitation(invitation: InvitationCreate):
    # Check if event exists
    event = next((e for e in events_db if e["id"] == invitation.event_id), None)
    if not event:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    
    # Create invitation
    new_invitation = {
        "id": len(invitations_db) + 1,
        "event_id": invitation.event_id,
        "guest_name": invitation.guest_name,
        "guest_email": invitation.guest_email
    }
    
    invitations_db.append(new_invitation)
    
    return InvitationResponse(
        id=new_invitation["id"],
        event_id=new_invitation["event_id"],
        guest_name=new_invitation["guest_name"],
        guest_email=new_invitation["guest_email"],
        event_title=event["title"]
    )

@app.get("/api/confirmations")
async def get_confirmations():
    return confirmations_db

@app.get("/confirmation/{folio}", response_class=HTMLResponse)
async def view_confirmation(folio: str):
    """Mostrar confirmación individual por folio (para QR)"""
    # Buscar confirmación por folio
    confirmation = None
    for conf in confirmations_db:
        if conf.get("folio") == folio:
            confirmation = conf
            break
    
    if not confirmation:
        return HTMLResponse("""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Confirmación no encontrada</title>
            <script src="https://cdn.tailwindcss.com"></script>
        </head>
        <body class="bg-red-50 min-h-screen flex items-center justify-center">
            <div class="text-center">
                <div class="text-6xl mb-4">❌</div>
                <h1 class="text-2xl font-bold text-red-800 mb-4">Confirmación no encontrada</h1>
                <p class="text-red-600">El folio proporcionado no existe en nuestros registros.</p>
                <a href="/" class="mt-4 inline-block bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700">
                    Ir al inicio
                </a>
            </div>
        </body>
        </html>
        """)
    
    # Formatear fecha
    fecha = datetime.fromisoformat(confirmation["timestamp"]).strftime("%d/%m/%Y %H:%M")
    
    return HTMLResponse(f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Confirmación {confirmation["folio"]}</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <script>
            tailwind.config = {{
                theme: {{
                    extend: {{
                        colors: {{
                            'up-gold': {{
                                50: '#fefdf8',
                                100: '#fdf9e9', 
                                200: '#fbf0c5',
                                600: '#d4950f',
                                700: '#b37b0d',
                                800: '#8f5e14'
                            }}
                        }}
                    }}
                }}
            }}
        </script>
    </head>
    <body class="bg-gradient-to-br from-up-gold-50 to-up-gold-100 min-h-screen">
        <div class="container mx-auto px-4 py-8">
            <div class="max-w-2xl mx-auto bg-white rounded-lg shadow-lg p-8 border border-up-gold-200">
                <div class="text-center mb-6">
                    <div class="w-16 h-16 bg-gradient-to-br from-up-gold-600 to-up-gold-700 rounded-full flex items-center justify-center mx-auto mb-4">
                        <span class="text-white font-bold text-2xl" style="filter: brightness(0) invert(1);">🎓</span>
                    </div>
                    <h1 class="text-3xl font-bold text-up-gold-800 mb-2">Posgrado en TIC's</h1>
                    <p class="text-up-gold-600">Celebración de Finalización</p>
                </div>
                
                <div class="bg-up-gold-50 p-6 rounded-lg border border-up-gold-200 mb-6">
                    <h2 class="text-xl font-bold text-up-gold-800 mb-4 text-center">
                        {"✅ CONFIRMACIÓN DE ASISTENCIA" if confirmation["will_attend"] else "❌ NO ASISTENCIA"}
                    </h2>
                    
                    <div class="space-y-3">
                        <div class="flex justify-between">
                            <span class="font-semibold">📋 Folio:</span>
                            <span class="font-mono bg-gray-100 px-2 py-1 rounded">{confirmation["folio"]}</span>
                        </div>
                        <div class="flex justify-between">
                            <span class="font-semibold">👤 Nombre:</span>
                            <span>{confirmation["name"]}</span>
                        </div>
                        <div class="flex justify-between">
                            <span class="font-semibold">📧 Email:</span>
                            <span>{confirmation["email"]}</span>
                        </div>
                        <div class="flex justify-between">
                            <span class="font-semibold">✅ Asistencia:</span>
                            <span class="{"text-green-600 font-semibold" if confirmation["will_attend"] else "text-red-600 font-semibold"}">
                                {"SÍ ASISTIRÉ" if confirmation["will_attend"] else "NO PODRÉ ASISTIR"}
                            </span>
                        </div>
                        {"<div class='flex justify-between'><span class='font-semibold'>👥 Acompañantes:</span><span>" + str(confirmation["guests"]) + "</span></div>" if confirmation["will_attend"] else ""}
                        <div class="flex justify-between">
                            <span class="font-semibold">📱 WhatsApp:</span>
                            <span>{confirmation["phone"]}</span>
                        </div>
                        <div class="flex justify-between">
                            <span class="font-semibold">⏰ Confirmado:</span>
                            <span>{fecha}</span>
                        </div>
                    </div>
                </div>
                
                {"<div class='text-center'><p class='text-sm text-gray-600 mb-4'>🎫 Este es tu pase de acceso válido</p><p class='text-xs text-gray-500'>Recibirás la ubicación exacta vía WhatsApp</p></div>" if confirmation["will_attend"] else "<div class='text-center'><p class='text-sm text-gray-600'>Gracias por tu respuesta</p></div>"}
                
                <div class="text-center mt-6">
                    <a href="/" class="bg-up-gold-600 text-white px-6 py-2 rounded hover:bg-up-gold-700 transition duration-200">
                        🏠 Ir al inicio
                    </a>
                </div>
            </div>
        </div>
        
        <footer class="text-center py-4 text-sm text-gray-500">
            <p>Sistema desarrollado por <a href="https://iux.com.mx" class="text-blue-600 hover:text-blue-800">IUX - Software Jurídico</a></p>
        </footer>
    </body>
    </html>
    """)

@app.post("/api/send-email")
async def send_email_endpoint(data: dict):
    """Enviar confirmación por email"""
    try:
        folio = data.get("folio")
        email = data.get("email")
        name = data.get("name")
        
        if not all([folio, email, name]):
            raise HTTPException(status_code=400, detail="Datos incompletos")
        
        # Buscar la confirmación
        confirmation = None
        for conf in confirmations_db:
            if conf["folio"] == folio:
                confirmation = conf
                break
        
        if not confirmation:
            raise HTTPException(status_code=404, detail="Confirmación no encontrada")
        
        # Enviar email
        success = send_confirmation_email(
            email=email,
            name=name,
            folio=folio,
            will_attend=confirmation["will_attend"],
            guests=confirmation["guests"],
            phone=confirmation["phone"]
        )
        
        if success:
            return {"message": "Email enviado exitosamente"}
        else:
            raise HTTPException(status_code=500, detail="Error al enviar email")
            
    except Exception as e:
        logger.error(f"Error enviando email: {e}")
        raise HTTPException(status_code=500, detail=str(e))

def generate_folio():
    """Genera un folio único con formato AW-XXX"""
    return f"AW-{len(confirmations_db) + 234:03d}"

def send_confirmation_email(email: str, name: str, folio: str, image_data: str):
    """Envía email con la confirmación"""
    try:
        # Configuración del email (usar variables de entorno en producción)
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = "invitaciones@up.edu.mx"  # Cambiar por email real
        sender_password = "password"  # Cambiar por password real
        
        # Crear mensaje
        msg = MIMEMultipart('related')
        msg['From'] = sender_email
        msg['To'] = email
        msg['Subject'] = f"Confirmación de Asistencia - Folio {folio}"
        
        # HTML del email
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="background: linear-gradient(135deg, #d4950f, #b37b0d); padding: 20px; border-radius: 10px 10px 0 0; text-align: center;">
                <h1 style="color: white; margin: 0;">Universidad Panamericana</h1>
                <p style="color: #fdf9e9; margin: 5px 0;">Campus Guadalajara</p>
            </div>
            <div style="background: white; padding: 30px; border-radius: 0 0 10px 10px; border: 2px solid #d4950f;">
                <h2 style="color: #d4950f; text-align: center;">¡Confirmación Recibida!</h2>
                <p>Estimado/a <strong>{name}</strong>,</p>
                <p>Hemos recibido tu confirmación de asistencia para la <strong>Fiesta de Finalización del Posgrado</strong>.</p>
                
                <div style="background: #fdf9e9; padding: 15px; border-left: 4px solid #d4950f; margin: 20px 0;">
                    <p><strong>📋 Folio:</strong> {folio}</p>
                    <p><strong>📅 Fecha:</strong> Viernes 14 de noviembre de 2025</p>
                    <p><strong>⏰ Hora:</strong> 17:00 hrs</p>
                    <p><strong>📍 Lugar:</strong> Ciudad Granja</p>
                </div>
                
                <p>Adjunto encontrarás tu pase de acceso. Por favor, presenta este documento el día del evento.</p>
                <p>La ubicación exacta se enviará por WhatsApp al número registrado.</p>
                
                <div style="text-align: center; margin: 30px 0;">
                    <p style="color: #666; font-size: 12px;">Este es tu pase de acceso oficial</p>
                </div>
                
                <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
                <p style="text-align: center; color: #888; font-size: 12px;">
                    Posgrado en TIC's<br>
                    Celebración de Finalización
                </p>
            </div>
        </body>
        </html>
        """
        
        msg.attach(MIMEText(html_body, 'html'))
        
        # Adjuntar imagen si existe
        if image_data:
            image_binary = base64.b64decode(image_data.split(',')[1])
            img = MIMEImage(image_binary)
            img.add_header('Content-Disposition', f'attachment; filename="invitacion_{folio}.png"')
            msg.attach(img)
        
        # Nota: En desarrollo, solo simular envío
        print(f"Email simulado enviado a {email} con folio {folio}")
        return True
        
        # Para producción, descomentar:
        # server = smtplib.SMTP(smtp_server, smtp_port)
        # server.starttls()
        # server.login(sender_email, sender_password)
        # server.send_message(msg)
        # server.quit()
        
    except Exception as e:
        print(f"Error enviando email: {e}")
        return False

@app.post("/api/confirmations", response_model=ConfirmationResponse)
async def create_confirmation(confirmation: ConfirmationCreate):
    
    # Validar email duplicado (excepto correachris1@gmail.com para pruebas)
    if confirmation.email != "correachris1@gmail.com":
        existing_confirmation = next((conf for conf in confirmations_db if conf["email"] == confirmation.email), None)
        if existing_confirmation:
            raise HTTPException(
                status_code=400, 
                detail=f"El email {confirmation.email} ya está registrado. Si necesitas actualizar tu confirmación, contacta al organizador."
            )
    
    # Si NO va a asistir, solo guardar y retornar mensaje
    if not confirmation.will_attend:
        new_confirmation = {
            "id": len(confirmations_db) + 1,
            "folio": "",
            "name": confirmation.name,
            "email": confirmation.email,
            "will_attend": confirmation.will_attend,
            "guests": 0,
            "phone": confirmation.phone,
            "timestamp": datetime.now().isoformat(),
            "qr_url": None
        }
        
        confirmations_db.append(new_confirmation)
        
        # Enviar email de no asistencia (opcional)
        event_details = {
            "email": confirmation.email,
            "attending": False,
            "companions": 0,
            "whatsapp": confirmation.phone,
            "confirmed_at": datetime.now().strftime("%d/%m/%Y %H:%M")
        }
        
        try:
            from email_config import EMAIL_CONFIG
            
            if EMAIL_CONFIG["enabled"]:
                await email_service.send_confirmation_email(
                    to_email=confirmation.email,
                    guest_name=confirmation.name,
                    event_details=event_details
                )
                logger.info(f"✅ Email de no asistencia enviado a {confirmation.email}")
            else:
                logger.info(f"📧 Email simulado (no asistencia) enviado a {confirmation.email}")
                print(f"🚫 SIMULACIÓN: Email de no asistencia para {confirmation.name}")
                print(f"📧 A: {confirmation.email}")
                print("="*60)
        except Exception as e:
            logger.error(f"Error enviando email de no asistencia: {str(e)}")
            print(f"📧 SIMULACIÓN: Email de no asistencia que se enviaría a {confirmation.email}")
        
        return ConfirmationResponse(**new_confirmation)
    
    # Si SÍ va a asistir, generar folio y QR
    folio = generate_folio()
    qr_url = f"https://registro.iux.com.mx/confirmation/{folio}"
    
    # Crear confirmación
    new_confirmation = {
        "id": len(confirmations_db) + 1,
        "folio": folio,
        "name": confirmation.name,
        "email": confirmation.email,
        "will_attend": confirmation.will_attend,
        "guests": confirmation.guests,
        "phone": confirmation.phone,
        "timestamp": datetime.now().isoformat(),
        "qr_url": qr_url
    }
    
    confirmations_db.append(new_confirmation)
    
    # Preparar detalles del evento para el email
    event_details = {
        "email": confirmation.email,
        "attending": True,
        "companions": confirmation.guests,
        "whatsapp": confirmation.phone,
        "confirmed_at": datetime.now().strftime("%d/%m/%Y %H:%M")
    }
    
    # El email se enviará después desde el frontend con el pase generado
    logger.info(f"🎯 Confirmación guardada para {confirmation.name} - Email se enviará con pase generado")
    
    return ConfirmationResponse(**new_confirmation)

@app.post("/api/send-confirmation-email")
async def send_email_confirmation(data: dict):
    """Envía la confirmación por email"""
    try:
        folio = data.get("folio")
        email = data.get("email")
        name = data.get("name")
        image_data = data.get("imageData")
        
        if not all([folio, email, name]):
            raise HTTPException(status_code=400, detail="Datos incompletos")
        
        success = send_confirmation_email(email, name, folio, image_data)
        
        if success:
            return {"success": True, "message": "Email enviado correctamente"}
        else:
            raise HTTPException(status_code=500, detail="Error enviando email")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/confirmation/{folio}")
async def get_confirmation_by_folio(folio: str):
    """Obtiene confirmación por folio (para QR)"""
    confirmation = next((c for c in confirmations_db if c.get("folio") == folio), None)
    if not confirmation:
        raise HTTPException(status_code=404, detail="Confirmación no encontrada")
    
    return confirmation

@app.post("/api/confirmations/{invitation_id}")
async def confirm_invitation(invitation_id: int, attendance: bool = True):
    invitation = next((inv for inv in invitations_db if inv["id"] == invitation_id), None)
    if not invitation:
        raise HTTPException(status_code=404, detail="Invitación no encontrada")
    
    return {
        "message": "Confirmación recibida",
        "invitation_id": invitation_id,
        "will_attend": attendance
    }

@app.post("/api/send-pass-email")
async def send_pass_email(data: dict):
    """
    Envía el pase de acceso por email usando la imagen generada en el frontend
    """
    try:
        from email_config import EMAIL_CONFIG
        
        if not EMAIL_CONFIG["enabled"]:
            return {"success": False, "message": "Email no configurado"}
            
        # Preparar detalles del evento
        event_details = {
            "email": data.get("email"),
            "attending": True,
            "companions": 0,  # Se podría pasar en data si es necesario
            "whatsapp": "",   # Se podría pasar en data si es necesario
            "confirmed_at": datetime.now().strftime("%d/%m/%Y %H:%M")
        }
        
        # Enviar email con el pase
        result = await email_service.send_confirmation_email(
            to_email=data.get("email"),
            guest_name=data.get("name"),
            event_details=event_details,
            pass_image_base64=data.get("pass_image_base64")
        )
        
        if result["success"]:
            logger.info(f"✅ Pase enviado por email a {data.get('email')}")
            return {"success": True, "message": "Pase enviado exitosamente"}
        else:
            logger.error(f"❌ Error enviando pase: {result['message']}")
            return {"success": False, "message": result["message"]}
            
    except Exception as e:
        logger.error(f"❌ Error en send_pass_email: {str(e)}")
        return {"success": False, "message": str(e)}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "simple_main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
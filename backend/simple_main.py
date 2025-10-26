from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel, EmailStr
from typing import List, Optional
import os

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
        "name": "María González López",
        "phone": "+52 33 1234 5678",
        "will_attend": True,
        "guests": 2,
        "timestamp": "2025-10-20T10:30:00.000Z"
    },
    {
        "id": 2,
        "name": "Juan Carlos Pérez",
        "phone": "+52 33 8765 4321",
        "will_attend": True,
        "guests": 1,
        "timestamp": "2025-10-21T14:15:00.000Z"
    },
    {
        "id": 3,
        "name": "Ana María Rodríguez",
        "phone": "+52 33 9876 5432",
        "will_attend": False,
        "guests": 0,
        "timestamp": "2025-10-22T09:45:00.000Z"
    },
    {
        "id": 4,
        "name": "Luis Fernando Sánchez",
        "phone": "+52 33 2468 1357",
        "will_attend": True,
        "guests": 3,
        "timestamp": "2025-10-23T16:20:00.000Z"
    }
]
events_db = [
    {
        "id": 1,
        "title": "Fiesta de Finalización del Posgrado",
        "description": "Posgrado en Derecho de las Tecnologías de la Información",
        "date": "2025-11-14",
        "time": "17:00",
        "location": "Ciudad Granja, Universidad Panamericana - Campus Guadalajara"
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
    will_attend: bool
    guests: int = 0
    phone: str

class ConfirmationResponse(BaseModel):
    id: int
    name: str
    will_attend: bool
    guests: int
    phone: str
    timestamp: str

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

@app.post("/api/confirmations", response_model=ConfirmationResponse)
async def create_confirmation(confirmation: ConfirmationCreate):
    from datetime import datetime
    
    # Crear confirmación
    new_confirmation = {
        "id": len(confirmations_db) + 1,
        "name": confirmation.name,
        "will_attend": confirmation.will_attend,
        "guests": confirmation.guests,
        "phone": confirmation.phone,
        "timestamp": datetime.now().isoformat()
    }
    
    confirmations_db.append(new_confirmation)
    
    return ConfirmationResponse(**new_confirmation)

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
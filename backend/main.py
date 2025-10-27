from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, EmailStr
from typing import Optional
import json
import os
from datetime import datetime
import uuid

app = FastAPI(title="Sistema de Invitaciones")

# Modelo para confirmación
class ConfirmationRequest(BaseModel):
    name: str
    email: EmailStr
    will_attend: bool
    guests: int = 0
    phone: str
    privacy_accept: bool = True

# Rutas relativas desde backend/
STATIC_DIR = os.path.join(os.path.dirname(__file__), "..", "static")
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(DATA_DIR, exist_ok=True)

# Ruta para servir archivos estáticos
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/")
def read_root():
    """Servir la página de confirmación"""
    return FileResponse(os.path.join(STATIC_DIR, "confirmation.html"))

@app.get("/test")
def test():
    return {"status": "ok", "message": "API funcionando correctamente"}

@app.post("/api/confirmations")
async def create_confirmation(confirmation: ConfirmationRequest):
    """Crear una nueva confirmación de asistencia"""
    try:
        # Generar folio único
        folio = f"UP-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8].upper()}"
        
        # Crear objeto de confirmación
        confirmation_data = {
            "folio": folio,
            "name": confirmation.name,
            "email": confirmation.email,
            "will_attend": confirmation.will_attend,
            "guests": confirmation.guests,
            "phone": confirmation.phone,
            "privacy_accept": confirmation.privacy_accept,
            "timestamp": datetime.now().isoformat(),
            "qr_url": f"http://localhost:8000/confirmation/{folio}"
        }
        
        # Guardar en archivo JSON
        confirmations_file = os.path.join(DATA_DIR, "confirmations.json")
        
        # Leer confirmaciones existentes
        confirmations = []
        if os.path.exists(confirmations_file):
            with open(confirmations_file, 'r', encoding='utf-8') as f:
                try:
                    confirmations = json.load(f)
                except json.JSONDecodeError:
                    confirmations = []
        
        # Agregar nueva confirmación
        confirmations.append(confirmation_data)
        
        # Guardar todas las confirmaciones
        with open(confirmations_file, 'w', encoding='utf-8') as f:
            json.dump(confirmations, f, ensure_ascii=False, indent=2)
        
        return JSONResponse(
            status_code=201,
            content=confirmation_data
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al guardar confirmación: {str(e)}")

@app.post("/api/send-pass-email")
async def send_pass_email(request: Request):
    """Endpoint para recibir la imagen del pase y enviar por email"""
    try:
        from email_service import email_service
        
        data = await request.json()
        email = data.get('email')
        name = data.get('name')
        folio = data.get('folio')
        pass_image_base64 = data.get('pass_image_base64')
        
        print(f"📧 Pase recibido para envío: {name} ({email}) - Folio: {folio}")
        
        # Preparar detalles del evento para el email
        event_details = {
            'email': email,
            'attending': True,
            'companions': data.get('guests', 0),
            'whatsapp': data.get('phone', ''),
            'confirmed_at': datetime.now().strftime('%d/%m/%Y %H:%M')
        }
        
        # Enviar email con el pase adjunto
        result = await email_service.send_confirmation_email(
            to_email=email,
            guest_name=name,
            event_details=event_details,
            pass_image_base64=pass_image_base64
        )
        
        if result['success']:
            print(f"✅ Email enviado exitosamente a {email}")
        else:
            print(f"❌ Error enviando email: {result['message']}")
        
        return result
        
    except Exception as e:
        print(f"❌ Error en send-pass-email: {str(e)}")
        return {"success": False, "message": str(e)}

@app.get("/api/confirmations")
async def get_confirmations():
    """Obtener todas las confirmaciones"""
    try:
        confirmations_file = os.path.join(DATA_DIR, "confirmations.json")
        
        if not os.path.exists(confirmations_file):
            return []
        
        with open(confirmations_file, 'r', encoding='utf-8') as f:
            confirmations = json.load(f)
        
        return confirmations
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener confirmaciones: {str(e)}")

@app.get("/confirmation/{folio}")
async def get_confirmation_by_folio(folio: str):
    """Obtener una confirmación específica por folio"""
    try:
        confirmations_file = os.path.join(DATA_DIR, "confirmations.json")
        
        if not os.path.exists(confirmations_file):
            raise HTTPException(status_code=404, detail="Confirmación no encontrada")
        
        with open(confirmations_file, 'r', encoding='utf-8') as f:
            confirmations = json.load(f)
        
        # Buscar confirmación por folio
        for conf in confirmations:
            if conf['folio'] == folio:
                return conf
        
        raise HTTPException(status_code=404, detail="Confirmación no encontrada")
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al buscar confirmación: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

#!/bin/bash

echo "🔧 Creando backend mejorado con mejor manejo de errores..."

# Crear directorio backend mejorado
mkdir -p /home/ubuntu/invitation-system/backend

# Crear main.py mejorado
cat > /home/ubuntu/invitation-system/backend/main.py << 'EOF'
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, validator
import json
import os
from datetime import datetime
from typing import List, Optional
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Sistema de Invitaciones UP", version="1.0.0")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo de datos para RSVP
class RSVPModel(BaseModel):
    nombre: str
    email: str
    telefono: str
    confirmacion: str
    acompanantes: int
    comentarios: Optional[str] = ""
    
    @validator('nombre')
    def validate_nombre(cls, v):
        if not v or len(v.strip()) < 2:
            raise ValueError('El nombre debe tener al menos 2 caracteres')
        return v.strip()
    
    @validator('email')
    def validate_email(cls, v):
        if '@' not in v or '.' not in v:
            raise ValueError('Email inválido')
        return v.strip().lower()
    
    @validator('confirmacion')
    def validate_confirmacion(cls, v):
        if v not in ['si', 'no']:
            raise ValueError('Confirmación debe ser "si" o "no"')
        return v
    
    @validator('acompanantes')
    def validate_acompanantes(cls, v):
        if v < 0 or v > 5:
            raise ValueError('Número de acompañantes debe estar entre 0 y 5')
        return v

# Archivo de datos
DATA_FILE = '/data/rsvps.json'

def ensure_data_file():
    """Asegurar que el archivo de datos existe y es válido"""
    try:
        data_dir = os.path.dirname(DATA_FILE)
        if not os.path.exists(data_dir):
            os.makedirs(data_dir, mode=0o755)
            logger.info(f"Creado directorio de datos: {data_dir}")
        
        if not os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump([], f)
            os.chmod(DATA_FILE, 0o644)
            logger.info(f"Creado archivo de datos: {DATA_FILE}")
        
        # Verificar que el archivo es JSON válido
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if not isinstance(data, list):
                raise ValueError("El archivo de datos no contiene una lista")
    except Exception as e:
        logger.error(f"Error al verificar archivo de datos: {e}")
        # Crear archivo backup y nuevo archivo
        if os.path.exists(DATA_FILE):
            backup_file = f"{DATA_FILE}.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            os.rename(DATA_FILE, backup_file)
            logger.info(f"Archivo corrupto respaldado como: {backup_file}")
        
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f)
        os.chmod(DATA_FILE, 0o644)
        logger.info("Creado nuevo archivo de datos")

def load_rsvps() -> List[dict]:
    """Cargar RSVPs del archivo"""
    try:
        ensure_data_file()
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except Exception as e:
        logger.error(f"Error al cargar RSVPs: {e}")
        return []

def save_rsvp(rsvp_data: dict) -> bool:
    """Guardar RSVP en el archivo"""
    try:
        rsvps = load_rsvps()
        
        # Agregar timestamp y ID único
        rsvp_data['timestamp'] = datetime.now().isoformat()
        rsvp_data['id'] = len(rsvps) + 1
        
        rsvps.append(rsvp_data)
        
        # Guardar con backup
        backup_file = f"{DATA_FILE}.tmp"
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(rsvps, f, ensure_ascii=False, indent=2)
        
        os.replace(backup_file, DATA_FILE)
        os.chmod(DATA_FILE, 0o644)
        
        logger.info(f"RSVP guardado exitosamente: {rsvp_data['nombre']} ({rsvp_data['email']})")
        return True
    except Exception as e:
        logger.error(f"Error al guardar RSVP: {e}")
        return False

@app.get("/health")
async def health_check():
    """Verificar estado del servidor"""
    try:
        ensure_data_file()
        rsvps = load_rsvps()
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "rsvps_count": len(rsvps),
            "data_file_exists": os.path.exists(DATA_FILE)
        }
    except Exception as e:
        logger.error(f"Error en health check: {e}")
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)}
        )

@app.post("/api/rsvp")
async def create_rsvp(rsvp: RSVPModel):
    """Crear nuevo RSVP"""
    try:
        logger.info(f"Recibiendo RSVP de: {rsvp.nombre} ({rsvp.email})")
        
        # Verificar si ya existe un RSVP con este email
        existing_rsvps = load_rsvps()
        for existing in existing_rsvps:
            if existing.get('email', '').lower() == rsvp.email.lower():
                logger.warning(f"RSVP duplicado para email: {rsvp.email}")
                raise HTTPException(
                    status_code=400,
                    detail="Ya existe un RSVP registrado con este email"
                )
        
        rsvp_data = rsvp.dict()
        
        if save_rsvp(rsvp_data):
            return {
                "message": "RSVP registrado exitosamente",
                "data": rsvp_data,
                "status": "success"
            }
        else:
            raise HTTPException(
                status_code=500,
                detail="Error al guardar el RSVP. Por favor intenta nuevamente."
            )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error inesperado en create_rsvp: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error interno del servidor: {str(e)}"
        )

@app.get("/api/rsvps")
async def get_rsvps():
    """Obtener todos los RSVPs"""
    try:
        rsvps = load_rsvps()
        return {
            "rsvps": rsvps,
            "total": len(rsvps),
            "confirmados": len([r for r in rsvps if r.get('confirmacion') == 'si']),
            "no_confirmados": len([r for r in rsvps if r.get('confirmacion') == 'no'])
        }
    except Exception as e:
        logger.error(f"Error al obtener RSVPs: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener RSVPs: {str(e)}"
        )

@app.get("/admin/confirmados", response_class=HTMLResponse)
async def admin_confirmados():
    """Panel de administración con lista de confirmados"""
    try:
        rsvps = load_rsvps()
        confirmados = [r for r in rsvps if r.get('confirmacion') == 'si']
        
        html_content = f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Admin - RSVPs Confirmados</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
                .header {{ background: #4a154b; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
                .stats {{ display: flex; gap: 20px; margin-bottom: 20px; }}
                .stat-card {{ background: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
                .rsvp-card {{ background: white; padding: 15px; margin-bottom: 15px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
                .confirmado {{ border-left: 5px solid #28a745; }}
                .no-confirmado {{ border-left: 5px solid #dc3545; }}
                .refresh-btn {{ background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🎓 Panel de Administración - Graduación UP</h1>
                <p>Gestión de RSVPs para la ceremonia de graduación</p>
            </div>
            
            <div class="stats">
                <div class="stat-card">
                    <h3>📊 Estadísticas</h3>
                    <p><strong>Total RSVPs:</strong> {len(rsvps)}</p>
                    <p><strong>Confirmados:</strong> {len(confirmados)}</p>
                    <p><strong>No confirmados:</strong> {len(rsvps) - len(confirmados)}</p>
                    <p><strong>Acompañantes totales:</strong> {sum(r.get('acompanantes', 0) for r in confirmados)}</p>
                </div>
            </div>
            
            <button class="refresh-btn" onclick="location.reload()">🔄 Actualizar</button>
            
            <h2>✅ RSVPs Confirmados ({len(confirmados)})</h2>
        """
        
        for i, rsvp in enumerate(confirmados, 1):
            acompanantes = rsvp.get('acompanantes', 0)
            comentarios = rsvp.get('comentarios', '') or 'Sin comentarios'
            timestamp = rsvp.get('timestamp', 'No disponible')
            
            html_content += f"""
            <div class="rsvp-card confirmado">
                <h3>#{i} - {rsvp.get('nombre', 'Sin nombre')}</h3>
                <p><strong>📧 Email:</strong> {rsvp.get('email', 'Sin email')}</p>
                <p><strong>📞 Teléfono:</strong> {rsvp.get('telefono', 'Sin teléfono')}</p>
                <p><strong>👥 Acompañantes:</strong> {acompanantes}</p>
                <p><strong>💬 Comentarios:</strong> {comentarios}</p>
                <p><strong>🕒 Fecha de registro:</strong> {timestamp}</p>
            </div>
            """
        
        html_content += """
            </body>
        </html>
        """
        
        return html_content
    except Exception as e:
        logger.error(f"Error en admin panel: {e}")
        return f"""
        <html><body>
        <h1>Error en el panel de administración</h1>
        <p>Error: {str(e)}</p>
        </body></html>
        """

# Inicializar archivo de datos al arrancar
@app.on_event("startup")
async def startup_event():
    logger.info("🚀 Iniciando servidor de invitaciones...")
    ensure_data_file()
    logger.info("✅ Servidor iniciado correctamente")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
EOF

# Crear requirements.txt actualizado
cat > /home/ubuntu/invitation-system/backend/requirements.txt << 'EOF'
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
python-multipart==0.0.6
EOF

echo "✅ Backend mejorado creado exitosamente"
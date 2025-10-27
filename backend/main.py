from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Sistema de Invitaciones",
    version="1.0.0",
    description="Sistema completo de gestión de invitaciones"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "🎉 ¡Sistema de Invitaciones funcionando correctamente!",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "docs": "/docs",
            "health": "/health",
            "api": "/api"
        }
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "backend", "timestamp": "2025-10-25"}

@app.get("/api/")
async def api_root():
    return {
        "message": "API del Sistema de Invitaciones",
        "version": "1.0.0",
        "available_endpoints": ["/", "/health", "/docs"]
    }

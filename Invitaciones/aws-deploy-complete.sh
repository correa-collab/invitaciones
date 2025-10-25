#!/bin/bash

echo "🚀 Script de Deployment Completo para AWS"
echo "========================================="

# 1. Verificar directorio actual
echo "📁 Verificando directorio actual..."
pwd
ls -la

# 2. Crear estructura de directorios
echo "📁 Creando estructura de directorios..."
mkdir -p backend frontend

# 3. Crear backend/requirements.txt
echo "📝 Creando backend/requirements.txt..."
cat > backend/requirements.txt << 'EOF'
fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.5.0
EOF

# 4. Crear backend/main.py
echo "📝 Creando backend/main.py..."
cat > backend/main.py << 'EOF'
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
EOF

# 5. Crear backend/Dockerfile
echo "📝 Creando backend/Dockerfile..."
cat > backend/Dockerfile << 'EOF'
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
EOF

# 6. Crear frontend/Dockerfile
echo "📝 Creando frontend/Dockerfile..."
cat > frontend/Dockerfile << 'EOF'
FROM nginx:alpine

# Create a beautiful landing page
RUN echo '<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sistema de Invitaciones</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
        }
        .container {
            text-align: center;
            padding: 2rem;
            background: rgba(255,255,255,0.1);
            border-radius: 20px;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            max-width: 600px;
            margin: 2rem;
        }
        h1 { font-size: 3rem; margin-bottom: 1rem; }
        .emoji { font-size: 4rem; margin-bottom: 1rem; }
        p { font-size: 1.2rem; margin-bottom: 2rem; opacity: 0.9; }
        .btn {
            display: inline-block;
            padding: 1rem 2rem;
            margin: 0.5rem;
            background: rgba(255,255,255,0.2);
            color: white;
            text-decoration: none;
            border-radius: 50px;
            border: 2px solid rgba(255,255,255,0.3);
            transition: all 0.3s ease;
            font-weight: 600;
        }
        .btn:hover {
            background: rgba(255,255,255,0.3);
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }
        .status {
            background: rgba(0,255,0,0.2);
            padding: 0.5rem 1rem;
            border-radius: 25px;
            margin: 1rem 0;
            font-weight: 600;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="emoji">🎉</div>
        <h1>Sistema de Invitaciones</h1>
        <div class="status">✅ Funcionando Correctamente</div>
        <p>Tu aplicación está desplegada y funcionando en AWS EC2</p>
        <a href="/docs" class="btn">📚 Ver API Docs</a>
        <a href="/health" class="btn">❤️ Health Check</a>
        <p style="margin-top: 2rem; font-size: 1rem; opacity: 0.7;">
            Servidor: AWS EC2 • IP: 3.140.201.39 • Puerto: 80
        </p>
    </div>
</body>
</html>' > /usr/share/nginx/html/index.html

# Configure nginx to proxy API calls
RUN echo 'server {
    listen 80;
    server_name localhost;
    
    location / {
        root /usr/share/nginx/html;
        index index.html;
        try_files $uri $uri/ /index.html;
    }
    
    location /docs {
        proxy_pass http://backend:8000/docs;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /health {
        proxy_pass http://backend:8000/health;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /api {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}' > /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
EOF

# 7. Crear docker-compose.yml
echo "📝 Creando docker-compose.yml..."
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  # Base de datos PostgreSQL
  database:
    image: postgres:15
    environment:
      POSTGRES_DB: invitaciones_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password123
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    networks:
      - app-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Backend API (FastAPI)
  backend:
    build: ./backend
    environment:
      DATABASE_URL: postgresql://postgres:password123@database:5432/invitaciones_db
      SECRET_KEY: invitaciones_secret_key_2025
    depends_on:
      database:
        condition: service_healthy
    ports:
      - "8000:8000"
    networks:
      - app-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Frontend (Nginx)
  frontend:
    build: ./frontend
    depends_on:
      backend:
        condition: service_healthy
    ports:
      - "80:80"
    networks:
      - app-network

volumes:
  postgres_data:

networks:
  app-network:
    driver: bridge
EOF

# 8. Mostrar estructura creada
echo "📋 Verificando estructura creada..."
echo "=== Estructura de directorios ==="
find . -type f -name "*.py" -o -name "*.txt" -o -name "Dockerfile" -o -name "*.yml" | sort

echo ""
echo "=== Contenido de archivos principales ==="
echo "--- requirements.txt ---"
cat backend/requirements.txt

echo ""
echo "--- docker-compose.yml (primeras 20 líneas) ---"
head -20 docker-compose.yml

# 9. Parar servicios anteriores
echo "🛑 Parando servicios anteriores..."
sudo docker-compose down 2>/dev/null || true

# 10. Construir y ejecutar
echo "🚀 Construyendo y ejecutando servicios..."
sudo docker-compose up -d --build

# 11. Esperar un momento para que se inicien
echo "⏱️ Esperando que los servicios se inicien..."
sleep 10

# 12. Verificar estado
echo "📊 Verificando estado de los servicios..."
sudo docker-compose ps

# 13. Mostrar logs recientes
echo "📝 Logs recientes:"
sudo docker-compose logs --tail=10

# 14. Verificar conectividad
echo "🌐 Verificando conectividad..."
curl -s http://localhost/health || echo "❌ Health check falló"
curl -s http://localhost/ | head -1 || echo "❌ Frontend no responde"

echo ""
echo "🎉 ¡DEPLOYMENT COMPLETADO!"
echo "================================"
echo "🌐 Frontend: http://3.140.201.39"
echo "📚 API Docs: http://3.140.201.39/docs"
echo "❤️ Health: http://3.140.201.39/health"
echo ""
echo "📋 Comandos útiles:"
echo "sudo docker-compose ps          # Ver estado"
echo "sudo docker-compose logs -f     # Ver logs en vivo"
echo "sudo docker-compose restart     # Reiniciar"
echo "sudo docker-compose down        # Parar todo"
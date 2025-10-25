# 🚀 Guía Rápida de Inicio

## Opción 1: Usar Docker Compose (Recomendado)

### Requisitos previos
- Docker instalado
- Docker Compose instalado

### Iniciar el proyecto

```bash
# Iniciar todos los servicios
docker-compose up --build -d

# Ver logs
docker-compose logs -f

# Detener servicios
docker-compose down
```

### URLs
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

---

## Opción 2: Desarrollo Local (Sin Docker)

### Requisitos previos
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+

### 1. Configurar Base de Datos

```bash
# Crear base de datos PostgreSQL
createdb invitaciones_db

# O usar el script SQL incluido
psql -U postgres -f database/init.sql
```

### 2. Backend (FastAPI)

```bash
cd backend

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno (opcional)
cp .env.example .env  # Si existe, o crear uno nuevo

# Iniciar servidor
uvicorn main:app --reload --port 8000
```

### 3. Frontend (React)

En otra terminal:

```bash
cd frontend

# Instalar dependencias
npm install

# Iniciar servidor de desarrollo
npm run dev
```

### URLs de desarrollo
- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

---

## Opción 3: Script de Inicio Automático

```bash
# Hacer ejecutable (solo la primera vez)
chmod +x start.sh

# Ejecutar script interactivo
./start.sh
```

El script te guiará para elegir entre Docker o instalación local.

---

## Variables de Entorno

Crea un archivo `.env` en el directorio `backend/` con:

```env
# Database
DATABASE_URL=postgresql://postgres:password123@localhost:5432/invitaciones_db

# JWT
SECRET_KEY=tu_clave_secreta_super_segura

# Email (opcional para desarrollo)
EMAIL_PROVIDER=smtp
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_USER=tu_email@gmail.com
EMAIL_PASSWORD=tu_password
```

---

## Verificar Instalación

### Backend
```bash
curl http://localhost:8000/health
# Debe retornar: {"status": "healthy", "version": "1.0.0"}
```

### Frontend
Abre http://localhost:3000 en tu navegador

---

## Problemas Comunes

### Puerto 8000 ya en uso
```bash
# Linux/Mac
lsof -ti:8000 | xargs kill -9

# Windows
netstat -ano | findstr :8000
taskkill /PID <pid> /F
```

### Base de datos no conecta
- Verifica que PostgreSQL esté ejecutándose
- Verifica las credenciales en `DATABASE_URL`
- Asegúrate que la base de datos `invitaciones_db` existe

### npm install falla
```bash
# Limpiar caché y reinstalar
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
```

---

## Comandos Útiles

```bash
# Ver logs de Docker
docker-compose logs -f

# Reiniciar un servicio específico
docker-compose restart backend

# Reconstruir contenedores
docker-compose up --build

# Limpiar todo
docker-compose down -v
docker system prune -f
```

---

## Próximos Pasos

1. ✅ Proyecto iniciado
2. 📝 Revisar documentación en `README.md`
3. 👥 Crear usuario administrador
4. 🎉 Crear tu primer evento
5. 📧 Configurar servicio de email (AWS SES o SendGrid)

---

**¿Necesitas ayuda?** Revisa la documentación completa en `README.md` o `DEPLOYMENT-GUIDE.md`

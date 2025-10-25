# 🎯 Guía de Referencia Rápida

## ⚡ Inicio Rápido

```bash
# Opción más fácil (script interactivo)
./start.sh

# O con Docker (recomendado)
docker-compose up --build -d

# O desarrollo local automático
./run-local.sh
```

---

## 📋 Comandos Útiles

### Docker Compose
```bash
# Iniciar
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener
docker-compose down

# Reiniciar un servicio
docker-compose restart backend

# Ver estado
docker-compose ps
```

### Desarrollo Local

#### Backend
```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
uvicorn main:app --reload --port 8000
```

#### Frontend
```bash
cd frontend
npm run dev
```

### Base de Datos
```bash
# PostgreSQL
createdb invitaciones_db

# Ver estado
psql -l
```

---

## 🌐 URLs

| Servicio | URL | Descripción |
|----------|-----|-------------|
| Frontend | http://localhost:3000 | Interfaz de usuario |
| Backend API | http://localhost:8000 | API REST |
| API Docs | http://localhost:8000/docs | Swagger UI |
| Health Check | http://localhost:8000/health | Estado del servidor |

---

## 🛠 Solución de Problemas

### Puerto ocupado
```bash
# Ver qué usa el puerto 8000
lsof -i :8000
# O
netstat -ano | findstr :8000

# Matar proceso
kill -9 <PID>
```

### Reinstalar dependencias

#### Backend
```bash
cd backend
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Frontend
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Limpiar Docker
```bash
docker-compose down -v
docker system prune -f
```

---

## 📦 Estructura del Proyecto

```
invitaciones/
├── backend/              # FastAPI
│   ├── main.py          # App principal
│   ├── config.py        # Configuración
│   ├── routers/         # Endpoints
│   └── database/        # Modelos y conexión
├── frontend/            # React
│   ├── src/            # Código fuente
│   └── public/         # Archivos estáticos
├── database/           # Scripts SQL
├── start.sh           # Script interactivo
├── run-local.sh       # Inicio rápido
└── docker-compose.yml # Configuración Docker
```

---

## 🔐 Variables de Entorno

Archivo: `backend/.env`

```env
# Esenciales
DATABASE_URL=postgresql://postgres:password@localhost/invitaciones_db
SECRET_KEY=tu_clave_secreta

# Email (opcional)
EMAIL_PROVIDER=smtp
SMTP_SERVER=smtp.gmail.com
EMAIL_USER=tu@email.com
EMAIL_PASSWORD=tu_password
```

---

## 📚 Documentación Completa

- **START-GUIDE.md** - Guía detallada de inicio
- **CAMBIOS.md** - Resumen de cambios recientes
- **README.md** - Documentación principal
- **DEPLOYMENT-GUIDE.md** - Deploy en AWS

---

## 🆘 ¿Necesitas Ayuda?

1. Revisa **START-GUIDE.md** para instrucciones paso a paso
2. Verifica que todos los requisitos estén instalados
3. Revisa los logs: `docker-compose logs` o archivos .log
4. Asegúrate de tener las variables de entorno configuradas

---

**Última actualización**: Octubre 2025

# 🎉 Sistema de Gestión de Invitaciones para Eventos

[![Deploy Status](https://img.shields.io/badge/deploy-ready-brightgreen)](http://3.140.201.39)
[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://python.org)
[![React](https://img.shields.io/badge/React-18-blue)](https://reactjs.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-latest-green)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/Docker-compose-blue)](https://docker.com)

Una aplicación web completa para gestionar invitaciones de eventos con confirmación automática y generación de PDFs.

## 🌟 Características Principales

### 🎯 **Para Organizadores**
- **Dashboard Completo**: Vista general de eventos, invitados y confirmaciones
- **Gestión de Eventos**: Crear, editar y administrar eventos fácilmente
- **Lista de Invitados**: Importar/exportar listas, gestión completa de datos
- **Envío Automático**: Emails personalizados con plantillas profesionales
- **Reportes y Analytics**: Estadísticas en tiempo real de confirmaciones

### 👥 **Para Invitados**
- **Confirmación RSVP**: Página pública simple y elegante
- **Sin Registro**: Confirmación directa mediante token único
- **Responsive**: Funciona perfecto en móvil y desktop
- **Confirmación PDF**: Descarga automática del comprobante

### 🔧 **Técnicas**
- **Autenticación JWT**: Sistema seguro de login
- **API REST**: Backend robusto con FastAPI
- **Base de Datos**: PostgreSQL con migraciones automáticas
- **Containerización**: Docker para deployment fácil

## 🛠 Stack Tecnológico

- **Frontend**: React 18 + TypeScript + Tailwind CSS
- **Backend**: FastAPI + Python 3.11
- **Base de Datos**: PostgreSQL 15
- **Email**: AWS SES / SendGrid
- **PDF Generation**: ReportLab
- **Deployment**: Docker + AWS EC2
- **Proxy**: Nginx

## 📁 Estructura del Proyecto

```
/
├── frontend/           # Aplicación React
├── backend/            # API FastAPI
├── database/           # Scripts SQL y migraciones
├── docker/            # Contenedores Docker
├── docs/              # Documentación
└── deployment/        # Scripts de deployment
```

## 🚀 Inicio Rápido

### Opción 1: Script Automático (Más Fácil)
```bash
# Ejecutar script interactivo
./start.sh
```

### Opción 2: Docker Compose (Recomendado)
```bash
# Iniciar todos los servicios
docker-compose up --build -d

# Ver estado
docker-compose ps

# URLs disponibles:
# - Frontend: http://localhost:3000
# - Backend: http://localhost:8000
# - API Docs: http://localhost:8000/docs
```

### Opción 3: Desarrollo Local Rápido
```bash
# Script que inicia backend y frontend automáticamente
./run-local.sh
```

📖 **Más detalles**: Ver [START-GUIDE.md](START-GUIDE.md) para instrucciones completas

---

## 🌐 Deploy Rápido (AWS)

### 1️⃣ **Clonar Repositorio**
```bash
git clone https://github.com/tu-usuario/invitaciones.git
cd invitaciones
```

### 2️⃣ **Deploy con Docker**
```bash
# Todo en un comando
sudo docker-compose up -d --build

# Verificar estado
sudo docker-compose ps
```

### 3️⃣ **¡Listo!**
- 🌐 **App**: http://3.140.201.39
- 📚 **API Docs**: http://3.140.201.39/api/docs
- 👨‍💼 **Admin**: http://3.140.201.39/dashboard

## 🛠 Desarrollo Local

### Backend (FastAPI)
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Frontend (React)
```bash
cd frontend
npm install
npm run dev  # Puerto 3000
```

### Base de Datos
```bash
# PostgreSQL local
createdb invitaciones_db
# Las tablas se crean automáticamente
```

## 🌐 URLs

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Admin Panel**: http://localhost:3000/admin

## 📧 Configuración Email

Configure las variables de entorno en `.env`:

```env
EMAIL_PROVIDER=aws_ses
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_REGION=us-east-1
```

## 🗃 Base de Datos

```bash
# Crear base de datos
createdb invitaciones_db

# Ejecutar migraciones
cd backend
alembic upgrade head
```

## 📋 Features Roadmap

- [x] Estructura base del proyecto
- [ ] Autenticación de usuarios
- [ ] CRUD de eventos
- [ ] Gestión de invitados
- [ ] Envío de emails
- [ ] Página de confirmación RSVP
- [ ] Generación de PDFs
- [ ] Dashboard y reportes
- [ ] Deployment a AWS

## 🤝 Contribuir

1. Fork del proyecto
2. Crear branch (`git checkout -b feature/nueva-feature`)
3. Commit cambios (`git commit -am 'Add nueva feature'`)
4. Push al branch (`git push origin feature/nueva-feature`)
5. Abrir Pull Request

## 📄 Licencia

MIT License - ver archivo [LICENSE](LICENSE)

---

**Estado**: En desarrollo activo 🚧
**Última actualización**: Octubre 2025
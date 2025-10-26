<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Sistema de Gestión de Invitaciones para Eventos

Este es un proyecto completo para gestionar invitaciones de eventos con:
- Frontend: React + TypeScript
- Backend: FastAPI + Python
- Base de datos: PostgreSQL
- Deployment: Docker + AWS

## Características principales:
- Creación y gestión de eventos
- Administración de listas de invitados
- Envío automático de invitaciones por email
- Seguimiento de confirmaciones (RSVP)
- Generación de PDFs de confirmación
- Panel de administración
- Autenticación de usuarios
- Página pública de confirmación

## Estructura del proyecto:
- `/frontend/` - Aplicación React con TypeScript
- `/backend/` - API FastAPI con Python
- `/database/` - Scripts y migraciones de PostgreSQL
- `/docker/` - Configuración de contenedores
- `/docs/` - Documentación del proyecto

## Estado del proyecto: ✅ COMPLETADO - Estructura base lista

### ✅ Completado:
- [x] Estructura completa de carpetas y archivos
- [x] Backend FastAPI con autenticación y modelos de base de datos
- [x] Frontend React con TypeScript y Tailwind CSS
- [x] Configuración Docker para deployment
- [x] Scripts de deployment para AWS EC2
- [x] Extensiones de VS Code instaladas

### 🚀 Próximos pasos:
1. **Instalar Node.js** en el sistema para compilar el frontend
2. **Configurar Python environment** para el backend
3. **Conectar al servidor AWS** (IP: 3.140.201.39) 
4. **Deploy con Docker** usando `docker-compose up -d`
5. **Configurar base de datos** PostgreSQL
6. **Implementar funcionalidades** de envío de emails y PDF

### 🌐 URLs una vez deployado:
- Frontend: http://3.140.201.39
- Backend API: http://3.140.201.39/api/docs
- Dashboard: http://3.140.201.39/dashboard
# 🎓 Sistema de Invitaciones - Universidad Panamericana

Sistema completo de gestión de invitaciones para eventos académicos con colorimetría institucional dorada.

## ✨ Características Principales

- 🎨 **Diseño Universidad Panamericana** - Colorimetría dorada institucional sin logo
- 📝 **Confirmación de Asistencia** - Formulario intuitivo con validación
- 📊 **Panel de Administración** - Estadísticas en tiempo real y lista de asistentes
- 💾 **Exportación CSV** - Descarga completa de datos de confirmación
- 🖼️ **Imagen de Confirmación** - Generación automática con Canvas API
- 📱 **Responsive Design** - Funciona perfectamente en dispositivos móviles
- 🔄 **Tiempo Real** - Actualizaciones automáticas de confirmaciones

## 🛠️ Tecnologías

- **Backend:** FastAPI + Python 3.13
- **Frontend:** HTML + CSS + JavaScript + Tailwind CSS
- **Base de Datos:** En memoria (para desarrollo)
- **Deployment:** Docker + AWS EC2

## 📁 Estructura del Proyecto

```
/Invitaciones/
├── backend/
│   ├── simple_main.py      # Servidor FastAPI principal
│   └── requirements.txt    # Dependencias Python
├── static/
│   ├── index.html         # Página principal del evento
│   ├── confirmation.html  # Formulario de confirmación
│   └── admin.html         # Panel de administración
├── docker-compose-simple.yml  # Configuración Docker
├── Dockerfile.simple          # Imagen Docker
└── deploy-simple.sh           # Script de deployment
```

## 🚀 Instalación y Uso

### Desarrollo Local

```bash
# 1. Clonar el repositorio
git clone https://github.com/TU_USUARIO/invitaciones-up.git
cd invitaciones-up

# 2. Configurar entorno Python
python -m venv .venv
source .venv/bin/activate  # En Mac/Linux
pip install -r backend/requirements.txt

# 3. Ejecutar servidor
python backend/simple_main.py

# 4. Abrir en navegador
# http://127.0.0.1:8000 - Página principal
# http://127.0.0.1:8000/admin.html - Panel admin
```

### Deployment en AWS

```bash
# 1. Comprimir proyecto
./deploy-simple.sh

# 2. En servidor AWS EC2 (vía Instance Connect):
# Subir archivo invitaciones-deploy.tar.gz

# 3. Extraer y ejecutar
tar -xzf invitaciones-deploy.tar.gz
sudo apt update
sudo apt install -y docker.io docker-compose
sudo docker-compose -f docker-compose-simple.yml up -d --build

# 4. Verificar
sudo docker-compose -f docker-compose-simple.yml ps
```

## 🌐 URLs una vez Deployado

- **Página Principal:** `http://3.140.201.39`
- **Formulario:** `http://3.140.201.39/confirmation.html`
- **Panel Admin:** `http://3.140.201.39/admin.html`

## 📊 Funcionalidades del Panel Admin

- ✅ **Estadísticas:** Confirmados, no asisten, total personas
- 🔍 **Filtros:** Por nombre, asistencia, fecha
- 📋 **Ordenamiento:** Nombre, fecha, acompañantes
- 💾 **Exportación:** CSV con todos los datos
- 🔄 **Actualización:** En tiempo real

## 🎨 Diseño Visual

- **Colores:** Paleta dorada Universidad Panamericana (up-gold-50 a up-gold-900)
- **Tipografía:** Arial/Sans-serif para mejor legibilidad
- **Iconos:** Emojis para interfaz amigable
- **Layout:** Responsive con Tailwind CSS

## 📝 Datos de Prueba

El sistema incluye 4 confirmaciones de ejemplo:
- María González López (SÍ asiste, 2 acompañantes)
- Juan Carlos Pérez (SÍ asiste, 1 acompañante)
- Ana María Rodríguez (NO asiste)
- Luis Fernando Sánchez (SÍ asiste, 3 acompañantes)

## 🔧 Comandos Útiles

```bash
# Ver logs del contenedor
sudo docker-compose -f docker-compose-simple.yml logs -f

# Reiniciar servicios
sudo docker-compose -f docker-compose-simple.yml restart

# Parar todo
sudo docker-compose -f docker-compose-simple.yml down

# Estado de contenedores
sudo docker ps
```

## 📞 Soporte

Para soporte técnico o preguntas sobre el sistema, contactar al administrador del sistema.

---

**© 2025 Sistema de Invitaciones UP - Desarrollado con ❤️ para Universidad Panamericana**
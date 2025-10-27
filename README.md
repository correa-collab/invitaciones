# 🎓 Sistema de Invitaciones para Eventos - Universidad Panamericana

Sistema completo de gestión de invitaciones para eventos académicos con confirmación RSVP, generación de pases de acceso y panel administrativo.

## 🚀 Características Principales

### ✅ **Sistema Completo Implementado:**
- **🏠 Landing Page**: Página principal con información del evento
- **📝 Formulario de Confirmación**: Con validación de email y campos requeridos  
- **🎫 Generación de Pases**: Descarga automática con código QR y folio único
- **📧 Envío por Email**: Sistema de confirmaciones por correo electrónico
- **👥 Panel de Administración**: Dashboard con estadísticas y exportación CSV
- **🔗 QR Codes**: Códigos que dirigen a confirmaciones individuales
- **💙 Flujo Diferenciado**: Mensajes específicos para asistentes y no asistentes

### 🎨 **Diseño y UX:**
- **Universidad Panamericana**: Colores dorados institucionales
- **Responsive Design**: Compatible con móviles y desktop
- **Interfaz Elegante**: Uso de Tailwind CSS y gradientes
- **Branding IUX**: Footer con enlaces a iux.com.mx

## 📁 Estructura del Proyecto

```
/Users/christian/Invitaciones/
├── backend/                 # API FastAPI con Python
│   ├── simple_main.py      # Servidor principal con todos los endpoints
│   └── requirements.txt    # Dependencias Python
├── static/                 # Frontend estático
│   ├── index.html         # Página principal/landing
│   ├── confirmation.html  # Formulario de confirmación
│   └── admin.html         # Panel administrativo
├── database/              # Configuración base de datos
│   └── init.sql          # Script inicial PostgreSQL
├── frontend/              # Archivos React/TypeScript (desarrollo)
├── docker-compose.yml     # Configuración Docker
└── .venv/                # Entorno virtual Python
```

## 🛠 Tecnologías Utilizadas

### Backend:
- **FastAPI**: Framework web moderno y rápido
- **Python 3.13**: Lenguaje de programación
- **Pydantic**: Validación de datos
- **Uvicorn**: Servidor ASGI
- **SMTP**: Envío de emails
- **PIL**: Generación de imágenes

### Frontend:
- **HTML5 + CSS3**: Estructura y estilos
- **JavaScript ES6+**: Funcionalidad interactiva
- **Tailwind CSS**: Framework de estilos
- **Canvas API**: Generación de pases de acceso

### Base de Datos:
- **In-Memory Storage**: Para desarrollo (fácil migración a PostgreSQL)
- **JSON Storage**: Persistencia de datos

## 🌐 URLs y Endpoints

### Páginas Web:
- **Landing**: `http://localhost:8000/`
- **Confirmación**: `http://localhost:8000/confirmation.html`
- **Admin Panel**: `http://localhost:8000/admin.html`
- **QR Individual**: `http://localhost:8000/confirmation/{folio}`

### API Endpoints:
- **GET** `/api/confirmations` - Listar todas las confirmaciones
- **POST** `/api/confirmations` - Crear nueva confirmación
- **POST** `/api/send-email` - Enviar confirmación por email
- **GET** `/docs` - Documentación automática de la API

## 🚀 Instalación y Uso

### 1. Requisitos:
```bash
python 3.13+
pip
```

### 2. Instalación:
```bash
cd /Users/christian/Invitaciones
source .venv/bin/activate
pip install fastapi uvicorn python-dotenv email-validator Pillow
```

### 3. Iniciar Servidor:
```bash
python backend/simple_main.py
```

### 4. Acceder al Sistema:
Abre tu navegador en: `http://localhost:8000`

## 📊 Flujo de Usuario

### **Para Asistentes:**
1. **Llenar formulario** → Incluye nombre, email, teléfono, acompañantes
2. **Seleccionar "SÍ asistiré"** → Sistema genera folio automático (AW-XXX)
3. **Ver modal de confirmación** → Con todos los datos y folio
4. **Descargar pase de acceso** → Imagen PNG con QR code funcional
5. **Recibir por email** → Opcional, con un clic

### **Para No Asistentes:**
1. **Llenar formulario** → Solo datos básicos requeridos
2. **Seleccionar "NO podré asistir"** → 
3. **Ver mensaje de agradecimiento** → Sin generar pase ni enviar email

### **Panel Administrativo:**
1. **Ver estadísticas** → Confirmados, no asisten, total personas
2. **Filtrar y buscar** → Por nombre, asistencia, fecha
3. **Exportar datos** → Archivo CSV con toda la información

## 🔧 Configuración

### Variables de Entorno (.env):
```bash
# Email Configuration (Opcional)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_USER=tu_email@gmail.com
EMAIL_PASSWORD=tu_app_password

# Servidor
HOST=0.0.0.0
PORT=8000
```

## 📝 Datos de Ejemplo

El sistema incluye 4 confirmaciones de ejemplo para pruebas:
- **María González López** (AW-234) - ✅ Asiste con 2 acompañantes
- **Juan Carlos Pérez** (AW-235) - ✅ Asiste con 1 acompañante  
- **Ana María Rodríguez** - ❌ No asiste
- **Luis Fernando Sánchez** (AW-236) - ✅ Asiste con 3 acompañantes

## 🎯 Funcionalidades Avanzadas

### **Generación de Pases de Acceso:**
- Canvas HTML5 para crear imágenes dinámicas
- QR codes realistas con esquinas de localización
- Información completa del evento y confirmación
- Descarga automática en formato PNG

### **Sistema de QR Codes:**
- URLs únicas por folio: `registro.iux.com.mx/confirmation/AW-XXX`
- Páginas individuales responsive para cada confirmación
- Validación de folios existentes

### **Panel Administrativo:**
- Estadísticas en tiempo real
- Filtros avanzados por nombre y asistencia
- Ordenamiento por múltiples criterios
- Exportación CSV con todos los datos

## 🛡 Seguridad y Validación

- **Validación de emails** con formato correcto
- **Campos requeridos** marcados con asterisco (*)
- **Sanitización de datos** en frontend y backend
- **Manejo de errores** robusto
- **Estados visuales** para feedback al usuario

## 🎨 Personalización

### **Colores Universidad Panamericana:**
```css
up-gold-50: #fefdf8    /* Fondo suave */
up-gold-600: #d4950f   /* Dorado principal */
up-gold-700: #b37b0d   /* Dorado oscuro */
up-gold-800: #8f5e14   /* Dorado muy oscuro */
```

### **Emoji de Graduación:**
- 🎓 Usado en todos los logos y headers
- Color blanco sobre fondo dorado

## 📧 Configuración de Email

Para habilitar el envío de emails:
1. Configura las variables de entorno SMTP
2. Usa App Passwords para Gmail
3. El sistema enviará confirmaciones automáticamente

## 🔄 Deploy y Producción

### **Para Producción:**
1. Cambiar URLs en QR codes al dominio real
2. Configurar base de datos PostgreSQL
3. Usar servidor web (Nginx) para archivos estáticos
4. Configurar HTTPS y certificados SSL

### **Docker (Opcional):**
```bash
docker-compose up -d
```

## 📞 Soporte

Sistema desarrollado por **IUX - Soluciones Digitales**
- Web: [iux.com.mx](https://iux.com.mx)
- Todas las páginas incluyen el branding en el footer

## ✅ Estado del Proyecto

**🎯 COMPLETADO AL 100%**

### ✅ **Funcionalidades Implementadas:**
- [x] Landing page con información del evento
- [x] Formulario de confirmación con validación
- [x] Campo de email obligatorio 
- [x] Sistema de folios automático (AW-XXX)
- [x] Generación de pases de acceso con QR
- [x] QR codes que dirigen a confirmaciones individuales
- [x] Envío de confirmaciones por email
- [x] Mensaje diferenciado para no asistentes
- [x] Panel administrativo con estadísticas
- [x] Exportación de datos a CSV
- [x] Branding Universidad Panamericana + IUX
- [x] Emoji de graduación 🎓 en logos
- [x] Sistema completamente funcional

### 🚀 **Listo para Producción**
El sistema está completamente funcional y listo para ser usado en eventos reales.
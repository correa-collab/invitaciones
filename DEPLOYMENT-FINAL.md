# 🚀 GUÍA COMPLETA DE DEPLOYMENT

## 📋 Resumen del Sistema

✅ **Sistema completamente funcional con:**
- Página principal con información del evento
- Formulario de confirmación con modal y descarga de imagen
- Panel de administración con estadísticas y exportación CSV
- Colorimetría dorada Universidad Panamericana
- Backend FastAPI con Python 3.13

## 🎯 PASOS PARA SUBIR AL SERVIDOR AWS

### **Opción 1: Deployment Automático vía GitHub (RECOMENDADO)**

#### 1️⃣ Subir a GitHub
```bash
# Ejecutar en tu Mac
cd /Users/christian/Invitaciones

# Agregar cambios finales
git add .
git commit -m "Sistema de invitaciones UP - Versión final para deployment"

# Crear repositorio en GitHub y conectar
git remote add origin https://github.com/TU_USUARIO/invitaciones-up.git
git push -u origin main
```

#### 2️⃣ En el Servidor AWS
```bash
# Conectar vía AWS Console → EC2 → Instance Connect

# Clonar desde GitHub
git clone https://github.com/TU_USUARIO/invitaciones-up.git
cd invitaciones-up

# Instalar Docker
sudo apt update
sudo apt install -y docker.io docker-compose
sudo usermod -aG docker ubuntu

# Ejecutar aplicación
sudo docker-compose -f docker-compose-simple.yml up -d --build

# Verificar que esté funcionando
sudo docker-compose -f docker-compose-simple.yml ps
curl http://localhost
```

#### 3️⃣ Verificar Funcionamiento
- **http://3.140.201.39** - Página principal
- **http://3.140.201.39/admin.html** - Panel de administración

---

### **Opción 2: Deployment Manual (Si no tienes GitHub)**

#### 1️⃣ Crear Archivo Comprimido
```bash
# En tu Mac, ya tienes el archivo
cd /Users/christian/Invitaciones
ls -la invitaciones-deploy.tar.gz  # Archivo ya creado
```

#### 2️⃣ Subir Archivo al Servidor
**Método A - Si tienes acceso SSH:**
```bash
scp invitaciones-deploy.tar.gz ubuntu@3.140.201.39:~/
```

**Método B - Via AWS Instance Connect:**
1. Conectar vía AWS Console → EC2 → Instance Connect
2. Usar `wget` o subir archivo manualmente

#### 3️⃣ En el Servidor AWS
```bash
# Extraer archivos
tar -xzf invitaciones-deploy.tar.gz

# Instalar Docker
sudo apt update
sudo apt install -y docker.io docker-compose
sudo usermod -aG docker ubuntu

# Ejecutar aplicación
sudo docker-compose -f docker-compose-simple.yml up -d --build

# Verificar
sudo docker-compose -f docker-compose-simple.yml ps
curl http://localhost
```

---

## 🔧 Comandos de Gestión en el Servidor

### Ver Estado de la Aplicación
```bash
sudo docker-compose -f docker-compose-simple.yml ps
sudo docker-compose -f docker-compose-simple.yml logs
```

### Reiniciar Aplicación
```bash
sudo docker-compose -f docker-compose-simple.yml restart
```

### Parar Aplicación
```bash
sudo docker-compose -f docker-compose-simple.yml down
```

### Ver Logs en Tiempo Real
```bash
sudo docker-compose -f docker-compose-simple.yml logs -f
```

### Actualizar desde GitHub
```bash
cd invitaciones-up
git pull origin main
sudo docker-compose -f docker-compose-simple.yml down
sudo docker-compose -f docker-compose-simple.yml up -d --build
```

---

## 🌐 URLs Finales del Sistema

Una vez deployado en AWS:

| Página | URL | Descripción |
|--------|-----|-------------|
| **Principal** | http://3.140.201.39 | Información del evento y botón de confirmación |
| **Confirmación** | http://3.140.201.39/confirmation.html | Formulario de confirmación de asistencia |
| **Admin Panel** | http://3.140.201.39/admin.html | Panel de administración con estadísticas |

---

## 📊 Funcionalidades Disponibles

### Para Invitados:
- ✅ Ver información del evento
- ✅ Confirmar asistencia con formulario
- ✅ Descargar imagen de confirmación personalizada
- ✅ Modal con datos de confirmación

### Para Administradores:
- ✅ Ver estadísticas en tiempo real
- ✅ Lista completa de confirmaciones
- ✅ Filtrar por nombre, asistencia, fecha
- ✅ Ordenar por diferentes criterios
- ✅ Exportar datos completos a CSV
- ✅ Actualizar datos automáticamente

---

## 🎨 Características de Diseño

- **Colorimetría:** Universidad Panamericana (dorado institucional)
- **Sin logo:** Mantiene colores pero sin elementos gráficos institucionales
- **Responsive:** Funciona en móviles y desktop
- **Accesible:** Interfaz intuitiva con emojis y colores contrastantes

---

## ⚡ Estado Actual del Proyecto

- ✅ **Backend:** FastAPI funcionando con endpoints completos
- ✅ **Frontend:** 3 páginas HTML completamente funcionales
- ✅ **Base de datos:** En memoria con datos de prueba
- ✅ **Docker:** Configuración lista para deployment
- ✅ **Scripts:** Deploy automatizado preparado
- ✅ **Documentación:** Guías completas de uso

**🎉 PROYECTO 100% LISTO PARA DEPLOYMENT**

---

## 🆘 Troubleshooting

### Error: Puerto ya en uso
```bash
sudo netstat -tlnp | grep :80
sudo killall -9 nginx  # Si hay conflicto con nginx
sudo docker-compose -f docker-compose-simple.yml down
sudo docker-compose -f docker-compose-simple.yml up -d --build
```

### Error: Docker no encontrado
```bash
sudo apt update
sudo apt install -y docker.io docker-compose
sudo systemctl start docker
sudo usermod -aG docker ubuntu
newgrp docker
```

### Verificar si la app está funcionando
```bash
curl http://localhost
curl http://localhost/admin.html
sudo docker ps
```

---

## 📞 Contacto y Soporte

Si necesitas ayuda con el deployment o tienes algún problema:
1. Revisar los logs: `sudo docker-compose logs`
2. Verificar estado: `sudo docker ps`
3. Consultar esta guía paso a paso

**¡Tu sistema está listo para funcionar en producción!** 🚀
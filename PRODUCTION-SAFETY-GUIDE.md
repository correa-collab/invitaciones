# 🛡️ GUÍA DE DEPLOYMENT SEGURO PARA PRODUCCIÓN

## ⚠️ REGLAS DE ORO:

### ❌ **NUNCA EN PRODUCCIÓN:**
```bash
# PELIGROSO - Borra bases de datos
sudo docker-compose down -v
sudo docker system prune -af --volumes
sudo docker rmi $(sudo docker images -q)
```

### ✅ **SIEMPRE EN PRODUCCIÓN:**
```bash
# SEGURO - Preserva bases de datos
sudo docker-compose stop frontend backend
sudo docker-compose build --no-cache frontend backend
sudo docker-compose up -d
```

## 📋 **PROTOCOLO DE ACTUALIZACIÓN SEGURA:**

### 1️⃣ **Backup Automático:**
```bash
# Crear backup antes de cualquier cambio
mkdir -p backups/$(date +%Y%m%d_%H%M%S)
sudo docker exec container_db pg_dump -U postgres db_name > backup.sql
```

### 2️⃣ **Actualización de Código:**
```bash
cd /home/ubuntu/invitaciones
git stash  # Guardar cambios locales
git pull origin main
```

### 3️⃣ **Actualización de Servicios:**
```bash
# Para archivos estáticos (HTML, CSS, JS)
sudo docker-compose restart frontend

# Para código del backend
sudo docker-compose build --no-cache backend
sudo docker-compose up -d backend
```

### 4️⃣ **Verificación:**
```bash
sudo docker-compose ps
curl -s http://localhost/health
```

## 🗄️ **TIPOS DE DATOS:**

| Tipo | Se Borra | Se Preserva | Comando Seguro |
|------|----------|-------------|----------------|
| **Archivos HTML/CSS** | ✅ Se pueden borrar | ❌ No crítico | `restart frontend` |
| **Código Backend** | ✅ Se puede borrar | ❌ No crítico | `build backend` |
| **Base de Datos** | ❌ NUNCA borrar | ✅ CRÍTICO | Usar volúmenes |
| **Archivos subidos** | ❌ NUNCA borrar | ✅ CRÍTICO | Usar volúmenes |

## 🚀 **COMANDOS RECOMENDADOS:**

### **Para cambios de frontend:**
```bash
./safe-production-update.sh
```

### **Para cambios de backend:**
```bash
sudo docker-compose build --no-cache backend
sudo docker-compose up -d backend
```

### **Para emergencias (con backup):**
```bash
# 1. Backup
./backup-database.sh

# 2. Actualizar
./nuclear-fix.sh  # Solo si es necesario

# 3. Restaurar datos si hay problemas
./restore-database.sh
```

## 💡 **RECOMENDACIONES:**

1. **Usar volúmenes nombrados** para datos persistentes
2. **Backup automático** antes de cambios
3. **Testing en staging** antes de producción
4. **Rollback plan** siempre listo
5. **Monitoreo** después de cambios

## 🔍 **DETECCIÓN DE PROBLEMAS:**

Si después de una actualización:
- ❌ Los usuarios no pueden acceder → Problema de frontend
- ❌ Las confirmaciones no se guardan → Problema de backend/BD
- ❌ Los emails no se envían → Problema de configuración

**¡La clave es NUNCA usar comandos que borren volúmenes en producción! 🛡️**
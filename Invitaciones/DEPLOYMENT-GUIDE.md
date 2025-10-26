# 🚀 Guía Completa para Subir el Proyecto al Servidor AWS

## 📋 Pasos para Deployment

### 1️⃣ **Preparar el Proyecto Localmente** ✅
Ya tienes todos los archivos listos en tu Mac:
- ✅ Backend FastAPI con Python
- ✅ Frontend React con TypeScript  
- ✅ Docker Compose configurado
- ✅ Variables de entorno configuradas

---

### 2️⃣ **Conectar al Servidor AWS**

**Opción A: EC2 Instance Connect (Recomendado)**
1. Ve a AWS Console → EC2 → Instancias
2. Selecciona tu instancia `i-0c5c0d1bf71ba1f28`
3. Click "Conectar" → "Conexión de instancia EC2"
4. Se abrirá un terminal en el navegador

**Opción B: SSH (si funciona)**
```bash
ssh ubuntu@3.140.201.39
```

---

### 3️⃣ **Preparar el Servidor**

Una vez conectado al servidor, ejecuta estos comandos:

```bash
# Actualizar el sistema
sudo apt update && sudo apt upgrade -y

# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu
newgrp docker

# Instalar Docker Compose
sudo apt install -y docker-compose

# Instalar Git (si no está)
sudo apt install -y git unzip

# Crear directorio del proyecto
mkdir -p ~/invitaciones
cd ~/invitaciones
```

---

### 4️⃣ **Subir Archivos al Servidor**

**Opción A: Usando GitHub (Recomendado)**
```bash
# Si subes el proyecto a GitHub, clonarlo:
git clone https://github.com/tu-usuario/invitaciones.git .
```

**Opción B: Transferir archivos manualmente**
1. Comprimir el proyecto en tu Mac:
   ```bash
   cd /Users/christian/Invitaciones
   tar -czf invitaciones.tar.gz --exclude=node_modules --exclude=venv .
   ```

2. Subir usando scp (desde tu Mac):
   ```bash
   scp invitaciones.tar.gz ubuntu@3.140.201.39:~/
   ```

3. En el servidor, descomprimir:
   ```bash
   cd ~/invitaciones
   tar -xzf ../invitaciones.tar.gz
   ```

---

### 5️⃣ **Ejecutar la Aplicación**

En el servidor, dentro de `~/invitaciones`:

```bash
# Verificar que los archivos están ahí
ls -la

# Ver contenido del docker-compose
cat docker-compose.yml

# Construir y ejecutar todos los servicios
sudo docker-compose up -d --build

# Verificar que todo está funcionando
sudo docker-compose ps

# Ver logs si hay problemas
sudo docker-compose logs
```

---

### 6️⃣ **Verificar que Funciona**

Una vez ejecutado, verifica en tu navegador:

- **Frontend**: http://3.140.201.39
- **API Docs**: http://3.140.201.39/docs  
- **Backend**: http://3.140.201.39/api

---

### 🛠 **Comandos Útiles**

```bash
# Ver logs en tiempo real
sudo docker-compose logs -f

# Reiniciar servicios
sudo docker-compose restart

# Parar todo
sudo docker-compose down

# Ver estado de contenedores
sudo docker ps

# Limpiar sistema
sudo docker system prune -f
```

---

### 🔧 **Troubleshooting**

**Si hay errores:**

1. **Puerto ya en uso:**
   ```bash
   sudo netstat -tlnp | grep :80
   sudo killall -9 nginx
   ```

2. **Problemas de permisos:**
   ```bash
   sudo chown -R ubuntu:ubuntu ~/invitaciones
   ```

3. **Reiniciar Docker:**
   ```bash
   sudo systemctl restart docker
   ```

---

### 🎯 **Estado Actual**

- ✅ Proyecto creado y configurado
- ✅ Docker Compose listo
- ✅ Variables de entorno configuradas
- 🔄 **Siguiente**: Subir al servidor siguiendo esta guía

**¿Qué método prefieres para subir los archivos al servidor?**
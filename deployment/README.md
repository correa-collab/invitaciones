# Scripts de Deployment

## 🚀 Deploy a AWS EC2

Este directorio contiene scripts para hacer deployment automático al servidor AWS.

### Prerequisitos

1. **Servidor EC2 configurado** (IP: 3.140.201.39)
2. **Docker y Docker Compose instalados** en el servidor
3. **Acceso SSH** al servidor
4. **Puertos abiertos**: 80, 443, 22

### 🔧 Setup Inicial del Servidor

```bash
# Conectar al servidor
ssh ubuntu@3.140.201.39

# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu

# Instalar Docker Compose
sudo apt install docker-compose -y

# Instalar Git
sudo apt install git -y

# Reiniciar para aplicar cambios
sudo reboot
```

### 📦 Deploy de la Aplicación

```bash
# 1. Clonar el proyecto en el servidor
git clone <tu-repo-url> invitaciones
cd invitaciones

# 2. Configurar variables de entorno
cp backend/.env.example backend/.env
# Editar backend/.env con tus configuraciones

# 3. Construir y ejecutar
docker-compose up -d --build

# 4. Verificar que todo funciona
docker-compose ps
curl http://localhost
curl http://localhost/api/docs
```

### 🔄 Actualizar la Aplicación

```bash
# En el servidor
cd invitaciones
git pull origin main
docker-compose down
docker-compose up -d --build
```

### 📋 Comandos Útiles

```bash
# Ver logs
docker-compose logs -f

# Ver logs específicos
docker-compose logs -f backend
docker-compose logs -f frontend

# Reiniciar servicios
docker-compose restart

# Parar todo
docker-compose down

# Limpiar sistema
docker system prune -f
```

### 🌐 URLs de la Aplicación

Una vez deployado, accede a:

- **Frontend**: http://3.140.201.39
- **API Docs**: http://3.140.201.39/api/docs
- **Backend**: http://3.140.201.39/api

### 🔒 Configurar HTTPS (Opcional)

Para producción, configura SSL con Let's Encrypt:

```bash
# Instalar certbot
sudo apt install certbot python3-certbot-nginx

# Obtener certificado
sudo certbot --nginx -d tu-dominio.com

# Renovación automática
sudo crontab -e
# Agregar: 0 12 * * * /usr/bin/certbot renew --quiet
```
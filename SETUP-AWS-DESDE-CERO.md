# 🆘 SOLUCIÓN: Configurar AWS desde CERO

## El problema actual:
- ❌ No existe el repositorio git en el servidor
- ❌ No existe el servicio systemd
- ❌ Error de "externally-managed-environment"

---

## ✅ SOLUCIÓN COMPLETA EN 3 PASOS

### Paso 1: Subir el script al servidor
```bash
cd /Users/christian/Invitaciones
scp setup-aws-initial.sh ubuntu@3.140.201.39:~/
```

### Paso 2: Conectar al servidor
```bash
ssh ubuntu@3.140.201.39
```

### Paso 3: Ejecutar el script de configuración
```bash
chmod +x setup-aws-initial.sh
./setup-aws-initial.sh
```

**¡ESO ES TODO!** El script hace todo automáticamente:
- ✅ Instala dependencias del sistema
- ✅ Clona el repositorio desde GitHub
- ✅ Crea entorno virtual
- ✅ Instala dependencias Python
- ✅ Configura email_config.py con credenciales
- ✅ Configura Nginx
- ✅ Crea y activa el servicio systemd
- ✅ Inicia el servidor

---

## 🔍 Verificar que funcionó

Después de ejecutar el script, verifica:

```bash
# Ver estado del servicio
sudo systemctl status invitaciones

# Ver logs en tiempo real
sudo journalctl -u invitaciones -f

# Probar endpoint
curl http://localhost:8000/test
```

**Abre en tu navegador:**
- http://3.140.201.39

---

## 🔄 Para futuras actualizaciones (DESPUÉS de la instalación inicial)

Una vez configurado, usa este comando simple:

```bash
ssh ubuntu@3.140.201.39 << 'EOF'
cd /var/www/invitaciones
git pull origin main
source .venv/bin/activate
pip install --upgrade fastapi uvicorn python-dotenv email-validator
sudo systemctl restart invitaciones
sudo systemctl status invitaciones --no-pager -l
EOF
```

O desde tu computadora:
```bash
cd /Users/christian/Invitaciones
./deploy-quick.sh
```

---

## 🆘 Si algo falla

### Ver logs detallados:
```bash
sudo journalctl -u invitaciones -n 100 --no-pager
```

### Verificar archivos:
```bash
ls -la /var/www/invitaciones/
ls -la /var/www/invitaciones/backend/
```

### Reiniciar todo:
```bash
sudo systemctl restart invitaciones nginx
```

### Probar manualmente:
```bash
cd /var/www/invitaciones/backend
source ../.venv/bin/activate
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000
```

---

## 📝 Resumen de comandos clave

### Desde tu Mac:
```bash
# 1. Subir script
scp setup-aws-initial.sh ubuntu@3.140.201.39:~/

# 2. Conectar
ssh ubuntu@3.140.201.39

# 3. Ejecutar (en el servidor)
chmod +x setup-aws-initial.sh && ./setup-aws-initial.sh
```

### En el servidor AWS:
```bash
# Ver estado
sudo systemctl status invitaciones

# Ver logs
sudo journalctl -u invitaciones -f

# Reiniciar
sudo systemctl restart invitaciones

# Actualizar código
cd /var/www/invitaciones && git pull origin main && sudo systemctl restart invitaciones
```

---

## ✅ Checklist de Verificación

Después de la instalación, verifica que:
- [ ] El servicio está corriendo: `sudo systemctl status invitaciones`
- [ ] Nginx está activo: `sudo systemctl status nginx`
- [ ] El endpoint responde: `curl http://localhost:8000/test`
- [ ] La página carga en el navegador: http://3.140.201.39
- [ ] El formulario funciona correctamente
- [ ] Los emails se envían

---

## 🎯 Siguiente paso

**Ejecuta ahora:**
```bash
cd /Users/christian/Invitaciones
scp setup-aws-initial.sh ubuntu@3.140.201.39:~/
ssh ubuntu@3.140.201.39
```

Y luego en el servidor:
```bash
chmod +x setup-aws-initial.sh && ./setup-aws-initial.sh
```

¡Listo! 🎉

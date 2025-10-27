# 🚀 Guía Completa de Deployment a AWS

## 📋 Información del Servidor
- **IP:** 3.140.201.39
- **Usuario:** ubuntu
- **Dominio:** registro.iux.com.mx
- **Puerto:** 8000 (interno) / 80 (externo)

---

## ✅ OPCIÓN 1: Deployment Automático (Recomendado)

### Paso 1: Ejecutar script automático
```bash
cd /Users/christian/Invitaciones
chmod +x deploy-to-server.sh
./deploy-to-server.sh
```

**Si hay error de conexión SSH, continúa con la Opción 2 (Manual)**

---

## 🔧 OPCIÓN 2: Deployment Manual (Paso a Paso)

### Paso 1: Conectarse al servidor AWS
```bash
ssh ubuntu@3.140.201.39
```

### Paso 2: Ir al directorio del proyecto
```bash
cd /var/www/invitaciones
```

### Paso 3: Hacer backup de configuraciones importantes
```bash
# Backup del email_config.py si existe
cp backend/email_config.py /tmp/email_config_backup.py 2>/dev/null || echo "No hay config anterior"

# Backup del .env si existe
cp .env /tmp/env_backup 2>/dev/null || echo "No hay .env anterior"
```

### Paso 4: Actualizar código desde GitHub
```bash
# Traer últimos cambios
git fetch origin

# Guardar cambios locales si los hay
git stash

# Actualizar a la última versión
git reset --hard origin/main
git pull origin main

# Ver el último commit
git log --oneline -1
```

### Paso 5: Restaurar configuraciones sensibles
```bash
# Restaurar email_config.py
cp /tmp/email_config_backup.py backend/email_config.py 2>/dev/null || echo "Crear nuevo email_config.py"

# Si no existe, crear uno nuevo con tus credenciales
cat > backend/email_config.py << 'EOF'
"""
Configuracion de email
"""

EMAIL_CONFIG = {
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "email": "correa@iux.com.mx",
    "password": "qxpc egxf nnvd lvpj",
    "enabled": True
}
EOF
```

### Paso 6: Actualizar dependencias Python
```bash
# Activar entorno virtual
source .venv/bin/activate

# Actualizar pip
pip install --upgrade pip

# Instalar/actualizar dependencias
pip install fastapi uvicorn python-dotenv email-validator
```

### Paso 7: Verificar que los archivos estén correctos
```bash
# Ver estructura del backend
ls -la backend/

# Verificar que existan los archivos clave
ls backend/main.py
ls backend/email_service.py
ls backend/email_config.py
ls static/confirmation.html

# Ver primeras líneas del main.py
head -20 backend/main.py
```

### Paso 8: Probar el servidor manualmente (opcional)
```bash
# Detener el servicio actual
sudo systemctl stop invitaciones

# Probar el servidor manualmente
cd backend
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000

# Si funciona, presiona Ctrl+C para detenerlo
```

### Paso 9: Actualizar y reiniciar el servicio systemd
```bash
# Actualizar configuración del servicio
sudo tee /etc/systemd/system/invitaciones.service << 'EOF'
[Unit]
Description=Sistema de Invitaciones - Universidad Panamericana
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/var/www/invitaciones/backend
Environment=PATH=/var/www/invitaciones/.venv/bin
ExecStart=/var/www/invitaciones/.venv/bin/python -m uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

# Recargar configuración
sudo systemctl daemon-reload

# Reiniciar servicio
sudo systemctl restart invitaciones

# Verificar estado
sudo systemctl status invitaciones
```

### Paso 10: Verificar logs en tiempo real
```bash
# Ver logs del servicio
sudo journalctl -u invitaciones -f

# O ver logs de las últimas 50 líneas
sudo journalctl -u invitaciones -n 50
```

### Paso 11: Verificar que Nginx esté funcionando
```bash
# Estado de Nginx
sudo systemctl status nginx

# Probar configuración
sudo nginx -t

# Recargar si es necesario
sudo systemctl reload nginx
```

### Paso 12: Probar endpoints desde el servidor
```bash
# Probar endpoint local
curl http://localhost:8000/test

# Probar endpoint público
curl http://3.140.201.39/test
```

---

## 🧪 Verificación Post-Deployment

### Desde tu computadora local:
```bash
# Probar acceso a la página principal
curl http://3.140.201.39/

# O abrir en navegador:
# http://3.140.201.39
# http://registro.iux.com.mx
```

### Verificar que todo funcione:
1. ✅ Página de confirmación carga correctamente
2. ✅ Formulario acepta datos
3. ✅ Se guardan confirmaciones en `data/confirmations.json`
4. ✅ Emails se envían correctamente
5. ✅ Validación de acompañantes funciona (0 si no asiste)

---

## 🔍 Comandos de Diagnóstico

### Ver estado de servicios:
```bash
# Estado del servicio de invitaciones
sudo systemctl status invitaciones

# Estado de Nginx
sudo systemctl status nginx

# Ver procesos Python corriendo
ps aux | grep python

# Ver si el puerto 8000 está abierto
sudo lsof -i :8000
```

### Ver logs:
```bash
# Logs del servicio (últimas 100 líneas)
sudo journalctl -u invitaciones -n 100

# Logs de Nginx (errores)
sudo tail -f /var/log/nginx/error.log

# Logs de Nginx (accesos)
sudo tail -f /var/log/nginx/access.log
```

### Reiniciar servicios:
```bash
# Reiniciar servicio de invitaciones
sudo systemctl restart invitaciones

# Reiniciar Nginx
sudo systemctl restart nginx

# Reiniciar ambos
sudo systemctl restart invitaciones nginx
```

---

## 🆘 Solución de Problemas Comunes

### Problema: El servicio no inicia
```bash
# Ver error específico
sudo journalctl -u invitaciones -n 50

# Verificar que el archivo main.py existe
ls -la /var/www/invitaciones/backend/main.py

# Verificar permisos
sudo chown -R ubuntu:ubuntu /var/www/invitaciones
```

### Problema: Error de importación
```bash
# Reinstalar dependencias
cd /var/www/invitaciones
source .venv/bin/activate
pip install --force-reinstall fastapi uvicorn python-dotenv email-validator
```

### Problema: Error 502 Bad Gateway
```bash
# Verificar que el servicio esté corriendo
sudo systemctl status invitaciones

# Verificar logs
sudo journalctl -u invitaciones -n 50

# Reiniciar servicio
sudo systemctl restart invitaciones
```

### Problema: No se envían emails
```bash
# Verificar configuración de email
cat /var/www/invitaciones/backend/email_config.py

# Probar email manualmente
cd /var/www/invitaciones/backend
source ../.venv/bin/activate
python test_email.py
```

---

## 📝 Comandos Rápidos de Referencia

```bash
# Conectar al servidor
ssh ubuntu@3.140.201.39

# Ir al proyecto
cd /var/www/invitaciones

# Actualizar código
git pull origin main

# Reiniciar servicio
sudo systemctl restart invitaciones

# Ver logs
sudo journalctl -u invitaciones -f

# Ver estado
sudo systemctl status invitaciones nginx

# Salir del servidor
exit
```

---

## 🎯 Checklist Post-Deployment

- [ ] Código actualizado desde GitHub
- [ ] Dependencias instaladas/actualizadas
- [ ] `email_config.py` restaurado con credenciales
- [ ] Servicio systemd actualizado y reiniciado
- [ ] Nginx funcionando correctamente
- [ ] Sitio accesible desde http://3.140.201.39
- [ ] Formulario de confirmación funciona
- [ ] Emails se envían correctamente
- [ ] Validación de acompañantes activa
- [ ] Logs sin errores

---

## 📞 Soporte

Si encuentras problemas:
1. Revisa los logs: `sudo journalctl -u invitaciones -n 100`
2. Verifica el estado: `sudo systemctl status invitaciones`
3. Prueba manualmente: `cd backend && python3 -m uvicorn main:app --host 0.0.0.0 --port 8000`

# ⚡ COMANDOS RÁPIDOS PARA ACTUALIZAR AWS

## 🎯 Opción 1: SUPER RÁPIDO (Automático)
```bash
cd /Users/christian/Invitaciones
./deploy-quick.sh
```

---

## 🎯 Opción 2: MANUAL (5 comandos)

### 1. Conectar al servidor:
```bash
ssh ubuntu@3.140.201.39
```

### 2. Actualizar código:
```bash
cd /var/www/invitaciones && git pull origin main
```

### 3. Actualizar dependencias:
```bash
source .venv/bin/activate && pip install --upgrade fastapi uvicorn python-dotenv email-validator
```

### 4. Reiniciar servicio:
```bash
sudo systemctl restart invitaciones
```

### 5. Verificar estado:
```bash
sudo systemctl status invitaciones
curl http://localhost:8000/test
```

---

## ✅ Verificar que funcionó
Abre en tu navegador:
- http://3.140.201.39
- http://registro.iux.com.mx

---

## 🆘 Si hay problemas

### Ver logs:
```bash
sudo journalctl -u invitaciones -n 50
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

## 📝 IMPORTANTE: Restaurar email_config.py

Si los emails no funcionan después del deploy, ejecuta en el servidor:

```bash
cat > /var/www/invitaciones/backend/email_config.py << 'EOF'
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

sudo systemctl restart invitaciones
```

---

## 🎉 ¡Listo!

Después de ejecutar cualquiera de las opciones, tu servidor AWS estará actualizado con:
- ✅ Último código de GitHub
- ✅ Sistema de confirmaciones funcional
- ✅ Validación de acompañantes (0 si no asiste)
- ✅ Emails automáticos con pases adjuntos
- ✅ Interfaz mejorada

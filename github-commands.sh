#!/bin/bash

echo "🚀 Comandos para conectar con GitHub"
echo "=================================="
echo ""

echo "1️⃣ Después de crear el repo en GitHub, ejecuta:"
echo ""

echo "# Agregar el repositorio remoto (reemplaza TU-USUARIO)"
echo "git remote add origin https://github.com/TU-USUARIO/sistema-invitaciones.git"
echo ""

echo "# Verificar rama principal"
echo "git branch -M main"
echo ""

echo "# Subir código a GitHub"
echo "git push -u origin main"
echo ""

echo "2️⃣ Una vez subido, verifica en:"
echo "   https://github.com/TU-USUARIO/sistema-invitaciones"
echo ""

echo "3️⃣ Luego en el servidor AWS ejecuta:"
echo "   git clone https://github.com/TU-USUARIO/sistema-invitaciones.git ~/invitaciones"
echo "   cd ~/invitaciones"
echo "   sudo docker-compose up -d --build"
echo ""

echo "✅ ¡Tu app estará en http://3.140.201.39!"
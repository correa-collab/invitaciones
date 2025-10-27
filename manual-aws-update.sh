#!/bin/bash

echo "🔄 ACTUALIZACIÓN MANUAL DEL SERVIDOR AWS"
echo "======================================="

echo "🌐 Conectando al servidor: 3.140.201.39"
echo "📂 Directorio del proyecto: /home/ubuntu/invitaciones"
echo ""

echo "🚀 COMANDOS PARA EJECUTAR EN EL SERVIDOR:"
echo "----------------------------------------"

cat << 'EOF'
# 1. Conectar al servidor AWS
ssh ubuntu@3.140.201.39

# 2. Una vez conectado, ejecutar estos comandos:
cd /home/ubuntu/invitaciones

# 3. Actualizar código desde GitHub
echo "🔄 Actualizando código desde GitHub..."
git fetch origin
git reset --hard origin/main
git pull origin main

# 4. Reconstruir contenedores Docker
echo "🐳 Reconstruyendo contenedores Docker..."
sudo docker-compose down
sudo docker-compose up -d --build

# 5. Esperar que se inicien los servicios
echo "⏱️ Esperando que los servicios se inicien..."
sleep 15

# 6. Verificar estado
echo "📊 Estado de los servicios:"
sudo docker-compose ps

# 7. Verificar conectividad
echo "🌐 Verificando conectividad..."
curl -s http://localhost/health || echo '❌ Health check falló'

# 8. Verificar logs si hay problemas
echo "📝 Logs recientes:"
sudo docker-compose logs --tail=20

echo "🎉 ¡Actualización completa!"
EOF

echo ""
echo "🎯 URLs después de la actualización:"
echo "🌐 Frontend: http://registro.iux.com.mx"
echo "🌐 Frontend: http://3.140.201.39"
echo "📚 API Docs: http://registro.iux.com.mx/docs"
echo "❤️ Health: http://registro.iux.com.mx/health"
echo ""

echo "💡 INSTRUCCIONES:"
echo "1. Copia y pega los comandos de arriba"
echo "2. O ejecuta este archivo directamente con ./manual-aws-update.sh"
echo "3. Verifica que el sitio esté funcionando en http://registro.iux.com.mx"
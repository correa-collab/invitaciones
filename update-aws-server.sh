#!/bin/bash

echo "🔄 Script de Actualización del Servidor AWS"
echo "==========================================="

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

SERVER_IP="3.140.201.39"
PROJECT_DIR="/home/ubuntu/invitaciones"

echo -e "${BLUE}📡 Conectando al servidor AWS: $SERVER_IP${NC}"

# Comando completo para ejecutar en el servidor
REMOTE_COMMANDS="
cd $PROJECT_DIR && \
echo '🔄 Actualizando código desde GitHub...' && \
git fetch origin && \
git reset --hard origin/main && \
git pull origin main && \
echo '✅ Código actualizado' && \
echo '🐳 Reconstruyendo contenedores Docker...' && \
sudo docker-compose down && \
sudo docker-compose up -d --build && \
echo '⏱️ Esperando que los servicios se inicien...' && \
sleep 15 && \
echo '📊 Estado de los servicios:' && \
sudo docker-compose ps && \
echo '🌐 Verificando conectividad...' && \
curl -s http://localhost/health || echo '❌ Health check falló' && \
echo '🎉 ¡Actualización completa!'
"

# Ejecutar comandos remotos
echo -e "${YELLOW}🚀 Ejecutando actualización en el servidor...${NC}"

# Opción 1: Si tienes acceso SSH directo
if [ -f ~/.ssh/invitaciones-key.pem ]; then
    echo -e "${GREEN}🔑 Usando clave SSH...${NC}"
    ssh -i ~/.ssh/invitaciones-key.pem ubuntu@$SERVER_IP "$REMOTE_COMMANDS"
else
    echo -e "${YELLOW}⚠️ No se encontró la clave SSH. Usando métodos alternativos...${NC}"
    
    # Opción 2: Crear un script temporal para copiar al servidor
    echo -e "${BLUE}📝 Creando script de actualización temporal...${NC}"
    
    cat > temp_update_script.sh << EOF
#!/bin/bash
cd $PROJECT_DIR
echo '🔄 Actualizando código desde GitHub...'
git fetch origin
git reset --hard origin/main
git pull origin main
echo '✅ Código actualizado'

echo '🐳 Reconstruyendo contenedores Docker...'
sudo docker-compose down
sudo docker-compose up -d --build

echo '⏱️ Esperando que los servicios se inicien...'
sleep 15

echo '📊 Estado de los servicios:'
sudo docker-compose ps

echo '🌐 Verificando conectividad...'
curl -s http://localhost/health || echo '❌ Health check falló'

echo '🎉 ¡Actualización completa!'
echo '🌐 Tu sitio está disponible en: http://registro.iux.com.mx'
EOF

    chmod +x temp_update_script.sh
    
    echo -e "${GREEN}📋 Script creado: temp_update_script.sh${NC}"
    echo -e "${YELLOW}📤 Para aplicar la actualización, ejecuta este script en el servidor AWS:${NC}"
    echo -e "${BLUE}$(cat temp_update_script.sh)${NC}"
    
    echo ""
    echo -e "${RED}🚨 INSTRUCCIONES MANUALES:${NC}"
    echo "1. Conecta al servidor AWS"
    echo "2. Ejecuta los comandos mostrados arriba"
    echo "3. Verifica que http://registro.iux.com.mx esté actualizado"
fi

echo ""
echo -e "${GREEN}🎯 URLs después de la actualización:${NC}"
echo "🌐 Frontend: http://registro.iux.com.mx"
echo "🌐 Frontend: http://3.140.201.39"
echo "📚 API Docs: http://registro.iux.com.mx/docs"
echo "❤️ Health: http://registro.iux.com.mx/health"
echo "📋 Confirmación: http://registro.iux.com.mx/confirmation.html"

echo ""
echo -e "${BLUE}💡 Si necesitas ayuda manual:${NC}"
echo "1. ssh ubuntu@3.140.201.39"
echo "2. cd /home/ubuntu/invitaciones"
echo "3. git pull origin main"
echo "4. sudo docker-compose up -d --build"
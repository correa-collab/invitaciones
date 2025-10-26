#!/bin/bash

echo "🎯 COMANDOS PARA EL SERVIDOR AWS"
echo "================================="
echo ""

echo "Una vez que el código esté en GitHub, conecta al servidor AWS y ejecuta:"
echo ""

echo "1️⃣ Conectar al servidor:"
echo "   - AWS Console → EC2 → tu instancia → 'Conectar' → 'EC2 Instance Connect'"
echo "   - O por SSH: ssh ubuntu@3.140.201.39"
echo ""

echo "2️⃣ Preparar servidor:"
echo "sudo apt update && sudo apt upgrade -y"
echo "curl -fsSL https://get.docker.com -o get-docker.sh"
echo "sudo sh get-docker.sh"
echo "sudo usermod -aG docker ubuntu"
echo "sudo apt install -y docker-compose git"
echo "newgrp docker"
echo ""

echo "3️⃣ Clonar y ejecutar:"
echo "git clone https://github.com/correa-collab/invitaciones.git ~/invitaciones"
echo "cd ~/invitaciones"
echo "sudo docker-compose up -d --build"
echo ""

echo "4️⃣ Verificar:"
echo "sudo docker-compose ps"
echo "sudo docker-compose logs"
echo ""

echo "🌐 Tu aplicación estará disponible en:"
echo "   Frontend: http://3.140.201.39"
echo "   API Docs: http://3.140.201.39/api/docs"
echo "   Dashboard: http://3.140.201.39/dashboard"
echo ""

echo "📋 Comandos útiles:"
echo "   Ver logs: sudo docker-compose logs -f"
echo "   Reiniciar: sudo docker-compose restart"
echo "   Parar: sudo docker-compose down"
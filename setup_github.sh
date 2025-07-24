#!/bin/bash
# Script para configurar el repositorio de GitHub

echo "🚀 Configurando Discord Suggestions Bot para GitHub..."

# Inicializar git si no existe
if [ ! -d ".git" ]; then
    echo "📝 Inicializando repositorio Git..."
    git init
else
    echo "✅ Repositorio Git ya existe"
fi

# Configurar archivos para commit
echo "📦 Preparando archivos para commit..."
git add .

# Crear commit inicial
echo "💾 Creando commit inicial..."
git commit -m "Initial commit: Discord Suggestions Bot with button voting system

Features:
- Spanish slash commands (/sugerir, /config_canal, /ayuda)
- Integrated Discord button voting system
- One vote per user with vote switching
- Real-time vote counting
- Server-specific channel configuration
- 24/7 deployment ready for Render.com

Ready for production deployment!"

# Configurar rama principal
echo "🌟 Configurando rama principal..."
git branch -M main

echo ""
echo "✅ Repositorio configurado localmente!"
echo ""
echo "📋 Próximos pasos:"
echo "1. Crear repositorio en GitHub: https://github.com/new"
echo "2. Ejecutar: git remote add origin https://github.com/TU_USUARIO/NOMBRE_REPO.git"
echo "3. Ejecutar: git push -u origin main"
echo "4. Seguir DEPLOY_GUIDE.md para despliegue en Render.com"
echo ""
echo "🤖 ¡Tu bot estará funcionando 24/7 en pocos minutos!"
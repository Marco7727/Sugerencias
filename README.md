# Discord Suggestions Bot 🤖

Bot de Discord en español para gestionar sugerencias con sistema de votación mediante botones integrados.

## 🌟 Características

- ✅ Comandos slash en español
- 💡 Sistema de sugerencias con embeds personalizados
- 🗳️ Votación mediante botones integrados (✅ y ❌)
- 📊 Contador de votos en tiempo real
- ⚙️ Configuración de canal específico para sugerencias
- 🔒 Permisos de administrador para configuración
- 📝 Logs detallados para debugging

## 🚀 Instalación

### Requisitos

- Python 3.8 o superior
- discord.py

### Configuración

1. **Crear un bot en Discord Developer Portal:**
   - Ve a https://discord.com/developers/applications
   - Crea una nueva aplicación
   - Ve a la sección "Bot" y crea un bot
   - Copia el token del bot

2. **Configurar variables de entorno:**
   ```bash
   export DISCORD_BOT_TOKEN="tu_token_aqui"
   ```

3. **Invitar el bot a tu servidor:**
   - Ve a la sección "OAuth2" > "URL Generator"
   - Selecciona los scopes: `bot` y `applications.commands`
   - Permisos necesarios:
     - Send Messages
     - Use Slash Commands
     - Add Reactions
     - Read Message History
     - Embed Links

4. **Ejecutar el bot:**
   ```bash
   python main.py
   ```

## 🌐 Despliegue 24/7

### Render.com (Recomendado)

Para mantener tu bot funcionando 24/7 de forma gratuita:

1. **Subir a GitHub:**
   - Crear repositorio en GitHub
   - Subir todos los archivos del proyecto

2. **Configurar en Render.com:**
   - Crear cuenta en [render.com](https://render.com)
   - Conectar repositorio de GitHub
   - Configurar como "Worker"
   - Añadir variable `DISCORD_BOT_TOKEN`

3. **Archivos incluidos para deploy:**
   - `render_requirements.txt` - Dependencias
   - `Procfile` - Comando de inicio
   - `render.yaml` - Configuración de Render
   - `.gitignore` - Archivos a ignorar

Ver **[DEPLOY_GUIDE.md](DEPLOY_GUIDE.md)** para instrucciones detalladas paso a paso.

### Beneficios:
- ✅ **24/7 uptime** gratuito
- ✅ Auto-restart en caso de errores
- ✅ Logs centralizados
- ✅ Integración con GitHub

## 📋 Comandos

### `/sugerir <sugerencia>`
Envía una nueva sugerencia al canal configurado.
- **Parámetro:** `sugerencia` - Tu sugerencia (máximo 1000 caracteres)
- **Uso:** `/sugerir Añadir más eventos al servidor`

### `/config_canal <canal>`
Configura el canal donde se enviarán las sugerencias.
- **Permisos:** Solo administradores
- **Parámetro:** `canal` - Canal de texto donde aparecerán las sugerencias
- **Uso:** `/config_canal #sugerencias`

### `/ayuda`
Muestra la ayuda del bot con todos los comandos disponibles.

## 🗳️ Sistema de Votación

- ✅ **Aprobar:** Haz clic en la reacción verde para aprobar la sugerencia
- ❌ **Rechazar:** Haz clic en la reacción roja para rechazar la sugerencia
- 📊 **Conteo automático:** Los votos se actualizan en tiempo real

## 📁 Estructura del Proyecto


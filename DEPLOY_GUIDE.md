# 📋 Guía de Despliegue - Discord Sugerencias Bot

## 🚀 Despliegue en Render.com (24/7)

### Paso 1: Preparar GitHub Repository

1. **Crear repositorio en GitHub:**
   - Ve a [github.com](https://github.com) y crea un nuevo repositorio
   - Nombre sugerido: `discord-suggestions-bot`
   - Hazlo público o privado según prefieras

2. **Subir código a GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit - Discord Suggestions Bot"
   git branch -M main
   git remote add origin https://github.com/TU_USUARIO/discord-suggestions-bot.git
   git push -u origin main
   ```

### Paso 2: Configurar Render.com

1. **Crear cuenta en Render.com:**
   - Ve a [render.com](https://render.com)
   - Regístrate con tu cuenta de GitHub

2. **Conectar repositorio:**
   - Click en "New +" → "Web Service"
   - Conecta tu repositorio de GitHub
   - Selecciona el repositorio del bot

3. **Configurar el servicio:**
   - **Type:** `Web Service` (no Worker)
   - **Name:** `discord-suggestions-bot`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r render_requirements.txt`
   - **Start Command:** `python main.py`

4. **Configurar variables de entorno:**
   - En la sección "Environment Variables"
   - Añadir: `DISCORD_BOT_TOKEN` con el token de tu bot
   - **IMPORTANTE:** No compartas este token públicamente

### Paso 3: Deploy y Verificación

1. **Iniciar deploy:**
   - Click en "Create Worker"
   - Render automáticamente construirá y desplegará el bot

2. **Verificar logs:**
   - Ve a la pestaña "Logs"
   - Deberías ver: "🤖 Sugerencias#XXXX está conectado y listo!"

### Paso 4: UptimeRobot (Monitoreo 24/7)

1. **Crear cuenta en UptimeRobot:**
   - Ve a [uptimerobot.com](https://uptimerobot.com)
   - Crea una cuenta gratuita

2. **Configurar monitor HTTP:**
   - **Monitor Type:** HTTP(s)
   - **URL:** `https://tu-app.onrender.com/health`
   - **Monitoring Interval:** 5 minutos
   - **Monitor Timeout:** 30 segundos
   - **Monitor Name:** Discord Bot Health Check

3. **Configurar alertas:**
   - Email notifications cuando el bot esté down
   - Opcional: Webhook notifications a Discord

4. **Endpoint de salud incluido:**
   - El bot ahora incluye un servidor web en `/health`
   - Responde con JSON status del bot
   - UptimeRobot puede monitorear este endpoint

## 📁 Archivos Importantes para el Deploy

- `render_requirements.txt` - Dependencias de Python
- `Procfile` - Comando de inicio (para compatibilidad)
- `runtime.txt` - Versión de Python
- `render.yaml` - Configuración específica de Render
- `.gitignore` - Archivos a ignorar en Git

## 🔧 Solución de Problemas

### Bot no se conecta:
- Verifica que `DISCORD_BOT_TOKEN` esté configurado correctamente
- Revisa los logs en Render para errores específicos

### Comandos no funcionan:
- Asegúrate de que el bot tenga permisos en Discord
- Verifica que los comandos slash estén sincronizados

### Problemas de memoria:
- Render ofrece 512MB gratis, suficiente para este bot
- Si necesitas más, considera un plan pago

## 💡 Beneficios del Deploy en Render

- ✅ **24/7 uptime** - Tu bot estará siempre disponible
- ✅ **Auto-restart** - Se reinicia automáticamente si hay errores
- ✅ **Logs centralizados** - Fácil monitoreo y debugging
- ✅ **Integración con GitHub** - Auto-deploy con cada push
- ✅ **Plan gratuito** - 750 horas gratis por mes

## 🔄 Actualizaciones Futuras

Para actualizar el bot:
1. Haz cambios en tu código local
2. Commit y push a GitHub
3. Render automáticamente desplegará la nueva versión

¡Tu bot estará funcionando 24/7 sin interrupciones! 🎉
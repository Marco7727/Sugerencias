import os
import asyncio
import logging
from discord.ext import commands
import discord
from bot.suggestions import SuggestionsBot, setup_commands

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

async def main():
    """Función principal para iniciar el bot"""
    
    # Obtener token del bot desde variables de entorno
    bot_token = os.getenv('DISCORD_BOT_TOKEN')
    
    if not bot_token:
        logger.error("❌ Error: No se encontró el token del bot en las variables de entorno.")
        logger.error("Por favor, configura la variable DISCORD_BOT_TOKEN")
        return
    
    # Configurar intents del bot
    intents = discord.Intents.default()
    intents.message_content = False  # No necesario para slash commands
    intents.reactions = True
    intents.guilds = True
    
    # Crear instancia del bot
    bot = SuggestionsBot(
        command_prefix='!',
        intents=intents,
        help_command=None
    )
    
    # Configurar comandos slash
    setup_commands(bot)
    
    try:
        logger.info("🚀 Iniciando bot de sugerencias...")
        await bot.start(bot_token)
    except discord.LoginFailure:
        logger.error("❌ Error: Token del bot inválido")
    except Exception as e:
        logger.error(f"❌ Error inesperado: {e}")
    finally:
        await bot.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("⏹️ Bot detenido por el usuario")
    except Exception as e:
        logger.error(f"❌ Error fatal: {e}")

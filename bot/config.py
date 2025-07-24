"""
Configuración del bot de sugerencias
"""

# Colores para embeds
COLORS = {
    'success': 0x00ff00,  # Verde
    'error': 0xff0000,    # Rojo
    'info': 0x0099ff,     # Azul
    'warning': 0xffaa00,  # Naranja
    'suggestion': 0x7289da # Azul Discord
}

# Emojis para las reacciones
REACTIONS = {
    'approve': '✅',
    'reject': '❌'
}

# Mensajes del bot
MESSAGES = {
    'suggestion_submitted': '✅ **Tu sugerencia ha sido enviada correctamente**',
    'suggestion_title': '💡 Nueva Sugerencia',
    'votes_label': 'Votos:',
    'submitter_label': 'Enviado por:',
    'channel_not_configured': '⚠️ **Canal de sugerencias no configurado**\nUn administrador debe usar `/config_canal` primero.',
    'channel_configured': '✅ **Canal de sugerencias configurado correctamente**\nLas sugerencias se enviarán a {channel}',
    'no_permission': '❌ **No tienes permisos para usar este comando**\nSolo los administradores pueden configurar el canal.',
    'error_sending': '❌ **Error al enviar la sugerencia**\nInténtalo de nuevo más tarde.',
    'suggestion_too_long': '❌ **La sugerencia es demasiado larga**\nMáximo 1000 caracteres permitidos.',
    'suggestion_empty': '❌ **La sugerencia no puede estar vacía**\nPor favor, escribe tu sugerencia.',
    'bot_ready': '🤖 **Bot de sugerencias iniciado correctamente**',
    'help_title': '📋 **Comandos del Bot de Sugerencias**',
    'help_description': 'Lista de comandos disponibles:'
}

# Configuración de embed
EMBED_CONFIG = {
    'footer_text': 'Sistema de Sugerencias',
    'thumbnail_url': None,  # Se puede agregar una URL de imagen aquí
    'max_suggestion_length': 1000
}

# Configuración de la base de datos (simple archivo de texto)
DATABASE_FILE = 'suggestions_config.txt'

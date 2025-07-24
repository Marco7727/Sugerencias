import discord
from discord.ext import commands
from discord import app_commands
import json
import os
import logging
from datetime import datetime
from typing import Optional
from .config import COLORS, REACTIONS, MESSAGES, EMBED_CONFIG, DATABASE_FILE

logger = logging.getLogger(__name__)

class SuggestionVoteView(discord.ui.View):
    """Vista con botones para votar en sugerencias"""
    
    def __init__(self, suggestion_id: str):
        super().__init__(timeout=None)  # Sin timeout para que los botones permanezcan
        self.suggestion_id = suggestion_id
        self.votes = {"approve": set(), "reject": set()}  # Almacenar votos por usuario
    
    @discord.ui.button(label="0", style=discord.ButtonStyle.success, emoji="✅", custom_id="vote_approve")
    async def vote_approve(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_id = interaction.user.id
        
        # Remover de reject si existe
        self.votes["reject"].discard(user_id)
        
        # Toggle en approve
        if user_id in self.votes["approve"]:
            self.votes["approve"].remove(user_id)
        else:
            self.votes["approve"].add(user_id)
        
        await self.update_buttons_and_embed(interaction)
    
    @discord.ui.button(label="0", style=discord.ButtonStyle.danger, emoji="❌", custom_id="vote_reject")
    async def vote_reject(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_id = interaction.user.id
        
        # Remover de approve si existe
        self.votes["approve"].discard(user_id)
        
        # Toggle en reject
        if user_id in self.votes["reject"]:
            self.votes["reject"].remove(user_id)
        else:
            self.votes["reject"].add(user_id)
        
        await self.update_buttons_and_embed(interaction)
    
    async def update_buttons_and_embed(self, interaction: discord.Interaction):
        """Actualiza los botones y el embed con los nuevos votos"""
        approve_count = len(self.votes["approve"])
        reject_count = len(self.votes["reject"])
        
        # Actualizar etiquetas de botones
        self.children[0].label = str(approve_count)  # Botón de aprobar
        self.children[1].label = str(reject_count)   # Botón de rechazar
        
        # Actualizar embed
        embed = interaction.message.embeds[0]
        new_embed = discord.Embed(
            title=embed.title,
            description=embed.description,
            color=embed.color
        )
        
        # Restaurar campos originales excepto resultados
        for field in embed.fields:
            if "Resultados" not in field.name:
                new_embed.add_field(
                    name=field.name,
                    value=field.value,
                    inline=field.inline
                )
        
        # Añadir resultados actualizados
        votes_text = f"✅: {approve_count}\n❌: {reject_count}"
        new_embed.add_field(
            name="📊 Resultados",
            value=votes_text,
            inline=False
        )
        
        new_embed.set_footer(text=embed.footer.text if embed.footer else EMBED_CONFIG['footer_text'])
        new_embed.timestamp = embed.timestamp
        
        await interaction.response.edit_message(embed=new_embed, view=self)

class SuggestionsBot(commands.Bot):
    """Bot principal para gestión de sugerencias"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.suggestions_channels = {}  # guild_id: channel_id
        self.load_config()
    
    async def setup_hook(self):
        """Configuración inicial del bot"""
        try:
            # Sincronizar comandos slash globalmente
            synced = await self.tree.sync()
            logger.info(f"✅ Sincronizados {len(synced)} comandos slash globalmente")
        except Exception as e:
            logger.error(f"❌ Error sincronizando comandos: {e}")
    
    async def on_ready(self):
        """Evento cuando el bot está listo"""
        logger.info(f"🤖 {self.user} está conectado y listo!")
        logger.info(f"📊 Conectado a {len(self.guilds)} servidor(es)")
        
        # Cambiar estado del bot
        activity = discord.Activity(
            type=discord.ActivityType.watching, 
            name="sugerencias | /sugerir"
        )
        await self.change_presence(activity=activity)
    

    
    def load_config(self):
        """Carga la configuración desde archivo"""
        try:
            if os.path.exists(DATABASE_FILE):
                with open(DATABASE_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.suggestions_channels = data.get('channels', {})
                    logger.info(f"✅ Configuración cargada: {len(self.suggestions_channels)} canales configurados")
        except Exception as e:
            logger.error(f"❌ Error cargando configuración: {e}")
            self.suggestions_channels = {}
    
    def save_config(self):
        """Guarda la configuración en archivo"""
        try:
            data = {
                'channels': self.suggestions_channels,
                'last_updated': datetime.now().isoformat()
            }
            with open(DATABASE_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logger.info("✅ Configuración guardada correctamente")
        except Exception as e:
            logger.error(f"❌ Error guardando configuración: {e}")

# Comandos slash fuera de la clase
@app_commands.command(name="sugerir", description="Envía una nueva sugerencia")
@app_commands.describe(sugerencia="Tu sugerencia para el servidor")
async def suggest(interaction: discord.Interaction, sugerencia: str):
    """Comando para enviar sugerencias"""
    bot = interaction.client
    try:
        # Validar entrada
        if not sugerencia or sugerencia.strip() == "":
            await interaction.response.send_message(
                MESSAGES['suggestion_empty'], 
                ephemeral=True
            )
            return
        
        if len(sugerencia) > EMBED_CONFIG['max_suggestion_length']:
            await interaction.response.send_message(
                MESSAGES['suggestion_too_long'], 
                ephemeral=True
            )
            return
        
        # Verificar si hay canal configurado
        if not interaction.guild:
            await interaction.response.send_message(
                "❌ **Error:** Este comando solo puede usarse en un servidor.",
                ephemeral=True
            )
            return
            
        guild_id = str(interaction.guild.id)
        if guild_id not in bot.suggestions_channels:
            await interaction.response.send_message(
                MESSAGES['channel_not_configured'], 
                ephemeral=True
            )
            return
        
        # Obtener canal de sugerencias
        channel_id = bot.suggestions_channels[guild_id]
        channel = interaction.guild.get_channel(int(channel_id))
        
        if not channel or not isinstance(channel, discord.TextChannel):
            await interaction.response.send_message(
                "❌ **Canal de sugerencias no encontrado**\nContacta con un administrador.", 
                ephemeral=True
            )
            return
        
        # Crear embed de sugerencia
        embed = discord.Embed(
            title="💡 Nueva Sugerencia",
            description=sugerencia,
            color=COLORS['suggestion']
        )
        
        embed.add_field(
            name=f"👤 {MESSAGES['submitter_label']}",
            value=interaction.user.mention,
            inline=True
        )
        
        # Formato inicial de votos
        votes_text = f"✅: 0\n❌: 0"
        
        embed.add_field(
            name="📊 Resultados",
            value=votes_text,
            inline=False
        )
        

        
        embed.set_footer(text=EMBED_CONFIG['footer_text'])
        embed.timestamp = datetime.now()
        
        # Crear vista con botones
        view = SuggestionVoteView(suggestion_id=str(interaction.guild.id) + "_" + str(datetime.now().timestamp()))
        
        # Enviar sugerencia con botones
        suggestion_message = await channel.send(embed=embed, view=view)
        
        # Confirmar al usuario
        await interaction.response.send_message(
            MESSAGES['suggestion_submitted'], 
            ephemeral=True
        )
        
        logger.info(f"✅ Sugerencia enviada por {interaction.user} en {interaction.guild.name if interaction.guild else 'servidor desconocido'}")
        
    except Exception as e:
        logger.error(f"❌ Error procesando sugerencia: {e}")
        await interaction.response.send_message(
            MESSAGES['error_sending'], 
            ephemeral=True
        )

@app_commands.command(name="config_canal", description="Configura el canal para sugerencias (Solo administradores)")
@app_commands.describe(canal="Canal donde se enviarán las sugerencias")
async def config_channel(interaction: discord.Interaction, canal: discord.TextChannel):
    """Comando para configurar el canal de sugerencias"""
    bot = interaction.client
    try:
        # Verificar que estamos en un servidor y que el usuario es miembro
        if not interaction.guild or not isinstance(interaction.user, discord.Member):
            await interaction.response.send_message(
                "❌ **Error:** Este comando solo puede usarse en un servidor.",
                ephemeral=True
            )
            return
            
        # Verificar permisos
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                MESSAGES['no_permission'], 
                ephemeral=True
            )
            return
        
        # Guardar configuración
        guild_id = str(interaction.guild.id)
        bot.suggestions_channels[guild_id] = str(canal.id)
        bot.save_config()
        
        # Confirmar configuración
        await interaction.response.send_message(
            MESSAGES['channel_configured'].format(channel=canal.mention),
            ephemeral=True
        )
        
        logger.info(f"✅ Canal configurado en {interaction.guild.name if interaction.guild else 'servidor desconocido'}: #{canal.name}")
    
    except Exception as e:
        logger.error(f"❌ Error configurando canal: {e}")
        await interaction.response.send_message(
            "❌ **Error al configurar el canal**\nInténtalo de nuevo.", 
            ephemeral=True
        )

@app_commands.command(name="ayuda", description="Muestra la ayuda del bot")
async def help_bot(interaction: discord.Interaction):
    """Comando de ayuda"""
    embed = discord.Embed(
        title=MESSAGES['help_title'],
        description=MESSAGES['help_description'],
        color=COLORS['info']
    )
    
    embed.add_field(
        name="/sugerir <sugerencia>",
        value="Envía una nueva sugerencia al canal configurado",
        inline=False
    )
    
    embed.add_field(
        name="/config_canal <canal>",
        value="Configura el canal para sugerencias (Solo administradores)",
        inline=False
    )
    
    embed.add_field(
        name="/ayuda",
        value="Muestra esta ayuda",
        inline=False
    )
    
    embed.add_field(
        name="🗳️ Votación",
        value=f"Usa {REACTIONS['approve']} para aprobar y {REACTIONS['reject']} para rechazar sugerencias",
        inline=False
    )
    
    embed.set_footer(text=EMBED_CONFIG['footer_text'])
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

# Agregar comandos al bot
def setup_commands(bot):
    """Configura los comandos del bot"""
    bot.tree.add_command(suggest)
    bot.tree.add_command(config_channel)
    bot.tree.add_command(help_bot)
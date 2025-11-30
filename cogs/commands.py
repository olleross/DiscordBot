import discord
from discord import app_commands
from discord.ext import commands
from utils import make_embed, load_config, save_config

# Load configuration
config = load_config()

# Custom check for role-based permissions
def role_check(role_id):
    async def predicate(interaction: discord.Interaction):
        # Check if the user has the required role
        if not any(role.id == role_id for role in interaction.user.roles):
            await interaction.response.send_message(
                "You lack the required role to use this command.",
                ephemeral=True
            )
            return False
        return True
    return app_commands.check(predicate)

class CommandsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # /announcement command
    @app_commands.command(name="announcement", description="Send an announcement.")
    @role_check(1442918548451098808)
    async def announcement(self, interaction: discord.Interaction, message: str, ping: str = "@everyone", channel: discord.TextChannel = None):
        announcement_embed = make_embed("announcement_embed", {"message": message, "ping": ping})
        target_channel = channel or interaction.channel
        await target_channel.send(content=ping, embed=announcement_embed)
        await interaction.response.send_message("Announcement sent!", ephemeral=True)

    # /setup_embed command
    @app_commands.command(name="setup_embed", description="Edit embed templates.")
    @role_check(1442918548451098808)
    async def setup_embed(self, interaction: discord.Interaction, embed: str, field: str, value: str):
        if embed not in config:
            await interaction.response.send_message(f"No embed template found for: {embed}.", ephemeral=True)
            return
        config[embed][field] = value
        save_config(config)
        await interaction.response.send_message(f"Updated {embed}: {field} set to {value}.", ephemeral=True)

    # /refresh command
    @app_commands.command(name="refresh", description="Reload all cogs and config.")
    @role_check(1442918548451098808)
    async def refresh(self, interaction: discord.Interaction):
        self.bot.reload_extension("cogs.commands")
        self.bot.reload_extension("cogs.events")
        global config
        config = load_config()
        await interaction.response.send_message("Bot configuration and cogs refreshed.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(CommandsCog(bot))
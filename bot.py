import discord
from discord.ext import commands
from discord import Intents
import asyncio
from utils import load_config

# Intents
intents = Intents.default()
intents.members = True

# Load configuration
config = load_config()

# Bot setup
bot = commands.Bot(command_prefix="!", intents=intents)

# Load cogs
async def load_cogs():
    await bot.load_extension("cogs.commands")
    await bot.load_extension("cogs.events")

@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}!")

async def main():
    await load_cogs()
    await bot.start("YOUR_BOT_TOKEN")

asyncio.run(main())
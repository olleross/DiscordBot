import discord
from discord.ext import commands

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        embed = discord.Embed(title="Member Joined", description=f"{member.mention} has joined the server!", color=0x00ff00)
        channel = discord.utils.get(member.guild.text_channels, name="general")
        if channel:
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        embed = discord.Embed(title="Member Left", description=f"{member.mention} has left the server.", color=0xff0000)
        channel = discord.utils.get(member.guild.text_channels, name="general")
        if channel:
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.premium_since is None and after.premium_since is not None:
            embed = discord.Embed(title="Server Boosted!", description=f"{after.mention} just boosted the server! 🎉", color=0xFFD700)
            channel = discord.utils.get(after.guild.text_channels, name="general")
            if channel:
                await channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Events(bot))
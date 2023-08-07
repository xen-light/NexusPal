import platform
import discord
import psutil
import datetime
from discord.ext import commands

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = datetime.datetime.utcnow()

    # Command: Ping
    @commands.command(description="Will show the server info, bot info and latency + runtime.")
    async def ping(self, ctx):
        latency = round(self.bot.latency * 1000)
        os_info = f'{platform.system()} {platform.release()} ({platform.architecture()[0]})'
        # Server information
        server = ctx.guild
        total_members = server.member_count
        online_members = sum(1 for member in server.members if member.status == discord.Status.online and not member.bot)
        offline_members = total_members - online_members
        bot_count = sum(member.bot for member in server.members)
        
        # Bot information
        bot_name = self.bot.user.name
        bot_id = self.bot.user.id
        bot_uptime = datetime.datetime.utcnow() - self.start_time
        cpu_usage = psutil.cpu_percent()
        memory_usage = psutil.virtual_memory().percent
        
        # Create an embed
        embed = discord.Embed(title='🏓 Pong!', color=discord.Color.green())
        embed.add_field(name='Latency', value=f'{latency}ms', inline=False)
        embed.add_field(name='Operating System', value=os_info, inline=False)
        embed.add_field(name='Server Info', value=f'Server: {server.name}\nOnline Members: {online_members}\nOffline Members: {offline_members}\nTotal Members: {total_members}\nBots: {bot_count}', inline=False)
        embed.add_field(name='Bot Info', value=f'Name: {bot_name}\nID: {bot_id}\nUptime: {bot_uptime}', inline=False)
        embed.add_field(name='System Resources', value=f'CPU Usage: {cpu_usage}%\nMemory Usage: {memory_usage}%', inline=False)
        embed.set_footer(text=f'Requested by {ctx.author}')

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Ping(bot))
      
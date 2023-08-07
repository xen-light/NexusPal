import discord
from discord.ext import commands

class AboutBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="aboutbot", aliases=["info", "botinfo"], description="Everything about the bot.")
    async def about_bot(self, ctx):
        embed = discord.Embed(title=f"{self.bot.user.name} Information", color=discord.Color.blurple())
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        embed.add_field(name="Main Developer 👨‍💻", value="@xenwashere01", inline=False)
        embed.add_field(name="Support Server 🛠️", value="https://dsc.gg/nexuspal", inline=False)
        embed.add_field(name="Developer Website 🌐", value="https://xenlight.xyz/", inline=False)
        embed.add_field(name="Bot GitHub Page 🐙", value="https://github.com/xen-light/NexusPal", inline=False)
        embed.add_field(name="Invite the Bot 🤖", value="[Invite](https://discord.com/api/oauth2/authorize?client_id=1126221209407860926&permissions=1099645971574&scope=bot)", inline=False)

        await ctx.send(embed=embed)

async def setup(bot):
   await bot.add_cog(AboutBot(bot))
   
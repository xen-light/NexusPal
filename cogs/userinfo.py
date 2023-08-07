import discord
from discord.ext import commands

class UserinfoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Gives info about the tagged user or you if tagged no one.")
    async def userinfo(self, ctx, user: discord.User = None):
        user = user or ctx.author
        embed = discord.Embed(title=f"User Info - {user.name}", color=discord.Color.blue())

        if user.avatar.url:
            embed.set_thumbnail(url=user.avatar.url)
        else:
            embed.set_thumbnail(url=user.default.avatar.url)
        
        if user.bot:
            embed.add_field(name="🤖 Username", value=user.name, inline=True)
        else:
            embed.add_field(name="👤 Display name", value=user.display_name, inline=True)

        embed.add_field(name="🔢 Discriminator", value=user.discriminator, inline=True)
        embed.add_field(name="🆔 ID", value=user.id, inline=False)
        embed.add_field(name="📅 Created At", value=user.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)
        await ctx.send(embed=embed)

async def setup(bot):
   await bot.add_cog(UserinfoCog(bot))

import discord
from discord.ext import commands

class LockUnlock(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Lock the channel for everyone. You need **Manage Channels** permission.")
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        await channel.send(embed=self.lock_embed(channel))
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = False
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)

    @commands.command(description="Unlock the channel for everyone. You need **Manage Channels** permission.")
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = None
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await channel.send(embed=self.unlock_embed(channel))

    def lock_embed(self, channel):
        embed = discord.Embed(
            title="🔒 Channel Locked",
            description=f"The channel {channel.mention} has been locked.",
            color=discord.Color.red()
        )
        return embed

    def unlock_embed(self, channel):
        embed = discord.Embed(
            title="🔓 Channel Unlocked",
            description=f"The channel {channel.mention} has been unlocked.",
            color=discord.Color.green()
        )
        return embed

async def setup(bot):
   await bot.add_cog(LockUnlock(bot))
      
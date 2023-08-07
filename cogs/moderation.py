import discord
from discord.ext import commands
from datetime import timedelta

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def send_reason_dm(self, member, action, reason):
        try:
            dm_message = f"**Moderation Notice**\nYou have been {action} from {member.guild.name} for the following reason:\n```\n{reason}\n```"
            await member.send(dm_message)
        except discord.Forbidden:
            pass

    @commands.command(description="Kick others, you need **Kick Members** permission.")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="No reason provided."):
        author = ctx.author
        if member.top_role >= author.top_role:
            return await ctx.send("You can't moderate a user with higher or equal role than yours. :x:")
        await self.send_reason_dm(member, "kicked", reason)
        await member.kick(reason=reason)
        embed = discord.Embed(title=":boot: Kicked", description=f"{member.mention} has been kicked from the server.", color=discord.Color.gold())
        embed.add_field(name="Reason", value=reason, inline=False)
        await ctx.send(embed=embed)

    @commands.command(description="Ban others, you need **Ban Members** to use this .")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason="No reason provided."):
        author = ctx.author
        if member.top_role >= author.top_role:
            return await ctx.send("You can't moderate a user with higher or equal role than yours. :x:")
        await self.send_reason_dm(member, "banned", reason)
        await member.ban(reason=reason)
        embed = discord.Embed(title=":hammer: Banned", description=f"{member.mention} has been banned from the server.", color=discord.Color.red())
        embed.add_field(name="Reason", value=reason, inline=False)
        await ctx.send(embed=embed)

    @commands.command(description="Unban users by using USER ID. <@userid>. You need **Ban Members** permission to do this.")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user: discord.User):
                await ctx.guild.unban(user)
                embed = discord.Embed(title=":unlock: Unbanned", description=f"{user} has been unbanned.", color=discord.Color.green())
                await ctx.send(embed=embed)
                return

                embed = discord.Embed(title=":x: User Not Found", description="User not found in the ban list.", color=discord.Color.red())
                await ctx.send(embed=embed)

    @commands.command(description="Timeout users which will result in muting. You need to have **Manage Messages** permission to use this. Usage !timeout @target 10s/m/h reason.")
    @commands.has_permissions(manage_messages=True)
    async def timeout(self, ctx, member: discord.Member, duration: str, *, reason="No reason provided."):
        author = ctx.author
        if member.top_role >= author.top_role:
            return await ctx.send("You can't moderate a user with higher or equal role than yours. :x:")
        try:
            duration_value = int(duration)
            duration_msg = f"for {duration_value} seconds"
            duration_time = timedelta(seconds=duration_value)
        except ValueError:
            duration_value, duration_unit = int(duration[:-1]), duration[-1].lower()
            if duration_unit == 's':
                duration_msg = f"for {duration_value} seconds"
                duration_time = timedelta(seconds=duration_value)
            elif duration_unit == 'm':
                duration_msg = f"for {duration_value} minutes"
                duration_time = timedelta(minutes=duration_value)
            elif duration_unit == 'h':
                duration_msg = f"for {duration_value} hours"
                duration_time = timedelta(hours=duration_value)
            else:
                embed = discord.Embed(title=":x: Invalid Timeout Format", description="Use 's' for seconds, 'm' for minutes, or 'h' for hours.", color=discord.Color.red())
                await ctx.send(embed=embed)
                return

        await member.timeout(duration_time, reason=reason)
        await self.send_reason_dm(member, f"timed out {duration_msg}", reason)
        embed = discord.Embed(title=":clock1: Timed Out", description=f"{member.mention} has been timed out {duration_msg}.", color=discord.Color.orange())
        embed.add_field(name="Reason", value=reason, inline=False)
        await ctx.send(embed=embed)

async def setup(bot):
   await bot.add_cog(Moderation(bot))
      
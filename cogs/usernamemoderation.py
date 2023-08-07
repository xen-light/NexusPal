import discord
from discord.ext import commands
import random
import string

class UsernameModeration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Moderates the target user's users username.")
    @commands.has_permissions(manage_nicknames=True)
  
    async def moderate(self, ctx, member: discord.Member):
        author = ctx.author
        if member.top_role >= author.top_role:
            return await ctx.send("You can't moderate a user with higher or equal role than yours. :x:")

        # Generate a random string ID of 10 characters
        random_id = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

        try:
            # Change the member's nickname to the random ID
            await member.edit(nick=f"Moderated {random_id}")
            embed = discord.Embed(description=f"Successfully moderated {member.mention}'s username to 'Moderated {random_id}'. :white_check_mark:", color=discord.Color.green())
            await ctx.send(embed=embed)
        except discord.Forbidden:
            embed = discord.Embed(description="I don't have the necessary permissions to moderate this user's username. :no_entry:", color=discord.Color.red())
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(UsernameModeration(bot))

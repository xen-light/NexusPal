import discord
from discord.ext import commands
import asyncio
from datetime import timedelta

class Purge(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        description="Deletes a specified number of messages.",
        help="Deletes a specified number of messages. The maximum limit is 75.",
        examples="purge 100",
    )
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, limit: int):
        if limit > 75:
            await ctx.send("Limit is 75 messages max, purging 75 messages instead..", delete_after=5)
            limit = 75
        deleted = await ctx.channel.purge(limit=limit)
        embed = discord.Embed(
            title="Purged by {} :wastebasket:".format(ctx.author.name),
            description=f"Successfully purged {limit} messages. :white_check_mark:",
            color=discord.Color.red(),
            timestamp=ctx.message.created_at,
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Purge(bot))
      
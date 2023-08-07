import discord
from discord.ext import commands

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help", aliases=["h"])
    async def help_command(self, ctx, command_name: str = None):
        """Shows help for a command or all commands."""
        if command_name is None:
            # Show help for all commands
            embed = discord.Embed(title="Help", description="Here is a list of all commands:")
            for command in self.bot.commands:
                embed.add_field(name=command.name, value=command.description, inline=False)
            await ctx.send(embed=embed)
        else:
            # Show help for a specific command
            command = self.bot.get_command(command_name)
            if command is None:
                await ctx.send(f"Command `{command_name}` not found.")
            else:
                embed = discord.Embed(title=f"Help for `{command.name}`", description=command.description)
                embed.add_field(name="Usage", value=f"`{command.usage}`", inline=False)
                await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(HelpCog(bot))
  
import discord
from discord.ext import commands
import json

def get_prefix(bot, message):
    # Load custom prefixes from the JSON file
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    # Get the prefix for the current server or use the default prefix ('!')
    return prefixes.get(str(message.guild.id), '!')

bot = commands.Bot(command_prefix=get_prefix, intents=discord.Intents.all())

class Prefix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Change the prefix for your server. You need to have **manage guild** permission to use this.")
    @commands.has_permissions(manage_guild=True)
    async def setprefix(self, ctx, new_prefix):
        if len(new_prefix) > 10:
            return await ctx.send("The prefix can't be longer than 10 characters.")

        # Load custom prefixes from the JSON file
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)

        # Update the prefix for the current server
        prefixes[str(ctx.guild.id)] = new_prefix

        # Save the updated prefixes back to the JSON file
        with open('prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)

        # Update the bot's command prefix
        self.bot.command_prefix = get_prefix

        await ctx.send(f"Prefix updated to `{new_prefix}`.")

    async def on_guild_join(self, guild):
        # Add the default prefix '!' for the newly joined server
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)

        prefixes[str(guild.id)] = '!'

        with open('prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)

async def setup(bot):
   await bot.add_cog(Prefix(bot))
  
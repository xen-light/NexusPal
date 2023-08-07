import discord
from discord.ext import commands
import os
import asyncio
import traceback

# Function to handle errors
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
      embed = discord.Embed(title="Error :warning:", description="Invalid command! Try using the help command to see valid commands!", color=discord.Color.orange())
      await ctx.send(embed=embed)

    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title="Error :warning:", description="You need to provide all the required arguments for this command.", color=discord.Color.orange())
        await ctx.send(embed=embed)

    elif isinstance(error, commands.NoPrivateMessage):
        embed = discord.Embed(title="Error :no_entry:", description="This command cannot be used in private messages.", color=discord.Color.red())
        await ctx.send(embed=embed)

    elif isinstance(error, commands.DisabledCommand):
        embed = discord.Embed(title="Error :x:", description="This command is currently disabled and cannot be used.", color=discord.Color.red())
        await ctx.send(embed=embed)

    elif isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title="Error :hourglass_flowing_sand:", description=f"This command is on cooldown. Try again in {error.retry_after:.2f} seconds.", color=discord.Color.orange())
        await ctx.send(embed=embed)

    elif isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(title="Error :no_entry:", description="You don't have the necessary permissions to use this command.", color=discord.Color.red())
        await ctx.send(embed=embed)

    else:
        # Error handling for general errors
        error_message = ("Gah! Something went wrong, the developer of the bot has been informed about this. Sorry! Try again in a few hours! :warning:")
        embed = discord.Embed(title="Error :x:", description=error_message, color=discord.Color.red())
        await ctx.send(embed=embed)
      
        # Print the full error traceback
        traceback_msg = traceback.format_exception(type(error), error, error.__traceback__)
        traceback_text = "".join(traceback_msg)
        print(f"Error occurred in command '{ctx.command.qualified_name}':\n{traceback_text}")
      
                              

# Replace 'YOUR_TOKEN_HERE' with your actual bot token
BOT_TOKEN = 'token'

# Create the bot instance with the command prefix and all intents
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)
bot.on_command_error = on_command_error
bot.remove_command("help")
# Event: Bot is ready
@bot.event
async def on_ready():
    print('------------------------------------')
    print('Bot is online!')
    print(f'Logged in as: {bot.user.name} ({bot.user.id})')
    print('------------------------------------')
    print('Loaded Cogs:')
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            cog_name = filename[:-3]
            try:
                await asyncio.create_task(bot.load_extension(f'cogs.{cog_name}'))
                print(f'\t\u2713 {cog_name}')
            except Exception as e:
                traceback_str = traceback.format_exc(limit=1)
                print(f'\t\u274C {cog_name} [Error: {e}]')
                print(traceback_str)
    print('------------------------------------')

# Run the bot with the token
bot.run(BOT_TOKEN)

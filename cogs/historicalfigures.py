import discord
from discord.ext import commands
import requests

API_KEY = 'key'
API_URL = 'https://api.api-ninjas.com/v1/historicalfigures'

def truncate_text(text, max_length):
    if len(text) > max_length:
        text = text[:max_length - 3] + '...'
    return text

def format_attribute(attribute):
    # Remove underscores and capitalize the words
    return ' '.join(word.capitalize() for word in attribute.replace('_', ' ').split())

class HistoricalFigures(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="historicalfigure", aliases=["historical", "figure"], description="Shows info about a historical figure. Usage <prefix>historicalfigure Elizabeth II")
    async def historical_figure(self, ctx, *, name):
        headers = {'X-Api-Key': API_KEY}
        params = {'name': name}
        response = requests.get(API_URL, headers=headers, params=params)

        if response.status_code == requests.codes.ok:
            historical_data = response.json()
            if len(historical_data) > 0:
                figure = historical_data[0]

                # Extract historical figure data from the JSON response
                figure_name = figure.get('name', "N/A")
                figure_title = figure.get('title', "N/A")
                figure_info = figure.get('info', {})

                # Create the embed with historical figure information
                embed = discord.Embed(title=f"{figure_name} :scroll:", color=discord.Color.green())
                embed.set_author(name=figure_title)

                # Format each attribute and value and add them as embed fields
                for attribute, value in figure_info.items():
                    if value and isinstance(value, list):
                        value = ', '.join(value)
                    if value and len(value) <= 1024:
                        embed.add_field(name=f":small_orange_diamond: {format_attribute(attribute)}", value=truncate_text(value, 1024), inline=False)

                await ctx.send(embed=embed)
            else:
                await ctx.send(f"Sorry, I couldn't find information about the historical figure '{name}'. :x:")
        else:
            await ctx.send(f"An error occurred while fetching information for the historical figure '{name}'. :x:")

async def setup(bot):
    await bot.add_cog(HistoricalFigures(bot))
      

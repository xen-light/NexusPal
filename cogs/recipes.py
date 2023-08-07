import discord
from discord.ext import commands
import requests

API_KEY = 'key'
API_URL = 'https://api.api-ninjas.com/v1/recipe'

def format_ingredients(ingredients):
    formatted_ingredients = []
    for ingredient in ingredients.split('|'):
        formatted_ingredients.append(f":small_orange_diamond: {ingredient.strip()}")
    return '\n'.join(formatted_ingredients)[:1024]  # Truncate the ingredients to fit within the embed limit

def truncate_text(text):
    return text[:1024] if len(text) > 1024 else text

class Recipe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Shows a recipe. Usage <prefix>recipe Italian Wedding Soup")
    async def recipe(self, ctx, *, query):
        headers = {'X-Api-Key': API_KEY}
        params = {'query': query}
        response = requests.get(API_URL, headers=headers, params=params)

        if response.status_code == requests.codes.ok:
            recipes = response.json()
            if len(recipes) > 0:
                recipe = recipes[0]
                title = recipe.get('title', "N/A")
                ingredients = recipe.get('ingredients', "N/A")
                instructions = recipe.get('instructions', "N/A")
                servings = recipe.get('servings', "N/A")

                # Create the embed with recipe information
                embed = discord.Embed(title=f"{title} :cook:", description="Here's a delicious recipe for you! :yum:", color=discord.Color.green())
                try:
                    embed.add_field(name="Ingredients", value=format_ingredients(ingredients), inline=False)
                except discord.errors.HTTPException:
                    # Provide a link to a Google search for the recipe if the ingredient list is too long for the embed
                    embed.add_field(name="Ingredients", value=f"Too many ingredients to display, check the [recipe here](https://www.google.com/search?q={query.replace(' ', '+')}+recipe)", inline=False)

                parts = [instructions[i:i+1024] for i in range(0, len(instructions), 1024)]

                for idx, part in enumerate(parts, start=1):
                    embed.add_field(name=f"Instructions (Part {idx})", value=truncate_text(part), inline=False)

                embed.add_field(name="Servings", value=servings, inline=False)
                embed.set_footer(text="Bon Appétit!")

                await ctx.send(embed=embed)
            else:
                await ctx.send(f"Sorry, I couldn't find a recipe for '{query}'. :x:")
        else:
            await ctx.send(f"An error occurred while fetching the recipe for '{query}'. :x:")

async def setup(bot):
   await bot.add_cog(Recipe(bot))
  

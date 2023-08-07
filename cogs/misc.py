import discord
from discord.ext import commands
import requests
import asyncio
from datetime import datetime, timedelta

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Shows a cute cat picture.")
    async def cat(self, ctx):
        api_url = 'https://api.thecatapi.com/v1/images/search'
        response = requests.get(api_url)
        if response.status_code == requests.codes.ok:
            data = response.json()
            cat_url = data[0]['url']
            embed = discord.Embed(title="Meow! Here's a cute cat:", color=discord.Color.orange())
            embed.set_image(url=cat_url)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Sorry, I couldn't fetch a cat picture at the moment.")

    @commands.command(description="Shows a cute doggo picture.")
    async def dog(self, ctx):
        api_url = 'https://dog.ceo/api/breeds/image/random'
        response = requests.get(api_url)
        if response.status_code == requests.codes.ok:
            data = response.json()
            dog_url = data['message']
            embed = discord.Embed(title="Woof! Here's an adorable dog:", color=discord.Color.orange())
            embed.set_image(url=dog_url)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Sorry, I couldn't fetch a dog picture at the moment.")

async def setup(bot):
    await bot.add_cog(Misc(bot))
      
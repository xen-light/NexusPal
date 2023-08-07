import requests
import discord
from discord.ext import commands

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_url = 'https://api.api-ninjas.com/v1/facts?limit=1'
        self.headers = {'X-Api-Key': 'key'}

    @commands.command(description="Shows a random fact.")
    async def fact(self, ctx):
        response = requests.get(self.api_url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            fact = data[0]['fact']

            embed = discord.Embed(title="📚 Fun Fact!", description=fact, color=discord.Color.blue())
            embed.set_footer(text="Powered by API-Ninjas")
            await ctx.send(embed=embed)
        else:
            await ctx.send("Oops! Something went wrong. Try again later.")

async def setup(bot):
   await bot.add_cog(Fun(bot))
  

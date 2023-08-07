import discord
from discord.ext import commands
import requests

MEME_API_URL = 'https://meme-api.com/gimme'

class Meme(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='gimmememe', aliases=['meme'], description="Shows a meme from Reddit.")
    async def gimme_meme(self, ctx):
        response = requests.get(MEME_API_URL)

        if response.status_code == requests.codes.ok:
            meme_data = response.json()
            title = meme_data.get('title', "Untitled Meme")
            subreddit = meme_data.get('subreddit', "Unknown")
            image_url = meme_data.get('url', None)

            if image_url:
                embed = discord.Embed(title=title, url=meme_data['postLink'], color=discord.Color.random())
                embed.set_image(url=image_url)
                embed.set_footer(text=f"Posted on r/{subreddit} by {meme_data['author']} | Upvotes: {meme_data['ups']}")
                embed.set_author(name="Here's your random meme!", icon_url=self.bot.user.avatar.url)

                await ctx.send(embed=embed)
            else:
                await ctx.send("Oops! Something went wrong while fetching the meme. Try again later.")
        else:
            await ctx.send("Oops! Something went wrong while fetching the meme. Try again later.")

async def setup(bot):
    await bot.add_cog(Meme(bot))
      
import discord
import requests
from discord.ext import commands

class AutoFilter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.is_filter_on = False

    async def filter_message(self, message, content):
        await message.delete()
        censor_message = f'{message.author.mention}, your message has been censored! :no_entry:'
        censored_content = content.replace(message.content, f'**{message.content}**')
        censored_content = censored_content.replace('*', r'\*')  # Escape asterisks
        
        embed = discord.Embed(title='Auto-Filter', description=censored_content, color=discord.Color.red())
        embed.set_author(name=message.author.name)
        
        await message.channel.send(censor_message, embed=embed, delete_after=15)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if self.is_filter_on:
            url = "https://community-purgomalum.p.rapidapi.com/json"
            querystring = {"text": message.content}

            headers = {
                "X-RapidAPI-Key": "key",
                "X-RapidAPI-Host": "community-purgomalum.p.rapidapi.com"
            }

            response = requests.get(url, headers=headers, params=querystring)

            if response.ok:
                result = response.json().get('result')
                if result != message.content:
                    await self.filter_message(message, result)

    @commands.command(description="Automatically censors bad words. You need to have **Manage Messages** permission.")
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def autofilter(self, ctx, mode: str):
        mode = mode.lower()
        if mode == 'on':
            self.is_filter_on = True
            embed = discord.Embed(title='Auto-Filter :green_circle:', description='Auto-filter is now **ON**. Filtering messages with bad words. :eye_in_speech_bubble:', color=discord.Color.green())
        elif mode == 'off':
            self.is_filter_on = False
            embed = discord.Embed(title='Auto-Filter :red_circle:', description='Auto-filter is now **OFF**. Allowing all messages. :eyes:', color=discord.Color.red())
        else:
            await ctx.send('Invalid mode. Use `on` or `off`.')
            return

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(AutoFilter(bot))

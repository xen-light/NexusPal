import discord
from discord.ext import commands
import asyncio
from datetime import timedelta

class AntiSpam(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.antispam_enabled = False
        self.spam_threshold = 8  # Number of messages within the time period to be considered spam
        self.spam_time = 10  # Time period in seconds
        self.spam_tracker = {}

    async def spam_timer(self, user_id):
        await asyncio.sleep(self.spam_time)
        if user_id in self.spam_tracker:
            del self.spam_tracker[user_id]

    def is_spamming(self, user_id):
        if user_id in self.spam_tracker:
            return len(self.spam_tracker[user_id]) >= self.spam_threshold
        return False

    @commands.Cog.listener()
    async def on_message(self, message):
        if self.antispam_enabled and not message.author.bot:
            user_id = message.author.id
            if user_id not in self.spam_tracker:
                self.spam_tracker[user_id] = [message]
            else:
                self.spam_tracker[user_id].append(message)
                if self.is_spamming(user_id):
                    if not message.channel.permissions_for(message.author).manage_messages:
                        await message.delete()
                        reason = "Spamming multiple messages in a short period of time."
                        timeout_duration = timedelta(minutes=60)
                        embed = discord.Embed(title='Anti-Spam :shield:', description=f"{message.author.mention}, you have been timed out for 60 minutes due to spamming! :no_entry:", color=discord.Color.red())
                        embed.add_field(name='Reason:', value=reason, inline=False)
                        await message.channel.send(embed=embed)
                        await message.author.timeout(timeout_duration, reason=reason)
                        asyncio.create_task(self.spam_timer(user_id))

    @commands.command(description="Automatic spam protection, spammers will be timed for 1 hour, you need to have **Manage Messages**.")
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    async def antispam(self, ctx, mode: str):
        mode = mode.lower()
        if mode == 'on':
            self.antispam_enabled = True
            embed = discord.Embed(title='Anti-Spam :shield:', description='Anti-spam feature is now **ON**. Spamming will result in timeouts.', color=discord.Color.green())
        elif mode == 'off':
            self.antispam_enabled = False
            embed = discord.Embed(title='Anti-Spam :shield:', description='Anti-spam feature is now **OFF**. Spamming will not be monitored.', color=discord.Color.red())
        else:
            embed = discord.Embed(title='Invalid Mode', description='Please use `on` or `off` to toggle the Anti-Spam feature.', color=discord.Color.red())

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(AntiSpam(bot))
      
import discord
from discord.ext import commands, tasks
import asyncio
import datetime
import pytz
import re

def parse_time(time_string):
    time_string = time_string.lower()
    time_regex = re.match(r'^(\d+)([smhd])$', time_string)
    if not time_regex:
        raise ValueError("Invalid time format")
    
    time_unit = time_regex.group(2)
    time_value = int(time_regex.group(1))

    if time_unit == 's':
        return datetime.timedelta(seconds=time_value)
    elif time_unit == 'm':
        return datetime.timedelta(minutes=time_value)
    elif time_unit == 'h':
        return datetime.timedelta(hours=time_value)
    elif time_unit == 'd':
        return datetime.timedelta(days=time_value)
    else:
        raise ValueError("Invalid time unit")


class RemindMeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reminders = []
        self.check_reminders.start()

    @commands.command(name="remindme", description="Command for reminders. Usage <prefix>remindme 10s/m/d.")
    async def remindme(self, ctx, time_str, *, reminder):
        try:
            delta = parse_time(time_str)
        except ValueError as e:
            return await ctx.send(f"Error: {e}")

        future_time = datetime.datetime.utcnow() + delta
        self.reminders.append({
            'user_id': ctx.author.id,
            'timestamp': future_time.timestamp(),
            'reminder': reminder
        })
        await ctx.send(f"**🕒 I will remind you in {time_str} to: {reminder}**", delete_after=5)

    @tasks.loop(seconds=10)
    async def check_reminders(self):
        
        now = datetime.datetime.utcnow().timestamp()
        reminders_to_remove = []
        reminders_to_send = {}

        for reminder in self.reminders:
            if reminder['timestamp'] <= now:
                user_id = reminder['user_id']
                reminder_text = reminder['reminder']

                if user_id not in reminders_to_send:
                    reminders_to_send[user_id] = []
                reminders_to_send[user_id].append(reminder_text)
                reminders_to_remove.append(reminder)

        for reminder in reminders_to_remove:
            self.reminders.remove(reminder)

        for user_id, reminder_texts in reminders_to_send.items():
            user = self.bot.get_user(user_id)
            if user:
                reminders_str = "\n".join(reminder_texts)
                embed = discord.Embed(title="⏰ Reminders", description=reminders_str, color=0x00FF00)
                await user.send(embed=embed)

    @check_reminders.before_loop
    async def before_check_reminders(self):
        await self.bot.wait_until_ready()
        

async def setup(bot):
   await bot.add_cog(RemindMeCog(bot))
  
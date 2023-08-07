import discord
from discord.ext import commands
import requests

API_KEY = 'RqvQ0vVzqqlKgXCHVDa5iQ==ks9jSvGHeXt7pRT2'
API_URL = 'https://api.api-ninjas.com/v1/weather'

class Weather(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Shows the weather info about the specified city. Usage <prefix>weather London")
    async def weather(self, ctx, *, city):
        headers = {'X-Api-Key': API_KEY}
        params = {'city': city}
        response = requests.get(API_URL, headers=headers, params=params)

        if response.status_code == requests.codes.ok:
            weather_data = response.json()

            # Extract weather data from the JSON response
            wind_speed = weather_data['wind_speed']
            wind_degrees = weather_data['wind_degrees']
            temperature = weather_data['temp']
            humidity = weather_data['humidity']
            sunset = weather_data['sunset']
            min_temp = weather_data['min_temp']
            cloud_pct = weather_data['cloud_pct']
            feels_like = weather_data['feels_like']
            sunrise = weather_data['sunrise']
            max_temp = weather_data['max_temp']

            # Create the embed with weather information
            embed = discord.Embed(title=f"Weather in {city.capitalize()} :partly_sunny:", color=discord.Color.blue())
            embed.add_field(name="Temperature :thermometer:", value=f"{temperature}°C (Feels like {feels_like}°C)")
            embed.add_field(name="Humidity :droplet:", value=f"{humidity}%")
            embed.add_field(name="Wind :wind_blowing_face:", value=f"{wind_speed} km/h, {wind_degrees}°")
            embed.add_field(name="Cloud Cover :cloud:", value=f"{cloud_pct}%")
            embed.add_field(name="Sunrise :sunrise_over_mountains:", value=f"<t:{sunrise}:R>")
            embed.add_field(name="Sunset :city_sunset:", value=f"<t:{sunset}:R>")
            embed.add_field(name="Min Temperature :cold_face:", value=f"{min_temp}°C")
            embed.add_field(name="Max Temperature :fire:", value=f"{max_temp}°C")

            await ctx.send(embed=embed)
        else:
            await ctx.send(f"An error occurred while fetching the weather information for {city}. :x:")

async def setup(bot):
    await bot.add_cog(Weather(bot))

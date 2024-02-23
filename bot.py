import discord
from discord.ext import commands
import os

from css_server_wrapper import Server
import ip_utils

# Initialize the bot
TOKEN = os.getenv("TOKEN")
if TOKEN is None:
    print("set the TOKEN env variable")
    exit(1)
intents = discord.Intents.all()
intents.presences = True
intents.messages = True
bot = commands.Bot(command_prefix='!', intents=intents)

server = Server(ip_utils.get_local_ip())


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="Css"))


@bot.command(name="hello")
async def hello(ctx):
    await ctx.send("Hello there!")


@bot.command(name="changelevel")
async def changelevel(ctx, map):
    server.change_level_to(map)
    await ctx.send("chnaged")

bot.run(TOKEN)

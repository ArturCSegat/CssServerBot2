import discord
from discord.ext import commands
import os

from css_server_wrapper import Server
from ip_utils import get_local_ip

# ENV BOOZANZA
TOKEN = os.getenv("TOKEN")
if TOKEN is None:
    print("set the TOKEN env variable")
    exit(1)
PORT = os.getenv("PORT")
if PORT is None:
    PORT = 27015
PORT = int(PORT)
IP = os.getenv("IP")
if IP is None:
    IP = get_local_ip()
PATH = os.getenv("SRCDS_PATH")
if PATH is None:
    print(f"The SRCDS_PATH env variable is not set, tring to access existing server at {IP}:{PORT}")
    PATH = ""
PASSWD = os.getenv("RCON_PASSWD")
if PASSWD is None:
    print("must set the RCON_PASSWD env variable")
    exit(1)

intents = discord.Intents.all()
intents.presences = True
intents.messages = True
bot = commands.Bot(command_prefix='!', intents=intents)

server = Server(PATH, IP, PORT, PASSWD)
if not isinstance(server, Server):
    print(server.__str__())
    exit(1)


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

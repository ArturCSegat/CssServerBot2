import discord
from discord.ext import commands
import os
import asyncio

from css_server import CssServer
from ip_utils import get_local_ip
from scraper_wrapper import GameBananaScraper
import file_utils

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

server = CssServer(PATH, IP, PORT, PASSWD)
if not isinstance(server, CssServer):
    print(f"REAL ERROR: {server.__str__()}")
    exit(1)
scraper = GameBananaScraper()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="Counte Strike Source"))

@bot.command(name="changelevel")
async def changelevel(ctx, map):
    r = server.change_level_to(map)
    if r == "":
        r = "changed map"
    await ctx.send(r)

@bot.command(name="run")
async def run(ctx, cmd):
    real_cmd = ""
    for c in cmd:
        if c == '#':
            real_cmd += ' '
        else:
            real_cmd += c

    r = server.run(real_cmd)
    if r == "":
        r = "empty response"
    await ctx.send(r)

@bot.command(name="download_map")
async def download_map(ctx, map):
    await ctx.send("Procuando")
    if scraper.scrape(map) is False:
        await ctx.send("Faild to scrape map")
        return
    call = await ctx.send(f"is this the map you wnat? {scraper.last_map_url()}")
    await call.add_reaction("👍")
    await call.add_reaction("🔴")
    await ctx.send("conta até 5")
    await asyncio.sleep(5)

    res = await call.channel.fetch_message(call.id)

    sim = res.reactions[0].count
    nao = res.reactions[1].count

    if not (sim > nao and sim >= 2):
        await ctx.send("votação disse que não, cancelando")
        return

    scraper.save(f"{PATH}/cstrike/maps")
    r = server.change_level_to(scraper.last_map_name())
    if r == "":
        r = "changed map"
    await ctx.send(r)

@bot.command(name="download_map_link")
async def download_map_link(ctx, name, link):
    r = file_utils.save_map(f"{PATH}/cstrike/maps", name, link)
    if r is not None:
        await ctx.send(r.__str__())
        return
    await ctx.send("dinwaloaded")

bot.run(TOKEN)

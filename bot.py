import sys
from asyncio.locks import Event
import discord
from discord import message
from discord import client
from discord.enums import Status
from discord.ext import commands
import os
from ping3 import ping
import time
from discord.player import FFmpegAudio

intents = discord.Intents.default()
intents.presences = True
bot = commands.Bot(command_prefix='/', intents=intents)
path = "C:\\Users\\fishy\Pictures\\Cursed\\a Tam folder"


def Pinged(host):
    cheese = ping(host) * 1000
    # print(ping(host))
    time.sleep(1)
    hee = str(cheese)
    wee = hee[0] + hee[1] + hee[2] + hee[3] + hee[4] + hee[5] + 'ms'
    time.sleep(1)
    toReturn = str("Pinged " + host + ": " + wee)
    print(toReturn)
    return toReturn


def checkDir():
    if os.path.exists(path) == True:
        return True
    else:
        return False


@bot.command()
async def PingWifi(ctx, arg):
    await ctx.send(Pinged(arg))


@bot.command()
async def Help(ctx):
    file = open("help.md", "r")
    fileRead = str(file.read())
    await ctx.send(fileRead)


@bot.command()
async def WelcEmbed(ctx, arg):
    embed = discord.Embed(title="BeanBot", url="")
    pass


@bot.event
async def on_guild_join(guild):
    #print("change Text")
    # print(guild.text_channels)
    welc = open("BotJoin.md", "r")
    welc = str(welc.read())
    channel = bot.get_channel(839919450186711121)
    await channel.send(welc)

bot.run('Your Token Here')
bot.get_channel

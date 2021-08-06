import sys
from asyncio.locks import Event
import discord
from discord import message
from discord import client
from discord import embeds
from discord.enums import Status
from discord.ext import commands
import os
from ping3 import ping
import time
from discord.player import FFmpegAudio

intents = discord.Intents.default()
intents.presences = True
bot = commands.Bot(command_prefix='/', intents=intents)
TOKEN = 'Your Token Here'


def Pinged(host):
    cheese = ping(host) * 1000
    # print(ping(host))
    time.sleep(1)
    hee = str(cheese)
    wee = hee[0] + hee[1] + hee[2] + hee[3] + hee[4] + hee[5] + 'ms'
    time.sleep(1)
    toReturn = str("Pinged " + host + ": " + wee)
    print(toReturn)
    return wee


@bot.command()
async def PingWifi(ctx, arg):
    Embed = discord.Embed(title="Pinged", color=0xff0000)
    Embed.add_field(name=arg, value=Pinged(arg))
    await ctx.reply(embed=Embed)


@bot.command()
async def Help(ctx):
    file = open("help.md", "r")
    fileRead = str(file.read())
    Embed = discord.Embed(
        title="Help", description=fileRead, color=0x0400ff)
    Embed.set_footer(text="More Commands are coming soon")
    await ctx.reply(embed=Embed)


@bot.command()
async def AboutMe(ctx):
    welc = open("BotJoin.md", "r")
    welc = str(welc.read())
    Embed = discord.Embed(
        title="BeanBot version 0.2", url="https://github.com/BeanMan1408/BeanBot", description=welc, color=0xffffff)
    Embed.set_thumbnail(
        url="https://i.postimg.cc/zDH5KL3W/Bean-Bot-Transparent-Back.png")
    Embed.set_author(name="BeanMan", url="https://github.com/BeanMan1408/BeanBot-v0.1",
                     icon_url="https://i.postimg.cc/kgKdZLW5/Bean-Man2-132.gif")
    Embed.add_field(name="GitHub Description",
                    value="An Open Source Bot created by Me! (If you are gonna use the code to create a bot of your own. Please use a different name and bot profile picture)")
    await ctx.reply(embed=Embed)


@bot.command()
async def Disconnect(cxt):
    user = str(cxt.author)
    if user == "BeanMan#8008":
        await cxt.reply("Disconnecting...")
        time.sleep(1)
        await bot.change_presence(status=discord.Status.invisible, activity=None)
        await bot.close()


@bot.event
async def on_guild_join(guild):
    #print("change Text")
    # print(guild.text_channels)
    welc = open("BotJoin.md", "r")
    welc = str(welc.read())
    channel = bot.get_channel(839919450186711121)
    Embed = discord.Embed(
        title="BeanBot", url="https://github.com/BeanMan1408/BeanBot-v0.1", description=welc, color=0xf6ff00)
    Embed.set_thumbnail(
        url="https://i.postimg.cc/zDH5KL3W/Bean-Bot-Transparent-Back.png")
    Embed.set_author(name="BeanMan", url="https://github.com/BeanMan1408",
                     icon_url="https://i.postimg.cc/kgKdZLW5/Bean-Man2-132.gif")
    await channel.send(embed=Embed)


@bot.event
async def on_ready():
    print("w")
    active = discord.Game(name="Active")
    await bot.change_presence(activity=active, status=discord.Status.online)


bot.run(TOKEN)
bot.close

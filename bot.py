from discord import appinfo
import python_weather
import discord
from discord.ext import commands
import os
from ping3 import ping
import time
import paho.mqtt.client as mqtt
# Has all my info. Feel free to create your own SECRET.py file and add your own info.
import SECRET
from multiprocessing import Process
from syncer import sync
import random
import asyncio

intents = discord.Intents.all()
intents.presences = True
bot = commands.Bot(command_prefix='/', intents=intents)
TOKEN = SECRET.TOKEN
Broker = SECRET.BROKER
Port = SECRET.PORT
Topic = SECRET.TOPIC

""" NOTE: Currently Scraped
cheese = mqtt.Client(client_id=SECRET.CLIENTUSER, transport="tcp",
                     clean_session=False, userdata=None)

cheese.connect(host=Broker, port=Port, keepalive=60)

cheese.subscribe(topic=Topic, qos=1)
"""


def Pinged(host):  # Pings BeanBot's network to a domain.
    mes = ping(host) * 1000
    # print(ping(host))
    time.sleep(1)
    hee = str(mes)
    wee = hee[0] + hee[1] + hee[2] + hee[3] + hee[4] + hee[5] + 'ms'
    time.sleep(1)
    toReturn = str("Pinged " + host + ": " + wee)
    print(toReturn)
    return wee


async def fore(Location):  # Gets the current weather in a chosen city.
    Location = str(Location)
    c = python_weather.Client(format=python_weather.METRIC)
    weather = await c.find(Location)
    await c.close()
    we = str(weather.current.temperature)
    return we


@bot.command()
async def PingWifi(ctx, arg):  # Sends the ping information from Pinged().
    Embed = discord.Embed(title="Pinged", color=0xff0000)
    Embed.add_field(name=arg, value=Pinged(arg))
    await ctx.reply(embed=Embed)


@bot.command()
async def PingWeather(ctx, arg):  # Sends the current weather in a chosen city.
    orig = "-" or "_"
    wether = await fore(arg)
    arg = str(arg)
    if arg.__contains__('_'):
        we = arg.replace('_', ' ')
    elif arg.__contains__('-'):
        we = arg.replace('-', ' ')
    Embed = discord.Embed(title="Current Weather for " + we, color=0xabf7ff)
    Embed.set_thumbnail(url="https://i.postimg.cc/X72SYszf/Weather.png")
    Embed.add_field(name=we, value=wether + "°C")
    await ctx.reply(embed=Embed)


@bot.command()
# Plays Rock, Paper, Scissors (excuse the spaghetti code).
async def rps(ctx, args):
    o = random.randrange(1, 4)
    status = ""
    chose = ""
    # Tied
    # Rock
    if args == "rock" and o == 1:
        status = "We tied!"
        chose = "I chose rock :rock:"
    # Paper
    elif args == "paper" and o == 2:
        status = "We tied!"
        chose = "I chose paper :newspaper:"
    # Scissors
    elif args == "scissors" and o == 3:
        status = "We tied!"
        chose = "I chose scissors :scissors:"
    # You won
    # Paper
    elif args == "paper" and o == 1:
        status = "You won!"
        chose = "I chose rock :rock:"
    # Scissors
    elif args == "scissors" and o == 2:
        status = "You won!"
        chose = "I chose paper :newspaper:"
    # Rock
    elif args == "rock" and o == 3:
        status = "You won!"
        chose = "I chose scissors :scissors:"
    # Bot won
    # Paper
    elif args == "paper" and o == 3:
        status = "I won!"
        chose = "I chose scissors :scissors:"
    # Scissors
    elif args == "scissors" and o == 1:
        status = "I won!"
        chose = "I chose rock :rock:"
    # Rock
    elif args == "rock" and o == 2:
        status = "I won!"
        chose = "I chose paper :newspaper:"
    Embed = discord.Embed(title=status, description=chose, color=0xa8ffb7)
    await ctx.reply(embed=Embed)


@bot.command()
async def Help(ctx):  # Sends info about current commands.
    file = open("help.md", "r")
    fileRead = str(file.read())
    Embed = discord.Embed(
        title="Help", description=fileRead, color=0x0400ff)
    Embed.set_footer(text="More Commands are coming soon")
    await ctx.reply(embed=Embed)


@bot.command()
async def AboutMe(ctx):  # Sends info about BeanBot.
    welc = open("BotJoin.md", "r")
    welc = str(welc.read())
    Embed = discord.Embed(
        title="BeanBot version 0.21", url="https://github.com/BeanMan1408/BeanBot", description=welc, color=0xffffff)
    Embed.set_thumbnail(
        url="https://i.postimg.cc/zDH5KL3W/Bean-Bot-Transparent-Back.png")
    Embed.set_author(name="BeanMan", url="https://github.com/BeanMan1408/BeanBot",
                     icon_url="https://i.postimg.cc/kgKdZLW5/Bean-Man2-132.gif")
    Embed.add_field(name="GitHub Description",
                    value="An Open Source Bot created by Me! (If you are gonna use the code to create a bot of your own. Please use a different name and bot profile picture)")
    await ctx.reply(embed=Embed)

"""
@bot.command()
async def InviteBean(ctx): # Sends and Invite Link to the user.
    Embed = discord.Embed(title="Invite BeanBot to your Discord server!",
                          description="SECRET.INVITE", color=0xfff894)
    Embed.set_thumbnail(
        url="https://i.postimg.cc/zDH5KL3W/Bean-Bot-Transparent-Back.png")
    await ctx.reply(embed=Embed)
    pass
"""


@bot.event
async def on_ready():  # does stuff once the bot is ready.
    print("Online")
    active = discord.Game(name="Active")
    await bot.change_presence(activity=active, status=discord.Status.online)
    bot.appinfo = await bot.application_info()


@bot.command()
# Useful when adding new commands (Can only be used by the bot owner).
async def Disconnect(cxt):
    owner = bot.appinfo.owner
    user = cxt.author
    if user == owner:
        await cxt.reply("Disconnecting...")
        time.sleep(1)
        await bot.change_presence(status=discord.Status.invisible, activity=None)
        await bot.change_presence(status=discord.Status.invisible, activity=None)
        await bot.change_presence(status=discord.Status.invisible, activity=None)
        await bot.close()

""" NOTE: Currently Scraped
@sync
async def on_message(client, userdata, message):
    mes = str(message.payload.decode())
    # print(mes)
    if mes == "Disconn":
        print(mes)
        await Disconnect
"""


@bot.event
# Sends a welcome message when a user joins (Please excuse the mild spaghetti code).
async def on_member_join(member):
    guild = member.guild
    mem = guild.members
    mem = len(mem)
    channel = guild.system_channel
    welc = "Hi " + member.name + "! You're our " + str(mem) + "st member!"
    if mem == 1:
        welc = "You're our " + str(mem) + "st member!"
    elif mem == 2:
        welc = "You're our " + str(mem) + "nd member!"
    elif mem == 3:
        welc = "You're our " + str(mem) + "rd member!"
    else:
        welc = "You're our " + str(mem) + "th member!"
    Embed = discord.Embed(title="Hi " + member.name + "!",
                          description=welc, color=0xffffff)
    await channel.send(embed=Embed)
    pass

"""
@bot.event
async def on_disconnect(): # NOTE: Currently Scraped
    print("botbotbotbotbot")
    inactive = discord.Game(name="Disconnecting...")
    await bot.change_presence(activity=inactive, status=discord.Status.idle)
    await bot.change_presence(activity=inactive, status=discord.Status.idle)
    time.sleep(1.5)
    await bot.change_presence(activity=None, status=discord.Status.invisible)
    await bot.change_presence(activity=None, status=discord.Status.invisible)
"""


@bot.event
# When the bot joins a server, send a welcome message to the sys messages channel.
async def on_guild_join(guild):
    welc = open("BotJoin.md", "r")
    welc = str(welc.read())
    channel = guild.system_channel
    Embed = discord.Embed(
        title="BeanBot", url="https://github.com/BeanMan1408/BeanBot", description=welc, color=0xf6ff00)
    Embed.set_thumbnail(
        url="https://i.postimg.cc/zDH5KL3W/Bean-Bot-Transparent-Back.png")
    Embed.set_author(name="BeanMan", url="https://github.com/BeanMan1408",
                     icon_url="https://i.postimg.cc/kgKdZLW5/Bean-Man2-132.gif")
    await channel.send(embed=Embed)


@bot.command()
# Displays the welcome message when the bot joined the server.
async def Welcome(ctx):
    welc = open("BotJoin.md", "r")
    welc = str(welc.read())
    Embed = discord.Embed(
        title="BeanBot", url="https://github.com/BeanMan1408/BeanBot", description=welc, color=0xf6ff00)
    Embed.set_thumbnail(
        url="https://i.postimg.cc/zDH5KL3W/Bean-Bot-Transparent-Back.png")
    Embed.set_author(name="BeanMan", url="https://github.com/BeanMan1408",
                     icon_url="https://i.postimg.cc/kgKdZLW5/Bean-Man2-132.gif")
    await ctx.reply(embed=Embed)


@bot.command()
async def MemberList(ctx):  # Gets and sends a list of members in the server.
    mem = ctx.guild.members
    mem = str(len(mem))
    Embed = discord.Embed(title="There are " + mem +
                          " members in " + str(ctx.guild.name), color=0xffffff)
    await ctx.reply(embed=Embed)
    pass


# cheese.on_message = on_message #NOTE: Currently Scraped


def startBot():
    bot.run(TOKEN)


""" NOTE: Currently Scraped
def startServer():
    cheese.loop_forever()
"""

if __name__ == "__main__":
    p1 = Process(target=startBot)
    # p2 = Process(target=startServer) #NOTE: Currently Scraped
    p1.start()
    # p2.start() #NOTE: Currently Scraped

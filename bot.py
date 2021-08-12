import discord
from discord import message
from discord import client
from discord import embeds
from discord.enums import Status
from discord.ext import commands
import os
from discord.ext.commands.core import is_owner
from ping3 import ping
import time
import paho.mqtt.client as mqtt
import SECRET
from multiprocessing import Process
from syncer import sync
import asyncio

intents = discord.Intents.default()
intents.presences = True
bot = commands.Bot(command_prefix='/', intents=intents)
TOKEN = SECRET.TOKEN
Broker = SECRET.BROKER
Port = SECRET.PORT
Topic = SECRET.TOPIC

cheese = mqtt.Client(client_id=SECRET.CLIENTUSER, transport="tcp",
                     clean_session=False, userdata=None)

cheese.connect(host=Broker, port=Port, keepalive=60)

cheese.subscribe(topic=Topic, qos=1)


@bot.event
async def on_disconnect():
    global bot
    bot = commands.Bot(command_prefix='/', intents=intents)
    inactive = discord.Game(name="Disconnecting...")
    await bot.change_presence(activity=inactive, status=discord.Status.idle)
    await bot.change_presence(activity=inactive, status=discord.Status.idle)
    time.sleep(1.5)
    await bot.change_presence(activity=None, status=discord.Status.invisible)
    await bot.change_presence(activity=None, status=discord.Status.invisible)


async def ifClosed():
    if discord.Client.is_closed(bot) == True:
        await on_disconnect()


def Pinged(host):
    mes = ping(host) * 1000
    # print(ping(host))
    time.sleep(1)
    hee = str(mes)
    wee = hee[0] + hee[1] + hee[2] + hee[3] + hee[4] + hee[5] + 'ms'
    time.sleep(1)
    toReturn = str("Pinged " + host + ": " + wee)
    print(toReturn)
    return wee


@sync
async def on_message(client, userdata, message):
    mes = str(message.payload.decode())
    # print(mes)
    if mes == "Disconn":
        print(mes)
        await bot.close()
        await ifClosed()


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
        title="BeanBot version 0.2", url="https://github.com/BeanMan1408/BeanBot-v0.2", description=welc, color=0xffffff)
    Embed.set_thumbnail(
        url="https://i.postimg.cc/zDH5KL3W/Bean-Bot-Transparent-Back.png")
    Embed.set_author(name="BeanMan", url="https://github.com/BeanMan1408/BeanBot-v0.2",
                     icon_url="https://i.postimg.cc/kgKdZLW5/Bean-Man2-132.gif")
    Embed.add_field(name="GitHub Description",
                    value="An Open Source Bot created by Me! (If you are gonna use the code to create a bot of your own. Please use a different name and bot profile picture)")
    await ctx.reply(embed=Embed)


@bot.command()
async def Disconnect(cxt):
    bot.owner_id = 611983174305841152
    user = cxt.author.id
    if user == bot.owner_id:
        await cxt.reply("Disconnecting...")
        time.sleep(1)
        await bot.change_presence(status=discord.Status.invisible, activity=None)
        await bot.change_presence(status=discord.Status.invisible, activity=None)
        await bot.change_presence(status=discord.Status.invisible, activity=None)
        await bot.close()


@bot.event
async def on_guild_join(guild):
    welc = open("BotJoin.md", "r")
    welc = str(welc.read())
    channel = bot.get_channel(839919450186711121)
    Embed = discord.Embed(
        title="BeanBot", url="https://github.com/BeanMan1408/BeanBot-v0.2", description=welc, color=0xf6ff00)
    Embed.set_thumbnail(
        url="https://i.postimg.cc/zDH5KL3W/Bean-Bot-Transparent-Back.png")
    Embed.set_author(name="BeanMan", url="https://github.com/BeanMan1408",
                     icon_url="https://i.postimg.cc/kgKdZLW5/Bean-Man2-132.gif")
    await channel.send(embed=Embed)


@bot.event
async def on_ready():
    print("Online")
    active = discord.Game(name="Active")
    await bot.change_presence(activity=active, status=discord.Status.online)


def ListOfCommands():
    global bot
    bot = commands.Bot(command_prefix='/', intents=intents)
    bot.add_command(PingWifi)
    bot.add_command(Help)
    bot.add_command(AboutMe)
    return


cheese.on_message = on_message


def startBot():
    bot.run(TOKEN)


def startServer():
    cheese.loop_forever()


if __name__ == "__main__":
    p3 = Process(target=ListOfCommands)
    p1 = Process(target=startBot)
    #p2 = Process(target=startServer)
    p1.start()
    # p2.start()
    p3.start()

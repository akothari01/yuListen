from pytubefix import YouTube
import discord
from discord.ext import commands
from playList import playList, playNode
import asyncio
import os
from dotenv import load_dotenv


queue = playList()

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!yu ", intents=intents)

@bot.command()
async def join(ctx):
    if ctx.author.voice:
        await ctx.author.voice.channel.connect()
        await ctx.send("Yu is here!")
    else:
        await ctx.send("Yu needs you to join :(")

@bot.command()
async def play(ctx, url):
    vc = ctx.voice_client
    if vc.is_playing() or vc.is_paused():
        vc.stop() 
    yt = YouTube(url)
    print(yt.title)
    await ctx.send("Yu will now play " + yt.title)
    ys = yt.streams.get_audio_only()
    sng = ys.download(filename="test1.mp4") 
    source = discord.FFmpegOpusAudio(source=sng)
    if queue.head != None:
        ctx.voice_client.play(
            source,
            after=lambda e: asyncio.run_coroutine_threadsafe(play(ctx, queue.head.playLink), bot.loop)
        )
    else:
            ctx.voice_client.play(
            source,
            after=lambda e: asyncio.run_coroutine_threadsafe(play(ctx), bot.loop)
        )

@bot.command()
async def clear(ctx):
    queue.clearList()


@bot.command()
async def add(ctx, url):
    queue.insert(url)
    queue.printList()
    await ctx.send("Yu will add " + YouTube(url).title + " for you!")

@bot.command()
async def rest(ctx):
    node = queue.head
    answer = ""
    while node != None:
        answer += YouTube(node.playLink).title
        answer += "\n"
        node = node.next
    await ctx.send(answer)

@bot.command()
async def skip(ctx):
    if queue.head is not None:
        ctx.voice_client.stop()
        await ctx.send("Okie, Yu will sskip :(")
        asyncio.run_coroutine_threadsafe(play(ctx, queue.head.playLink), bot.loop)
    else:
        await ctx.send("Yu can't skip to something that doesn't exist (>.//.<)")

@bot.command()
async def myhelp(ctx):
    await ctx.send("Hello! I am Yu (>.//.<)\nI can play music!\nhere are my commands\n!yu play *insert url from youtube*\n !yu add *insert url*\n !yu skip\n !yu rest (to see your list)\nENJOY!!")

bot.run(TOKEN)
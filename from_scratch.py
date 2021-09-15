import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from discord import TextChannel
from youtube_dl import YoutubeDL

load_dotenv()
bot = commands.Bot(command_prefix=',')

players = {}

queue = []

@bot.event
async def on_ready():
    print('Bot online')


# Join vc command
@bot.command(aliases = ["j", "connect", "c"])
async def join(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await ctx.send("Already connected to " + str(channel))
    else:
        voice = await channel.connect()


# Play audio
@bot.command(aliases = ["p", "pl"])
async def play(ctx, url):
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    voice = get(bot.voice_clients, guild=ctx.guild)

    if not voice.is_playing():
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['url']
        print (str(URL))
        await ctx.send(str(URL))
        voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS, executable="FFmpeg.exe"))
        voice.is_playing()
        await ctx.send('Bot is playing')

# Check if the bot is already playing
    else:
        await ctx.send("Bot is already playing")
        return


# End pause
@bot.command(aliases = ["r", "re", "res"])
async def resume(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)

    if not voice.is_playing():
        voice.resume()
        await ctx.send('Bot is resuming')


# Pause music
@bot.command()
async def pause(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice.is_playing():
        voice.pause()
        await ctx.send('Music paused')


# Stop
@bot.command()
async def stop(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice.is_playing():
        voice.stop()
        await ctx.send('Stopping...')


# Disconnect from vc
@bot.command(aliases = ["d", "dis", "disc", "dc", "fuckoff", "leave"])
async def disconnect(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    await voice.disconnect()



bot.run(os.getenv('TOKEN'))

import discord
import os
# load our local env so we dont have the token in public
from dotenv import load_dotenv
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from discord import TextChannel
from youtube_dl import YoutubeDL
import ffmpeg

load_dotenv()
bot = commands.Bot(command_prefix=',')  # prefix our commands with '.'

players = {}


@bot.event  # check if bot is ready
async def on_ready():
    print('Bot online')


# command for bot to join the channel of the user, if the bot has already joined and is in a different channel, it will move to the channel the user is in
@bot.command()
async def join(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_bots, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()


# command to play sound from a youtube URL
@bot.command()
async def play(ctx, url):
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    voice = get(bot.voice_bots, guild=ctx.guild)

    if not voice.is_playing():
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['url']
        voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS, executable="C:/Users/Maxim N/Downloads/ffmpeg/bin/ffmpeg.exe"))
        voice.is_playing()
        await ctx.send('Bot is playing')

# check if the bot is already playing
    else:
        await ctx.send("Bot is already playing")
        return


# command to resume voice if it is paused
@bot.command()
async def resume(ctx):
    voice = get(bot.voice_bots, guild=ctx.guild)

    if not voice.is_playing():
        voice.resume()
        await ctx.send('Bot is resuming')


# command to pause voice if it is playing
@bot.command()
async def pause(ctx):
    voice = get(bot.voice_bots, guild=ctx.guild)

    if voice.is_playing():
        voice.pause()
        await ctx.send('Bot has been paused')


# command to stop voice
@bot.command()
async def stop(ctx):
    voice = get(bot.voice_bots, guild=ctx.guild)

    if voice.is_playing():
        voice.stop()
        await ctx.send('Stopping...')


# command to clear channel messages
@bot.command()
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)
    await ctx.send("Messages have been cleared")



Perms = "137488617024"
Invite = "https://discord.com/api/oauth2/authorize?client_id=887511460324970496&permissions=137488617024&scope=bot"
bot.run(os.getenv('TOKEN'))

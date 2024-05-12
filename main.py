import discord
from discord.ext import commands
import youtube_dl
import asyncio
from discord import Intents

bot = commands.Bot(command_prefix='!', intents=Intents.all())

@bot.event
async def on_ready():
    print("Yurrrrrrrrrr!")

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(1238350633015447560)
    await channel.send(f"Welcome to the City Of Fallen Angels!, {member.mention}!")
    
    guild = member.guild
    role = discord.utils.get(guild.roles, id=1238350632142897236)
    if role:
        await member.add_roles(role)
    else:
        print("Role not found!")
    
    memberCount = guild.member_count
    channel_to_update = bot.get_channel(1238350633015447555)
    await channel_to_update.edit(name=f"Members: {memberCount}")

spam_counter = {}

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    user_id = message.author.id
    if user_id not in spam_counter:
        spam_counter[user_id] = 0

    spam_counter[user_id] += 1

    if spam_counter[user_id] >= 7:
        await message.channel.send(f"{message.author.mention} has been timed out for Sucking Dick.")
        await message.author.add_roles(message.guild.get_role(1239147083672457216))  # Add timeout role here
        await message.channel.set_permissions(message.author, send_messages=False, reason="User spamming")
        await asyncio.sleep(600)  # 10 minutes timeout
        await message.channel.set_permissions(message.author, send_messages=True, reason="Timeout ended")
        spam_counter[user_id] = 0

    await bot.process_commands(message)

@bot.command()
async def members(ctx):
    guild = ctx.guild
    member_count = guild.member_count
    await ctx.send(f"There are {member_count} members in this server.")

@bot.command()
async def play(ctx, url):
    # Check if the user is in a voice channel
    if not ctx.author.voice:
        await ctx.send("You need to be in a voice channel to use this command.")
        return

    # Join the voice channel of the user who invoked the command
    channel = ctx.author.voice.channel
    voice_client = await channel.connect()

    # Download audio from YouTube video
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'extractaudio': True,  # Explicitly specify extractaudio flag
        'verbose': True,  # Enable verbose output
        'extractor': 'youtube',  # Use the YoutubeIE extractor
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info['formats'][0]['url']
        voice_client.play(discord.FFmpegPCMAudio(url2))

@bot.command()
async def stop(ctx):
    # Check if the bot is in a voice channel
    if ctx.voice_client:
        # Disconnect the bot from the voice channel
        await ctx.voice_client.disconnect()
    else:
        await ctx.send("I'm not in a voice channel.")
bot.run("MTIzOTEyNzM5NzcxMDgyMzQ1NQ.GVRVX1.WDnBeNqcBEw51z_NtCvaNz2YfuuNP5F9EYSPVQ")
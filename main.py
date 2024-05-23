import logging
import discord
from discord.ext import commands
import youtube_dl
import asyncio
import random
import datetime
from discord import Intents
import argparse

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s (%(name)s) [%(levelname)s] %(message)s")
logger = logging.getLogger("za_bot")

bot = commands.Bot(command_prefix="!", intents=Intents.all())


@bot.event
async def on_ready():
    logger.info("Yurrrrrrrrrr!")


@bot.event
async def on_member_join(member):
    channel = bot.get_channel(1238350633015447560)
    await channel.send(f"Welcome to the City Of Fallen Angels!, {member.mention}!")

    guild = member.guild
    role = discord.utils.get(guild.roles, id=1238350632142897236)
    if role:
        await member.add_roles(role)
    else:
        logger.error("Role not found!")

    member_count = guild.member_count
    channel_to_update = bot.get_channel(1238350633015447555)
    await channel_to_update.edit(name=f"Members: {member_count}")


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
        await message.channel.send(f"{message.author.mention} Shut The Fuck Up.")
        try:
            until = datetime.datetime.now(tz=datetime.UTC) + datetime.timedelta(
                minutes=10
            )
            logger.info(f"Timing Out User {message.author.mention}")
            await message.author.timeout(until, reason="User spamming")
        except Exception as e:
            logger.error(f"Failed to timeout {message.author}: {e}")
        spam_counter[user_id] = 0

    await bot.process_commands(message)


@bot.command()
async def members(ctx):
    guild = ctx.guild
    member_count = guild.member_count
    await ctx.send(f"There are {member_count} members in this server.")

@bot.command()
async def heartbeat(ctx):
    logger.info("Za Bot Im Alive NIGGUH")
    await ctx.send("check the console")


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
        "format": "bestaudio/best",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "extractaudio": True,  # Explicitly specify extractaudio flag
        "verbose": True,  # Enable verbose output
        "extractor": "youtube",  # Use the YoutubeIE extractor
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info["formats"][0]["url"]
        voice_client.play(discord.FFmpegPCMAudio(url2))


@bot.command()
async def stop(ctx):
    # Check if the bot is in a voice channel
    if ctx.voice_client:
        # Disconnect the bot from the voice channel
        await ctx.voice_client.disconnect()
    else:
        await ctx.send("I'm not in a voice channel.")


@bot.command()
async def giveaway(ctx, duration: int, prize: str, winners: int):
    await ctx.send(
        f"🎉 **Giveaway started!** 🎉\n\nPrize: {prize}\nDuration: {duration} hour(s)\nWinners: {winners}"
    )

    # Sleep for the duration of the giveaway
    await asyncio.sleep(duration * 3600)

    # Get all members of the server
    members = ctx.guild.members

    # Filter out bots
    eligible_members = [member for member in members if not member.bot]

    # Randomly select winners
    giveaway_winners = random.sample(
        eligible_members, min(len(eligible_members), winners)
    )

    # Announce winners
    winner_mentions = " ".join([winner.mention for winner in giveaway_winners])
    await ctx.send(
        f"🎉 **Giveaway ended!** 🎉\n\nPrize: {prize}\nWinners: {winner_mentions}\n\nCongratulations to the winners!"
    )


parser = argparse.ArgumentParser()
parser.add_argument("token", help="specify bot token to use")
cmdline = parser.parse_args()

bot.run(cmdline.token)

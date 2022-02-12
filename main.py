# bot.py
import os

from jkli import JKLIclient

from dotenv import load_dotenv

from discord.ext import commands

bot = commands.Bot(command_prefix='!')

load_dotenv('jkli.env')
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = JKLIclient(bot,RIOT_KEY = 'RGAPI-634c3b4c-9fc1-4ef2-938a-cbccd195607d')

client.run(TOKEN)
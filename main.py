# bot.py
import os

from jkli import JKLIclient

from dotenv import load_dotenv

from discord.ext import commands

bot = commands.Bot(command_prefix='$')

load_dotenv('jkli.env')
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = JKLIclient(bot,RIOT_KEY = 'RGAPI-2bfb8207-3929-4c46-a98e-e5d7c50ca0fd')

client.run(TOKEN)
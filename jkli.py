from discord.ext import commands

import config
import cassiopeia as cass
from cassiopeia import Summoner, Match, Patch, Champion
from cassiopeia.core import MatchHistory
from cassiopeia import Queue
from riotwatcher import RiotWatcher

import random

class JKLIclient(commands.Bot):
    def __init__(self,*args,**kwargs):
      commands.Bot.__init__(self,args)
      cass.set_riot_api_key(kwargs.get('RIOT_KEY'))
      watcher = RiotWatcher(kwargs.get('RIOT_KEY'))


    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')
    
    async def on_member_join(self,member):
        await member.create_dm()
        await member.dm_channel.send(
            f'Hi {member.name}, welcome to my Discord server!'
          )   

    #give user a choice
    async def option_menu(self,message):
      reactions = ["0️⃣","1️⃣","2️⃣"]
      for i in reactions:
          await message.add_reaction(i)

      reaction, user = await self.wait_for("reaction_add",check=lambda react, user: user == message.author)
      
      if user == message.author and str(reaction.emoji) in reactions and reaction.message == message:
        return reactions.index(reaction.emoji)
      return -1

    #get the the first 7 champion mastery for summoner
    def get_mastery(self,summ):
      response = ""
      try:
        for i in range(min(len(summ.champion_masteries),7)):
          response += summ.champion_masteries[i].champion.name + " : "
          response += str(summ.champion_masteries[i].points) + "\n"
      except Exception:
        response ="Summoner does not exist"
      return response

    #on user message !summoner
    async def on_message(self,message):
      if message.author == self.user:
          return
      
      if message.content.index(":") != -1:
        content = message.content.split(":")

      content[0] = content[0].strip().lower()
      content[1] = content[1].strip()

      response = ""
      if content[0] == '!summoner':
        ch = await self.option_menu(message)
      
        summ = Summoner(name = content[1], region ="NA")
        
        if(ch == 0):
          response =  self.get_mastery(summ)
           
        elif ch == 1:
          "stuff"

      
      await message.channel.send(response)

    


    async def shutdown(self,ctx):
      await ctx.bot.logout()


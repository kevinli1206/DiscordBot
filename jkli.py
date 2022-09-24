from discord.ext import commands

import cassiopeia as cass
from cassiopeia import Summoner, Match, Patch, Champion
from cassiopeia.core import MatchHistory
from cassiopeia import Queue
#from riotwatcher import RiotWatcher


#Primary client for JKLI Bot
class JKLIclient(commands.Bot):
    def __init__(self,*args,**kwargs):
      commands.Bot.__init__(self,args)
      cass.set_riot_api_key(kwargs.get('RIOT_KEY'))
      
      #watcher = RiotWatcher(kwargs.get('RIOT_KEY'))

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')
    
    async def on_member_join(self,member):
        await member.create_dm()
        await member.dm_channel.send(
            f'Hi {member.name}, welcome to my Discord server!'
          )   

    #give user a choice
    async def option_menu(self,message):
      reactions = ["0️⃣","1️⃣","2️⃣","3️⃣","4️⃣","5️⃣"]
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
        masteries = summ.champion_masteries
        for i in range(min(len(masteries),7)):
          response += masteries[i].champion.name + " : "
          response += str("{:,}".format(masteries[i].points)) + "\n"
      except Exception:
        response ="Summoner does not exist"
      return response

    #get the summoner's current rank
    def get_rank(self,summ):
      response = ""
      try:
        response = "Current Season Rank: \n"
        response += str(summ.ranks[Queue.ranked_solo_fives].tier);
        response += " " +str(summ.ranks[Queue.ranked_solo_fives].division)
      except Exception:
        response ="Summoner is not ranked"
      return response

    #get the summoner's level
    def get_level(self,summ):
      response = ""
      try:
        response = "Current Level: \n"
        response += str(summ.level);
      except Exception:
        response ="Summoner does not exist"
      return response

    #get the summoner's level
    def get_game(self,summ):
      response = ""
      
      try:
        match = summ.current_match
        response += "Blue Team: "
        for i in match.blue_team.participants:
          response += i.summoner.name + " | ";
        response = response[0:len(response)-2]
        response += "\n                                              vs.\n"

        response += "Red Team: "
        for i in match.red_team.participants:
          response += i.summoner.name + " | ";
        response = response[0:len(response)-2]
        response += "\n" + "Game Type: \n"
        queue = str(match.queue)
        queue = queue[6:len(queue)].replace("_", " ")
        response += queue;
      except Exception:
        response ="Summoner not in game"
        
      return response

    #get winrates for top 7 most played champs
    def get_winrates(self,summ,matches):
      response = "Win Rate Over 20 Games: \n"
      try:
        wins = 0
        total = 0

        for j in matches:
          team = j.blue_team

          for k in j.red_team.participants:
            if summ.name == k.summoner.name:
              team = j.red_team

          if team.win: wins += 1
          total +=1
        
        if total != 0:
          response += str(round(wins/total * 100,2)) + " %\n"
        else:
          response += str(0) + " %\n"

      except Exception:
        response = "Summoner does not exist"

      return response

    #commands weird, this until fix
    async def summ_help(self,message):
      print("here")
      response = "Type \"!summoner:{summoner_name}\" to get the statistics of the given summoner.\nReact with 0 to get summoner's highest mastery champions.\nReact with 1 to get summoner's winrates on highest mastery champions.\nReact with 2 to get champion's rank.\nReact with 3 to get summoner level.\nReact with 4 to get summoner game info.\nReact with 5 to quit"
      await message.channel.send(response)


    #on user message !summoner
    async def on_message(self,message):
      if message.author == self.user:
          return

      if message.content == "!help" :
        await self.summ_help(message)
        return;

      
      if ":" in message.content:
        content = message.content.split(":")
      else: return

      content[0] = content[0].strip().lower()
      content[1] = content[1].strip()

      response = ""
      #front load api calls
      try:
        summ = Summoner(name = content[1], region ="NA")
        matches = summ.match_history

        #make sure the match is valid and contains our person
        def match_filter(match):
              for i in match.participants:
                if i.summoner.name == summ.name:
                  return True
              return False
      
        matches.filter(match_filter)

      except Exception:
        print(Exception)
        await message.channel.send("Summoner Does Not Exist")
        return;
        
      while True:
        if content[0] == '!summoner':
          ch = await self.option_menu(message)
          if(ch == 0):
            response =  self.get_mastery(summ)+"\n\n"
          elif ch == 1:
            response = self.get_winrates(summ,matches)+"\n\n"
          elif ch == 2:
            response = self.get_rank(summ) +"\n\n"
          elif ch == 3:
            response = self.get_level(summ)+"\n\n"
          elif ch == 4:
            response = self.get_game(summ)+"\n\n"
          elif ch == 5:
            await message.channel.send("Peace.")
            return;
          await message.channel.send(response)

    async def shutdown(self,ctx):
      await ctx.bot.logout()


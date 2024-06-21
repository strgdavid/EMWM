import asyncio
import datetime
import json
import os
import random
import re

import discord
import requests
from bs4 import BeautifulSoup
from discord.ext import commands, tasks
from discord.flags import Intents
from dotenv import load_dotenv

from webserver import keep_alive

#variablen
load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_SECRET')


#discord bot
client =  commands.Bot(command_prefix=commands.when_mentioned_or("?"), help_command=None, intents=discord.Intents.all())
client.remove_command('help')
prefix = "?"


@client.event
async def on_ready():
    print(f"{client.user.name} is online")
    print(f"id: {client.user.id}")
    await status_task()


async def status_task():
    while True:
      await client.change_presence(activity=discord.Activity(type=discord.ActivityType.custom, 
                                                             name = '@',
                                                             state = '@strgdavid\'s Bot'))
      await asyncio.sleep(8)
      await client.change_presence(activity=discord.Activity(type = discord.ActivityType.custom, 
                                                             name = 'Entwicklungsphase',
                                                             state = 'In der Entwicklungsphase'))
      await asyncio.sleep(8)


@client.command(name='help')#, pass_context=True)
async def help(ctx):
  author = ctx.message.author

  embed = discord.Embed(
    colour = discord.Colour.orange()
  )

  embed.set_author(name="Help")
  embed.add_field(name="!help",value="Help command",inline=False)

  #await client.send_message(author,embed=embed)
  await ctx.send(embed=embed)
  #await client.say("Message sent to your DMs")

@client.command(name='gif')#, pass_context=True)
async def gif(ctx):
  await ctx.send('https://tenor.com/view/emirmono-mittelfinger-gif-791195104924975174')

#def is_date_in_range(date, start_date, end_date):
#   return start_date <= date <= end_date


@client.command(name='em')
async def em(ctx):
  date = datetime.date.today() #2024-06-20 anscheinend String
  
  datetime_now = datetime.datetime.now()
  dt2 = datetime.datetime(2023, 6, 20)
  
  if (datetime.datetime(1999, 1, 1) <= datetime_now <= datetime.datetime(2024, 6, 22)): #2. Spieltag bis 22.06.2024
    url = 'https://www.fussballdaten.de/em/2024/gruppenphase/2-spieltag/'
  elif (datetime.datetime(2024, 6, 23) <= datetime_now <= datetime.datetime(2024, 6, 26)): #3. Spieltag 23.06.2024-26.06.2024
    url = 'https://www.fussballdaten.de/em/2024/gruppenphase/3-spieltag/'
  elif (datetime.datetime(2024, 6, 27) <= datetime_now <= datetime.datetime(2024, 7, 2)): #Achtel 29.06.2024-02.07.2024
    url = 'https://www.fussballdaten.de/em/2024/achtelfinale/'
  elif (datetime.datetime(2024, 7, 3) <= datetime_now <= datetime.datetime(2024, 7, 6)): #Viertel 05.07.2024-06.07.2024
    url = 'https://www.fussballdaten.de/em/2024/viertelfinale/'
  elif (datetime.datetime(2024, 7, 7) <= datetime_now <= datetime.datetime(2024, 7, 10)): #Halb 09.07.2024-10.07.2024
    url = 'https://www.fussballdaten.de/em/2024/halbfinale/'
  elif (datetime.datetime(2024, 7, 11) <= datetime_now <= datetime.datetime(2024, 7, 14)): #Finale 14.07.2024
    url = 'https://www.fussballdaten.de/em/2024/finale/'
  else:
    url = 'https://www.fussballdaten.de/em/2024/finale/'
    
    #CHECKPOINT: URL FILTER JE NACH DATUM UND DAMIT AUCH SPIELTAG/XFINALE, DATETIMES EINSTELLEN AUF FILTER

    
  

  
  #1. Datum überprüfen
  #2. Spiele von dem Tag pullen
  #3. (schauen ob bald ein Spiel gespielt wird) kurz vor einem Spiel neue Wette eröffnen, Nachricht senden
  #4. bei der Nachricht anhand von Reaktionen wetten festlegen, wetten bis vor Spielbeginn akzeptieren, ändern können, neue wett-nachrichten schreiben zur bestätigung
  #5. bei halbzeit eventuell zwischenstand zeigen wer am nächsten dran ist
  #6. nach dem spiel das ergebnis festhalten, variablen in einer spielertabelle im code addieren/aktualisieren, nachricht des punktezuwachses schicken, zusätzlich punktestand
  # (zusätzliche befehle einbauen wie "leaderboard","historie {player}", "spiele-liste")

  
  

  
  #url = 'https://www.fussballdaten.de/em/2024/gruppenphase/2-spieltag/'
  html = requests.get(url)
  
  s = BeautifulSoup(html.content, 'html.parser')

  results = s.find(id = 'page-content')
  spielplan = results.find(class_ = 'content-spiele')
  spiel_titel = spielplan.find(class_ = 'spiele-row detils')
  
  spiel_titel_pl = spielplan.find_all(class_ = 'spiele-row detils')

  spiel_titel_pl_list = list(spiel_titel_pl)
  
  ###
  #spiel_titel_pl = spielplan.find_next(class_ = 'spiele-row detils')
  #spiel_titel_pl = spiel_titel.find
  ###
  
  n_spiele = len(spielplan.find_all(class_ = 'spiele-row detils'))


  for i in range(n_spiele):
    
  
  
    #result = re.split(r'([A-Za-z]+)(\d+:\d+)(\d+:\d+)([A-Za-z]+)([A-Z])', spiel_titel_pl_list[i].text) #spiel_titel ##########################
  
    ###
    #info_x = ""
    #for x in range(n_spiele):
    #  info_x = info_x + f"{result[x]} "


    land_1 = ""
    ergebnis = ""
    ergebnis_halb = ""
    land_2 = ""
    
    #land_1 = result[1]
    #ergebnis = result[2]
    #ergebnis_halb = result[3]
    #land_2 = result[4]
  
    #title_content = spiel_titel_pl_list[i].find(class_='ergebnis')['title'] #spiel_titel
  
    #spiel_datum = re.search(r'\((\d{2}\.\d{2}\.\d{4})', title_content).group(1)
  
    #nachricht = f"{spiel_datum}: {land_1} gegen {land_2}: {ergebnis} ({ergebnis_halb})"
    
    await ctx.send(spiel_titel_pl_list[i].text)
    #await ctx.send(spiel_titel_2)
  
    #print(spiel_titel_pl_list[1].text)
    
    #await ctx.send(f"{info_x} {spiel_datum}")
    
  #for i in range(n_spiele):
    

  






  





keep_alive()

client.run(TOKEN)
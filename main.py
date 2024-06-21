import asyncio
import datetime
import json
import os
import random
import datetime

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
  #await ctx.send('https://tenor.com/view/emirmono-mittelfinger-gif-791195104924975174')
  #await ctx.send('https://tenor.com/view/emirmono-mittelfinger-gif-791195104924975174')
  await ctx.send()

#def is_date_in_range(date, start_date, end_date):
#   return start_date <= date <= end_date


@client.command(name='em')
async def em(ctx):
  date = datetime.date.today() #2024-06-20 anscheinend String
  
  datetime_now = datetime.datetime.now()
  dt2 = datetime.datetime(2023, 6, 20)
  
  if(datetime.datetime(1999, 1, 1) <= datetime_now <= datetime.datetime(2100, 1, 1)):
    #print(dt)
    url = 'https://www.fussballdaten.de/em/2024/gruppenphase/2-spieltag/'
    print('ja, dazwischen') #CHECKPOINT: URL FILTER JE NACH DATUM UND DAMIT AUCH SPIELTAG/XFINALE, DATETIMES EINSTELLEN AUF FILTER

  
  #1. Datum überprüfen
  #2. Spiele von dem Tag pullen
  #3. (schauen ob bald ein Spiel gespielt wird) kurz vor einem Spiel neue Wette eröffnen, Nachricht senden
  #4. bei der Nachricht anhand von Reaktionen wetten festlegen, wetten bis vor Spielbeginn akzeptieren, ändern können, neue wett-nachrichten schreiben zur bestätigung
  #5. bei halbzeit eventuell zwischenstand zeigen wer am nächsten dran ist
  #6. nach dem spiel das ergebnis festhalten, variablen in einer spielertabelle im code addieren/aktualisieren, nachricht des punktezuwachses schicken, zusätzlich punktestand
  # (zusätzliche befehle einbauen wie "leaderboard","historie {player}", "spiele-liste")

  
  

  
  url = 'https://www.fussballdaten.de/em/2024/gruppenphase/2-spieltag/'
  html = requests.get(url)
  
  s = BeautifulSoup(html.content, 'html.parser')

  results = s.find(id = 'page-content')
  spielplan = results.find(class_ = 'content-spiele')
  #spiele = spielplan.find(class_ = 'spiele-row detils')
  n_spiele = len(spielplan.find_all(class_ = 'spiele-row detils'))
  
  print(n_spiele)
  #for i in range(n_spiele):
    #await ctx.send("ja")
    

  
  #await ctx.send('test')
  #print(soup.find_all(attrs={'class':'spiele-row.detils'}))





keep_alive()

client.run(TOKEN)
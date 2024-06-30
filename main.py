import asyncio
import datetime
import json
import os
import random
import re

import aiohttp
import discord
import pytz
import requests
import t
from bs4 import BeautifulSoup
from discord.ext import commands, tasks
from discord.flags import Intents
from dotenv import load_dotenv

import em_bets as embe
import em_datetime as emdt
import em_matches as emma
from webserver import keep_alive

#variablen
load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_SECRET')


#discord bot
client =  commands.Bot(command_prefix=commands.when_mentioned_or("?"), help_command=None, intents=discord.Intents.all())
client.remove_command('help')
prefix = "?"

tipp = False
em_channel_id = os.getenv('DISCORD_EM_CHANNEL_ID')







@client.event
async def on_ready():
    print(f"{client.user.name} is online")
    print(f"id: {client.user.id}")
    #send_message_loop.start()
    em_matches_loop.start()



    
    await status_task()
    #test1.start()
    #send_message_loop.start()










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
      #if tipp == False:
        


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
@client.command(name='clearchannel')
@commands.has_permissions(manage_messages=True)  # Optional: requires the user to have manage messages permissions
async def clear_channel(ctx, amount: int):
    await ctx.channel.purge(limit=amount)
    await ctx.send(f"Deleted {amount} messages.", delete_after=5)  # Optional: sends a confirmation message and deletes it after 5 seconds

  
def text1():
  return "text1"




@client.command(name='heutefake')
async def heutefake(ctx):
  date_now_str = emdt.get_date_now_str()

  matchObj_list = emma.get_spieltag_matches()

  #print(matchObj_list)
  
  for match in matchObj_list:
    #print(match.datum)
    
    if match.datum == "29.06.2024":
      await ctx.send(match)

@client.command(name='heute')
async def heute(ctx):
    date_now_str = emdt.get_date_now_str()

    matchObj_list = emma.get_spieltag_matches()

    #print(matchObj_list)

    for match in matchObj_list:
    #print(match.datum)

        if match.datum == date_now_str:
            await ctx.send(match)

@client.command(name='nextmatch')
async def nextmatch(ctx):
    message = emma.get_next_match()
    if message.land1 != "":
        await ctx.send(message)
    else:
        await ctx.send("Kein nächstes Match")

@client.command(name='today')
async def today(ctx):
    message = emma.get_matches_today()
    for match in message:
        await ctx.send(match)
    



##############################################

@client.command(name='openbets')
async def open_bets(ctx, client=client, match=emma.get_next_match()):
    pmatch = match if match else emma.get_next_match()
    await embe.open_bets(client, pmatch)

@client.command(name='openbetstest')
async def open_bets_test(ctx, client=client, match=emma.get_next_match()):
    await embe.open_bets(client, match)

@client.command(name='clearbets')
async def clear_bets(ctx, client=client):
    await embe.clear_bets(ctx, client)

@client.command(name='cleartxt')
async def clear_txt(ctx):
    await embe.clear_txt(ctx)

#@client.command(name='updatescores')
#async def update_scores(match):
#    await embe.update_scores(match) #kann nur vom bot benutzt werden, intern

@client.event
async def on_reaction_add(reaction, user):
    await embe.on_reaction_add(reaction, user)

async def process_reaction(reaction, user, country): #, bool = embe.process_reactions_bool
    await embe.process_reaction(reaction, user, country)




######################################################################################

async def test():
    channel = client.get_channel(int(os.getenv('DISCORD_EM_CHANNEL_ID')))
    if channel:
        await channel.send("gerade minutenzahl")
    else:
        print('Kanal nicht gefunden')


@tasks.loop(seconds=10)
async def test1():
    #channel = client.get_channel(int(os.getenv('DISCORD_EM_CHANNEL_ID')))
    channel = client.get_channel(1255542883243659436)
    #now = datetime.now()
    #if now.minute % 2 == 0:
    await channel.send("yes")


CHANNEL_ID=1255542883243659436
@tasks.loop(minutes=1)
async def send_message_loop():
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        await channel.send(emdt.get_time_now_packed())
    else:
        print(f"Kanal mit der ID {CHANNEL_ID} nicht gefunden")


@client.command(name='updatescores')
async def update_scores(ctx):
    await embe.update_scores(ctx)




bets_bet_is_open = False
bets_time_up = False





em_matches_in_loops = []


@tasks.loop(minutes=1)
async def em_matches_loop(): #ctx, client=client
    #print("test")
    #global em_matches_in_loops
    
    channel = client.get_channel(1255542883243659436)
    next_match = emma.get_next_match()
    time_next_match_packed = int(next_match.uhrzeit.replace(":", ""))
    time_now_packed = emdt.get_time_now_packed()
    
    if time_next_match_packed - time_now_packed < 300 and (next_match.land1+next_match.land2) not in em_matches_in_loops:
        #em_matches_in_loops.append(next_match)
        loop = create_new_em_loop(channel, next_match)
        loop.start()
        print(em_matches_in_loops)
        
    
    #send_message_loop.start()
    
    # next_match = emma.get_next_match()
    # time_next_match_packed = int(next_match.uhrzeit.replace(":", ""))
    # time_now_packed = emdt.get_time_now_packed()
    # if time_next_match_packed - time_now_packed < 100:

def create_new_em_loop(channel, match):
    @tasks.loop(minutes=1)
    async def test_loop():
        
        #global em_matches_in_loops
        time_match_packed = int(match.uhrzeit.replace(":", ""))
        time_now_packed = emdt.get_time_now_packed()
        
        if (match.land1+match.land2) not in em_matches_in_loops:
            await embe.open_bets(client, match)
            em_matches_in_loops.append(match.land1+match.land2)
        #if channel:
        #    await channel.send("test")
        if -10 <= time_match_packed - time_now_packed <= 0 and match in em_matches_in_loops:
            await embe.clear_bets(channel, client)
        if time_match_packed - time_now_packed <= -130 and match.ergebnis.replace(" ","") != "-:-": #mit einer methode überprüfen oder bei beiden .strip() benutzen
            await embe.update_scores(match)
            leaderboard_channel = client.get_channel(1256976133254152346)
            await embe.update_leaderboard_message(leaderboard_channel)
            

    return test_loop




@client.command(name='test1234')
async def test1234(ctx):
    #match = emma.get_next_match()
    # await ctx.send(match.ergebnis.split(":")[0])
    # await ctx.send(match.ergebnis.split(":")[1])
    # await ctx.send("test"+match.ergebnis.split(":")[0]+"test")
    # await ctx.send("test"+match.ergebnis.split(":")[1]+"test")
    # await ctx.send("test"+match.ergebnis.replace(" ","")+"test")
    #await ctx.send(int(match.ergebnis.replace(" ","").split(":")[0]))
    #torre1 = match.ergebnis.replace(" ","").split(":")[0]
    #tore1 = int(torre1)
    #torre2 = match.ergebnis.replace(" ","").split(":")[1]
    #tore2 = int(torre2)
    
    #await ctx.send(tore1)
    #await ctx.send(tore2) #versucht bindestrick in int umzuwandeln, geht nicht aber würde gehen
    ergebnis = "2 : 1"
    zore1 = int(ergebnis.replace(" ","").split(":")[0])
    zore2 = int(ergebnis.replace(" ","").split(":")[1])
    await ctx.send(zore1)
    await ctx.send(zore2)
    await ctx.send("test{}test{}test".format(zore1,zore2))
    await ctx.send(zore1+zore2)



    #await ctx.send("test{}test".format(int(match.ergebnis.replace(" ","").split(":")[0])))
    #await ctx.send("test{}test".format(int(match.ergebnis.replace(" ","").split(":")[1])))
     #print("test"+emdt.get_date_now_str()+"test")
    #print("test"+"29.06.2024"+"test")
    
    # match = emma.get_next_match()
    # print("AB HIER")
    
    # print(match.land1)
    # print(match.land2)
    # print(match.datum)
    # print(match.uhrzeit)
    # print(match.ergebnis)
    
    # print(emma.get_next_match_fake())
    
    #DER FEHLER IST IN DER DEFINITION DES MATCHES, ER ZÄHLT DIE ZEICHEN VON RECHTS ODER SO, HAB DEN STRING GEÄNDERT UND JETZT STEHT DA " vs.  | " STATT "18:00" ODER SOWAS
    























@client.command(name='updateleaderboard')
async def update_leaderboard_message(ctx):
    await embe.update_leaderboard_message(ctx)



































# Aufgabe, die jede Minute ausgeführt wird
# @tasks.loop(minutes=1)
# async def bets_loop():
    



#async def 





        
    
    #await channel.send("test funktioniert")
    






    #message = emdt.get_date_now_str() + " " + emdt.get_time_now()
    #match = emma.get_next_match_fake()
    #land1 = match.land1
    #land2 = match.land2


    #await ctx.send(land1 + land2)   
    #print(message)


    

    
    #a = "15:41"
    #b = a.replace(":","")
    #c = int(b)
    #print(c)
    #await ctx.send(c)



keep_alive()

client.run(TOKEN)
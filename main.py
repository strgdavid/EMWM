import asyncio
import datetime
import discord
import random
import json
import os

from discord.flags import Intents

from webserver import keep_alive
from discord.ext import commands, tasks


from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_SECRET')

client =  commands.Bot(command_prefix=commands.when_mentioned_or("?"), help_command=None, intents=discord.Intents.all())
client.remove_command('help')

#client = discord.Client()
prefix = "?"
status_value = "test"
status_1 = True

@client.event
async def on_ready():
    print(f"{client.user.name} is online")
    print(f"id: {client.user.id}")

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
  await ctx.send('https://tenor.com/view/emirmono-mittelfinger-gif-791195104924975174')




keep_alive()

client.run(TOKEN)
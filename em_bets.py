import discord
from discord.ext import commands, tasks

import em_datetime as emdt
import em_matches as emma
import os

sent_message_ids = []


async def open_bets_bool():
  next_match = emma.get_next_match()
  time_now_packed = emdt.get_time_now_packed()
  next_match_time_packed = int(next_match.uhrzeit.replace(":", ""))
  
  if next_match_time_packed - time_now_packed < 100:
    open_bets_bool = True
    return open_bets_bool
  else:
    open_bets_bool = False
    return open_bets_bool

async def open_bets(client, match):
    land1 = match.land1
    land2 = match.land2
    #land1 = emma.get_next_match().land1
    #land2 = emma.get_next_match().land2

    land1flagge = match.land1+"_flagge"
    land2flagge = match.land2+"_flagge"
    #land1flagge = emma.get_next_match().land1+"_flagge"
    #land2flagge = emma.get_next_match().land2+"_flagge"


    

    #print(land1flagge)
    #print(land2flagge)
    
    embed1 = discord.Embed(
        description="# "+land1,
        color=16777215)
    embed1.set_footer(
        text="Wie viele Tore?",
        icon_url="https://www.flyeralarm-sports.com/bilder/kk_dropper_uploads/IQ3682_1_HARDWARE_Photography_Front_Center_View_transparent.png")
    embed1.set_thumbnail(
        url=os.getenv(land1flagge))

    embed2 = discord.Embed(
        description="# "+land2,
        color=16777215)
    embed2.set_footer(
        text="Wie viele Tore?",
        icon_url="https://www.flyeralarm-sports.com/bilder/kk_dropper_uploads/IQ3682_1_HARDWARE_Photography_Front_Center_View_transparent.png")
        
    embed2.set_thumbnail(
        url=os.getenv(land2flagge))

    print(land1flagge)
    

    # Nachrichten erstellen
    #msg_de = await ctx.send(land1)
    #msg_fr = await ctx.send(land2)

    channel = client.get_channel(1255542883243659436) 
    
    message1 = "# {}: {} vs. {} | {}".format(match.datum, match.land1, match.land2, match.uhrzeit)
    msg1 = await channel.send(message1)
    msg_de = await channel.send(embed=embed1)
    msg_fr = await channel.send(embed=embed2)

    sent_message_ids.append(msg1.id)
    sent_message_ids.append(msg_de.id)
    sent_message_ids.append(msg_fr.id)

    # Emojis hinzufügen
    emojis = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']
    for emoji in emojis:
        await msg_de.add_reaction(emoji)
        await msg_fr.add_reaction(emoji)


# async def clear_message(ctx):
#   land1 = emma.get_next_match_fake().land1
#   land2 = emma.get_next_match_fake().land2

#   if ctx.author.id != 759391893863399444:
#     await ctx.send("Du hast keine Berechtigung, diesen Befehl auszuführen.")
#     return

#   # Nachrichten löschen
#   await ctx.message.delete()
#   async for message in ctx.history(limit=200):  # Anzahl der zu löschenden Nachrichten anpassen
#     if message.content == land1 or message.content == land2:
#         await message.delete()

async def clear_bets(ctx, client):
    channel = client.get_channel(1255542883243659436)
    if channel is None:
        await ctx.send("Channel not found.")
        return

    for message_id in sent_message_ids:
        try:
            msg = await channel.fetch_message(message_id)
            await msg.delete()
        except discord.NotFound:
            print(f"Message with ID {message_id} not found.")
        except discord.Forbidden:
            print(f"Do not have permissions to delete message with ID {message_id}.")
        except discord.HTTPException as e:
            print(f"Failed to delete message with ID {message_id}: {e}")

    # Clear the list after deleting messages
    sent_message_ids.clear()


async def clear_txt(ctx):
  if ctx.author.id != 759391893863399444:
    await ctx.send("Du hast keine Berechtigung, diesen Befehl auszuführen.")
    return
  # Daten in der reaktionen.txt löschen
  filename = 'reaktionen.txt'
  with open(filename, 'w'):
      pass  # Datei leeren

  await ctx.send("Alle Daten in der reaktionen.txt wurden gelöscht.")


async def on_reaction_add(reaction, user):
    land1 = emma.get_next_match().land1
    land2 = emma.get_next_match().land2

    if user.bot:  # Ignoriere Reaktionen von Bots
      return

  # Überprüfen, ob der Nutzer bereits eine Reaktion auf diese Nachricht hinterlassen hat
    existing_reactions = [r for r in reaction.message.reactions if str(r.emoji) in ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']]
    for r in existing_reactions:
        async for u in r.users():
            if u == user and r != reaction:
                await reaction.message.remove_reaction(r.emoji, user)

  # Entscheiden, ob die Reaktion auf Deutschland oder Frankreich ist und die entsprechende Aktion ausführen
  # if reaction.message.content == land1:
  #     await process_reaction(reaction, user, land1) #ANPASSEN AUF DIE DISCORD EMBED
  # elif reaction.message.content == land2:
  #     await process_reaction(reaction, user, land2)
    if land1 in reaction.message.embeds[0].description:
        await process_reaction(reaction, user, land1)
    elif land2 in reaction.message.embeds[0].description:
        await process_reaction(reaction, user, land2)

async def process_reaction(reaction, user, country):
  # Datei öffnen und Daten verarbeiten
  filename = 'reaktionen.txt'
  with open(filename, 'r') as f:
      lines = f.readlines()

  # Daten neu schreiben
  updated_data = []
  found_country = False
  for line in lines:
      if line.strip():
          parts = line.strip().split(':')
          if parts[0].startswith(f"{user.name}({user.id})"):
              # Nutzer gefunden, prüfe und aktualisiere die Zeile
              if parts[1].startswith(f"{country}."):
                  # Aktualisiere bestehende Zeile mit neuer Reaktion
                  updated_data.append(f"{user.name}({user.id}):{country}.{reaction.emoji[0]}")
                  found_country = True
              else:
                  # Behalte bestehende Zeile bei, da sie nicht für das aktuelle Land ist
                  updated_data.append(line.strip())
          else:
              # Behalte bestehende Zeilen bei
              updated_data.append(line.strip())

  # Falls für das Land des Nutzers noch keine Zeile existiert, füge eine neue hinzu
  if not found_country:
      updated_data.append(f"{user.name}({user.id}):{country}.{reaction.emoji[0]}")

  # In Datei schreiben
  with open(filename, 'w') as f:
      f.write('\n'.join(updated_data))

  # Alte Reaktionen des Nutzers entfernen
  for existing_reaction in reaction.message.reactions:
      async for u in existing_reaction.users():
          if user == u:
              await reaction.message.remove_reaction(existing_reaction.emoji, user)



async def update_scores(match):
    filename = 'reaktionen.txt'
    leaderboard_filename = 'leaderboard.txt'

    land1 = match.land1
    land2 = match.land2

    
    #land1 = emma.get_next_match().land1
    #land2 = emma.get_next_match().land2
    
    #deutschland_tore = 2
    #frankreich_tore = 1

    #land1_tore = 2 #BRAUCHE EINE METHODE DIE DAS LETZTE MATCH ABSPEICHERT UND DANN MUSS ICH DIE TORE HIER EINFÜGEN MIT SPLIT ":"
    #land2_tore = 1

    
    
    land1_tore = match.ergebnis.replace(" ","").split(":")[0] #############HIERRRRRRRR
    land2_tore = match.ergebnis.replace(" ","").split(":")[1]

    with open(filename, 'r') as f:
        lines = f.readlines()

    points_to_add = {}
    for line in lines:
        if line.strip():
            parts = line.strip().split(':')
            user_info = parts[0]
            country_bet = parts[1].split('.')
            country = country_bet[0]
            bet = int(country_bet[1])

            if user_info not in points_to_add:
                points_to_add[user_info] = {land1: -1, land2: -1}

            points_to_add[user_info][country] = bet

    for user, bets in points_to_add.items():
        points_to_add[user] = 0


        # ergebnis = 2:1
        # 10 pkt: ergebnis komplett richtg
        # 5 pkt: sieg richtig
        # 5 pkt: nur von einer seite tore richtig
        
        #exaktes ergebnis: +1
        if bets[land1] == land1_tore and bets[land2] == land2_tore:
            points_to_add[user] = points_to_add[user]+1

        #land1_tore richtig: +1
        if bets[land1] == land1_tore:
            points_to_add[user] = points_to_add[user]+1

        #land2_tore richtig: +1
        if bets[land2] == land2_tore:
            points_to_add[user] = points_to_add[user]+1
            

        #land1 sieg richtig: +1
        if bets[land1] > bets[land2] and land1_tore > land2_tore:
            points_to_add[user] = points_to_add[user]+1

        #land2 sieg richtig: +1
        if bets[land2] > bets[land1] and land2_tore > land1_tore:
            points_to_add[user] = points_to_add[user]+1

        
        #tor verhältnis richtig (3:2, 2:1, 1:0): +1
        land1_tore_while = land1_tore
        land2_tore_while = land2_tore
        while land1_tore_while >= 0 and land2_tore_while >= 0:
            if land1_tore_while == land1_tore and land2_tore_while == land2_tore:
                points_to_add[user] = points_to_add[user]+1
                break
            else:
                land1_tore_while = land1_tore_while - 1
                land2_tore_while = land2_tore_while - 1


    
        # else:
        #     points_to_add[user] = 0

    with open(leaderboard_filename, 'r') as f:
        leaderboard_lines = f.readlines()

    leaderboard_dict = {}
    for line in leaderboard_lines:
        if line.strip():
            parts = line.strip().split(':')
            user_info = parts[0]
            points = int(parts[1])
            leaderboard_dict[user_info] = points

    for user in points_to_add:
        if user not in leaderboard_dict:
            leaderboard_dict[user] = 0

    for user, points in points_to_add.items():
        leaderboard_dict[user] += points

    updated_leaderboard = [f"{user_info}:{points}" for user_info, points in leaderboard_dict.items()]

    with open(leaderboard_filename, 'w') as f:
        f.write('\n'.join(updated_leaderboard))

    print("Punkte wurden basierend auf den Wetten aktualisiert.")




async def update_leaderboard_message(ctx_or_channel):
    filename = 'leaderboard.txt'
    leaderboard_message_filename = 'leaderboard_message.txt'

    with open(filename, 'r') as f:
        lines = f.readlines()

    leaderboard = []
    for line in lines:
        if line.strip():
            parts = line.strip().split(':')
            user_info = parts[0]
            points = int(parts[1])
            leaderboard.append((user_info, points))

    leaderboard.sort(key=lambda x: x[1], reverse=True)

    with open(leaderboard_message_filename, 'w') as f:
        for i, (user_info, points) in enumerate(leaderboard, start=1):
            username = user_info.split('(')[0]
            f.write(f"{i}. {username} | {points}\n")

    ranks = [f"{i}." for i in range(1, len(leaderboard) + 1)]
    names = [user_info.split('(')[0] for user_info, _ in leaderboard]
    scores = [str(points) for _, points in leaderboard]

    leaderboard_embed = discord.Embed(title="LEADERBOARD", color=discord.Color.blue())
    leaderboard_embed.add_field(name="Platz", value="\n".join(ranks), inline=True)
    leaderboard_embed.add_field(name="Spieler", value="\n".join(names), inline=True)
    leaderboard_embed.add_field(name="Punkte", value="\n".join(scores), inline=True)

    if isinstance(ctx_or_channel, discord.ext.commands.Context):
        await ctx_or_channel.send("**# LEADERBOARD**", embed=leaderboard_embed)
    else:
        await ctx_or_channel.send("**# LEADERBOARD**", embed=leaderboard_embed)


    
    
  # with open("bets.json", "r") as f:
  #   bets = json.load(f)
  # return bets

  #schauen, welche matches heute gespielt werden.
  #schauen, ob das nächste match in den nächsten x stunden gespielt wird.
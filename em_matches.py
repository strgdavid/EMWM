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

import em_datetime as emdt
from webserver import keep_alive


class MatchObj:
  def __init__(self, land1, land2, datum, uhrzeit, ergebnis):
      self.land1 = land1
      self.land2 = land2
      self.datum = datum
      self.uhrzeit = uhrzeit
      self.ergebnis = ergebnis

  def __repr__(self):
    return f"Match({self.land1} vs {self.land2} on {self.datum} at {self.uhrzeit})"

  def __str__(self):
    #return f"{self.land1} vs. {self.land2} | {self.datum}  {self.uhrzeit}"
    return f"{self.land1} {self.land2} {self.datum} {self.uhrzeit} {self.ergebnis}"





def get_spieltag_matches():
  #date_now_str = emdt.get_date_now_str()
  
    #temporär achtel

  if (datetime.datetime(2024, 6, 27) <= datetime.datetime.now() <= datetime.datetime(2024, 7, 2)): #achtel
    url = 'https://www.dfb.de/maenner-nationalmannschaft/turniere/europameisterschaften/euro-spielplan/?no_cache=1&spieledb_path=%2Fde%2Fcompetitions%2Feuropameisterschaft%2Fseasons%2F2024-in-deutschland%2Fmatchday%2Fachtelfinale'
  elif (datetime.datetime(2024, 7, 3) <= datetime.datetime.now() <= datetime.datetime(2024, 7, 6)): #viertel
    url = 'https://www.dfb.de/maenner-nationalmannschaft/turniere/europameisterschaften/euro-spielplan/?no_cache=1&spieledb_path=%2Fde%2Fcompetitions%2Feuropameisterschaft%2Fseasons%2F2024-in-deutschland%2Fmatchday%2Fviertelfinale'
  elif (datetime.datetime(2024, 7, 7) <= datetime.datetime.now() <= datetime.datetime(2024, 7, 10)): #halb
    url = 'https://www.dfb.de/maenner-nationalmannschaft/turniere/europameisterschaften/euro-spielplan/?no_cache=1&spieledb_path=%2Fde%2Fcompetitions%2Feuropameisterschaft%2Fseasons%2F2024-in-deutschland%2Fmatchday%2Fhalbfinale'
  elif (datetime.datetime(2024, 7, 11) <= datetime.datetime.now() <= datetime.datetime(2024, 7, 14)):
    url = 'https://www.dfb.de/maenner-nationalmannschaft/turniere/europameisterschaften/euro-spielplan/?no_cache=1&spieledb_path=%2Fde%2Fcompetitions%2Feuropameisterschaft%2Fseasons%2F2024-in-deutschland%2Fmatchday%2Ffinale'
  else:
    url = 'https://www.dfb.de/maenner-nationalmannschaft/turniere/europameisterschaften/euro-spielplan/?no_cache=1&spieledb_path=%2Fde%2Fcompetitions%2Feuropameisterschaft%2Fseasons%2F2024-in-deutschland%2Fmatchday%2Fachtelfinale'
    
       
  #print(url)
  html = requests.get(url)

  s = BeautifulSoup(html.content, 'html.parser')

  matches = s.find_all('tr', id=re.compile(r'^match_'))

  matchObj_list = []
  #for match in matches:
  for match in matches:
    #datum = match.find(class_='column-date').text
    #print(datum)
    #print(match)
    
    land1 = match.find(class_='column-team-title text-right hidden-xs').text.strip()
    #print(land1)
    
    land2 = match.find(class_='column-team-title text-left hidden-xs').text.strip()
    #print(land2)
    
    datum = match.find(class_='column-date').text.strip()[-19:-9]
    #print(datum)
    
    uhrzeit = match.find(class_='column-date').text.strip()[-9:-4]
    #print(uhrzeit)
    
    try:
      ergebnis = match.find(class_='column-score').text.strip()
    except AttributeError:
      ergebnis = "-:-"

    #print(ergebnis+"\n")
    next_matchObj = MatchObj(land1, land2, datum, uhrzeit, ergebnis)
    matchObj_list.append(next_matchObj)

  return matchObj_list

def get_matches_today():
  matchObj_list = get_spieltag_matches()
  matches_today = []
  for match in matchObj_list:
    if match.datum == emdt.get_date_now_str():
      matches_today.append(match)
  return matches_today #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

def get_next_match():
  matches_today = get_matches_today()

  #return_match = MatchObj()
  return_match = MatchObj("","","","","")
  dtime = 0
  #time_now_packed = emdt.get_time_now_packed()

  for match in matches_today:
    time_now_packed = emdt.get_time_now_packed()
    #time_now_packed = emdt.get_time_now_packed()
    time_match_packed = int(match.uhrzeit.replace(":",""))

    #print(match)
    #print(time_now_packed)
    #print(time_match_packed)
    #print("{}\n".format(time_match_packed-time_now_packed))

    if time_now_packed < time_match_packed:
      #print("match in zukunft")
      if dtime != 0:
        #print("dtime bereits berührt")
        if time_match_packed-time_now_packed<dtime:
          #print("neue kürzeste dtime")
          dtime = time_match_packed-time_now_packed
          return_match = match
          #print("vergleichen mit dtime, wenn kleiner dann match = neueres match")
      else:
        #print("dtime war bis jetzt unberührt, neue dtime deswegen")
        dtime = time_match_packed-time_now_packed
        return_match = match
  return return_match


def get_next_match_fake():
  matches_today = get_matches_today()
      
  #return_match = MatchObj()
  return_match = MatchObj("","","","","")
  dtime = 0
  #time_now_packed = emdt.get_time_now_packed()
  
  for match in matches_today:
    time_now_packed = emdt.get_time_now_packed()
    #time_now_packed = emdt.get_time_now_packed()
    time_match_packed = int(match.uhrzeit.replace(":",""))

    #print(match)
    #print(time_now_packed)
    #print(time_match_packed)
    #print("{}\n".format(time_match_packed-time_now_packed))
    
    if time_now_packed < time_match_packed:
      #print("match in zukunft")
      if dtime != 0:
        #print("dtime bereits berührt")
        if time_match_packed-time_now_packed<dtime:
          #print("neue kürzeste dtime")
          dtime = time_match_packed-time_now_packed
          return_match = match
          #print("vergleichen mit dtime, wenn kleiner dann match = neueres match")
      else:
        #print("dtime war bis jetzt unberührt, neue dtime deswegen")
        dtime = time_match_packed-time_now_packed
        return_match = match
  return return_match
        
  #try:
  #  return return_match
  #except:
  #  return MatchObj("","","","","")
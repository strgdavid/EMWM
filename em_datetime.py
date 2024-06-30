import datetime

import pytz


def get_time_now(): #string
  time_now = datetime.datetime.today().astimezone(pytz.timezone('Europe/Berlin'))
  return time_now.strftime("%H:%M")

def get_time_now_packed(): #int ohne :
  return int(get_time_now().replace(":",""))

def get_date_now(): #date
  return datetime.date.today()

def get_date_now_str(): #string
  return datetime.date.today().strftime('%d.%m.%Y')

  
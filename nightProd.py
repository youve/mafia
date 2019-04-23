#!/usr/bin/python3
# Prod timers continue overnight

import requests
import argparse
import datetime
import sys
try:
    from bs4 import BeautifulSoup
except ModuleNotFoundError:
    print("This script requires the Beautiful Soup library version 4. Get it here: https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup")
    sys.exit()

def parse_page(url):
    res = requests.get(url)
    res.raise_for_status()
    return BeautifulSoup(res.text, "html.parser")

def prod_when(start, vla=False):
    frequency = args.frequency*60*60
    now = datetime.datetime.now()
    if now.month == 1 and start.startswith('Dec'):
        now -= datetime.timedelta(days=40)
    prod = datetime.datetime.strptime(str(now.year) + start, '%Y%b %d, %I:%M%p')
    if vla:
        nudge = prod + datetime.timedelta(hours=args.frequency*1.5)
        nudge += datetime.timedelta(hours=args.night)
    else:
        nudge = datetime.datetime(1,1,1)
    while prod.weekday() < 5 and frequency >= 1: # weekday
        prod = prod + datetime.timedelta(seconds=1)
        frequency -=1
    while prod.weekday() > 4 and frequency >= 1: #Time passes more slowly on the weekends
        prod = prod + datetime.timedelta(seconds=2)
        frequency -=1
    while prod.weekday() < 5 and frequency >= 1: #weekday
        prod = prod + datetime.timedelta(seconds=1)
        frequency -=1
    prod += datetime.timedelta(hours=args.night)
    if nudge > prod:
        return nudge.strftime("nudge at [countdown]%F %T[/countdown]")
    else:
        return prod.strftime("prod at [countdown]%F %T[/countdown]")

parser = argparse.ArgumentParser(description='Determine when next prod is due.')
parser.add_argument('-f', '--frequency', type=int, help="Frequency. Default: 36",
    default=36, nargs='?')
parser.add_argument('-n', '--night', help='Night duration in hours.', type=int,
    nargs='?', default=48)
parser.add_argument('url', help='Game url', type=str)

args = parser.parse_args()

overview_url = args.url + '&activity_overview=1'
home_url = args.url + '&ppp=5'

#Find players
home = parse_page(home_url)
players = {}
for fieldset in home.select('fieldset'):
    if fieldset.text.startswith('Living Players'):
        for player in fieldset.strings:
            if player != "Living Players":
                players[player.split('(')[0].strip()] = ''

#Find last activity
activity = parse_page(overview_url)
times = []
for div in activity.select('span'):
    for s in div.strings:
        if s.strip():
            times.append(s.strip())

for player in players:
    last_post = times[times.index(player) + 2]

    if times.index(player) + 5 >= len(times): # last in the list not vla
        players[player] = prod_when(last_post)
    elif times[times.index(player) + 5] in players: # not vla
        players[player] = prod_when(last_post)
    else: # vla
        players[player] = prod_when(last_post, vla=True)

    print(f'[b]{player}[/b]: {players[player]}')

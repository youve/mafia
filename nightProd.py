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

def spin_clock(prod, frequency):
    while frequency >= 1:
        while prod.weekday() < 5 and frequency >= 1: # weekday
            prod = prod + datetime.timedelta(seconds=1)
            frequency -=1
        while prod.weekday() > 4 and frequency >= 1:
            # Time passes more slowly on the weekends
            prod = prod + datetime.timedelta(seconds=2)
            frequency -=1
    return prod

def prod_when(start, vla=False):
    frequency = args.frequency*60*60
    now = datetime.datetime.now()
    daystart = datetime.datetime.strptime(str(now.year) + times[9], '%Y%b %d, %I:%M%p')
    daystart += datetime.timedelta(hours=args.night)
    if now.month == 1 and start.startswith('Dec'):
        now -= datetime.timedelta(days=40)
    start = datetime.datetime.strptime(str(now.year) + start, '%Y%b %d, %I:%M%p')
    prod = start
    if vla:
        nudge = start + datetime.timedelta(hours=args.frequency*1.5)
        nudge += datetime.timedelta(hours=args.night)
    else:
        nudge = datetime.datetime(1,1,1)

    prod = spin_clock(prod, frequency)

    prod += datetime.timedelta(hours=args.night)

    if not vla and prod < daystart:
        prod -= datetime.timedelta(hours=args.night)
        prod = spin_clock(prod, 24*60*60)
        prod += datetime.timedelta(hours=args.night)
        return prod.strftime(f"replace at [countdown]%F %T {tz}[/countdown]")
    if vla and nudge < daystart:
        nudge += datetime.timedelta(hours=args.frequency*1.5)
        replace = start + datetime.timedelta(days=5, hours=args.night)
        return nudge.strftime(f"Two nudges = a prod at [countdown]%F %T {tz}[/countdown]") + \
            replace.strftime(f" or replace at [countdown]%F %T {tz}[/countdown]")
    if nudge > prod:
        return nudge.strftime(f"nudge at [countdown]%F %T {tz}[/countdown]")
    else:
        return prod.strftime(f"prod at [countdown]%F %T {tz}[/countdown]")

parser = argparse.ArgumentParser(description='Determine when next prod is due.')
parser.add_argument('-f', '--frequency', type=int, help="Frequency. Default: 36",
    default=36, nargs='?')
parser.add_argument('-n', '--night', help='Night duration in hours. Default: 48',
    type=int, nargs='?', default=48)
parser.add_argument('url', help='Game url', type=str)

args = parser.parse_args()

overview_url = args.url + '&activity_overview=1'
home_url = args.url + '&ppp=5'

#Find players
home = parse_page(home_url)
if home.abbr.text == 'DST':
    tz = '-5.00'
else:
    tz = '-6.00'

players = []
for fieldset in home.select('fieldset'):
    if fieldset.text.startswith('Living Players'):
        for player in fieldset.strings:
            if player != "Living Players":
                players.append(player.split('(')[0].strip())

#Find last activity
activity = parse_page(overview_url)
times = []
for div in activity.select('span'):
    for s in div.strings:
        if s.strip():
            times.append(s.strip())

for player in players:
    if player not in times:
        print(f'[b]{player}[/b] never posted in the game!')
        continue

    last_post = times[times.index(player) + 2]
    vla = False
    try:
        datetime.datetime.strptime(times[times.index(player) + 5], '%B %d %Y')
        vla = True
    except:
        pass

    if vla:
        print(f'[b]{player}[/b]: {prod_when(last_post, vla=True)}')
    else:
        print(f'[b]{player}[/b]: {prod_when(last_post)}')

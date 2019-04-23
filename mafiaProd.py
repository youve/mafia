#!/usr/bin/python3
# When to prod a player
# Time passes more slowly on the weekends.

import argparse
import datetime
import re

parser = argparse.ArgumentParser(description='Determine when next prod is due.')
parser.add_argument('time', type=str, help="HH:MM")
parser.add_argument('-f', '--frequency', type=int, help="Frequency. Default: 36",
    default=36, nargs='?')
parser.add_argument('-v', '--vla', action='store_true', help='Are they V/LA?')
parser.add_argument('-e', '--emoji', type=str, help="emoji", nargs='?', default='🌐')
parser.add_argument('-c', '--countdown', help='Output in countdown format',  action="store_true")

args = parser.parse_args()

ydayRegex = re.compile('\s\(\d+\+1\)') # get rid of day of the year
if re.search(ydayRegex, args.time):
    args.time = re.sub(ydayRegex, '', args.time)

prod = datetime.datetime.strptime(args.time, "%Y.%m.%d %H:%M:%S")
nudge = False

frequency = args.frequency*60*60
if args.vla: # if player is on a leave of absence they get nudged slower but they don't get
    #slower weekends
    nudge = prod + datetime.timedelta(hours=args.frequency*1.5)
else:
    nudge = datetime.datetime(1,1,1) # prod will never be bigger than this
while prod.weekday() < 5 and frequency >= 1: # weekday
    prod = prod + datetime.timedelta(seconds=1)
    frequency -=1
while prod.weekday() > 4 and frequency >= 1: #Time passes more slowly on the weekends
    prod = prod + datetime.timedelta(seconds=2)
    frequency -=1
while prod.weekday() < 5 and frequency >= 1: #weekday
    prod = prod + datetime.timedelta(seconds=1)
    frequency -=1

if args.countdown:
    if nudge > prod:
        print(nudge.strftime("nudge at [countdown]%F %T[/countdown]"))
    else:
        print(prod.strftime("prod at [countdown]%F %T[/countdown]"))
else:
    if nudge > prod: # player is on leave of absence gets more time
        print(nudge.strftime('%j %H:%M'), args.emoji, 'nudge ')
    else:
        print(prod.strftime('%j %H:%M'), args.emoji, 'prod ')

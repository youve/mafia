#!/usr/bin/python3
# mafiaDeadlines.py
# usage:
# ./mafiaDeadlines.py "2018 09:30:00" 10 >> ../schedule/files/main

import argparse
import datetime
import re

parser = argparse.ArgumentParser(description='Deadline sizes')
parser.add_argument('start', metavar='start', type=str, default=datetime.datetime.now(),
                    help='%Y %j %H:%M')
parser.add_argument('length', metavar='length', type=int, nargs='?', default=10,
                    help='length of the dayphase')
parser.add_argument('emoji', metavar='emoji', type=str, help="emoji", nargs='?', default='🌐')

args = parser.parse_args()

yearRegex = re.compile("^\d{4}")
if yearRegex.search(args.start): # I remembered to put the year in
    start = datetime.datetime.strptime(args.start, '%Y %j %H:%M')
else: # I forgot to put the year in
    start =  datetime.datetime.strptime(str(datetime.datetime.today().year) + ' ' + args.start, '%Y %j %H:%M')

delta = datetime.timedelta(days=(args.length-1)/20)
emoji = args.emoji

#print the times to update the deadline size in a format `main` can understand
for i in range(1,21):
    print((start + delta*i).strftime('%j %H:%M'), emoji, 'dl', 100+5*i)
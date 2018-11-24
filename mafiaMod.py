#!/usr/bin/python3
# Mod a newbie game

import logging
#logging.disable()
import argparse
import sys
import random
import pprint
from selenium import webdriver
from selenium.webdriver.common.keys import Keys    
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logging.basicConfig(filename='log-mafiaMod.txt', level=logging.DEBUG, format='
%(asctime)s - %(levelname)s - %(message)s')
logging.debug("Start of program.")

#TODO: set these variables: PUBLICTHREAD, MAFIATHREAD, MODTHREAD, DEADTHREAD, ICTHREAD, GAMENUMBER, GAMETITLE, NUMBEREDPLAYERLIST, PLAYERLIST, LINK, TITLE, EXPLANATION, DESCRIPTION]

setups = {
    'A1' : ['mafia roleblocker', 'mafia goon', 'town cop', 'town neapolitan'] + ['vanilla townie'] * 5,
    'A2' : ['mafia roleblocker', 'mafia goon', 'town jailkeeper', 'town doctor'] + ['vanilla townie'] * 5,
    'A3' : ['mafia roleblocker', 'mafia goon', 'town cop', 'town doctor'] + ['vanilla townie'] * 5,
    'B1' : ['mafia rolecop', 'mafia goon', 'town cop', 'town tracker'] + ['vanilla townie'] * 5,
    'B2' : ['mafia rolecop', 'mafia goon', 'town jailkeeper', 'town tracker'] + ['vanilla townie'] * 5,
    'B3' : ['mafia rolecop', 'mafia goon', 'town neapolitan', 'town doctor'] + ['vanilla townie'] * 5,
    'C1' : ['mafia goon', 'mafia goon', 'town cop'] + ['vanilla townie'] * 6,
    'C2' : ['mafia goon', 'mafia goon', 'town jailkeeper'] + ['vanilla townie'] * 6,
    'C3' : ['mafia goon', 'mafia goon', 'town tracker', 'town doctor'] + ['vanilla townie'] * 5,
}

parser = argparse.ArgumentParser(description='Setup a newbie game.')
parser.add_argument('setup', metavar='setup', type=str, choices=setups.keys(),
                    help='Have the playerlist copied and ready to go.')
parser.add_argument('number', metavar='gamenumber', type=int, help="Game number")
parser.add_argument('title', metavar="gametitle", type=str, help="Name of the theme")
parser.add_argument('totalPlayers', metavar="totalPlayers", type=int, help="How many players", nargs='?', default=9)

args = parser.parse_args()
#args = parser.parse_args(['A1', '1900', 'Popcorn'])
logging.info(f"args: {args}")

players = []
if not args.number:
    args.number = input("Enter your game number: ")
if not args.title:
    args.title = input("Enter your game title: ")

try: // try to get playerlist from clipboard
    import pyperclip
    players = list(pyperclip.paste().split('\n'))
except ModuleNotFoundError:
    print('pyperclip module not found. Get it from https://pypi.org but you can use ctrl-v to paste. ')

if len(players) != args.totalPlayers:
    logging.debug(f"{len(players)} is not enough players: {', '.join(players)}")
    players = []
    print("Paste the players here, then hit enter: ")

while len(players) < args.totalPlayers:
    players.append(sys.stdin.readline().strip())

logging.debug(f"Playerlist: {', '.join(players)}")

NUMBEREDPLAYERLIST = []
PLAYERLIST = []
ICPLAYER = ""

for i, player in enumerate(players):
    NUMBEREDPLAYERLIST.append(f"{i+1}) {player}")
    if i == 8:
        PLAYERLIST.append(player.replace(' (IC)', ''))
        ICPLAYER = player
    else:
        PLAYERLIST.append(player.replace(' (SE)', ''))

shuffledPlayers = players[:]
random.shuffle(shuffledPlayers)

#assign roles
roles = dict(zip(shuffledPlayers,setups[setup]))

for role in roles:
    print(role[0], ':', role[1]) #mafia goon : player1

#TODO: set these variables: PUBLICTHREAD, MAFIATHREAD, MODTHREAD, DEADTHREAD, ICTHREAD, LINK, TITLE, EXPLANATION, DESCRIPTION]

def makeOP(whichThread):
    print(f"Making {whichThread} thread")
    browser = webdriver.Firefox()
    if whichThread == 'public':
        browser.get('https://forum.mafiascum.net/posting.php?mode=post&f=11')
    else:
        browser.get('https://forum.mafiascum.net/posting.php?mode=post&f=90')
    if "Login" in browser.title:
        elem = browser.find_element_by_name("username")
        elem.clear()
        elem.send_keys("Plotinus")
        elem = browser.find_element_by_name('autologin')
        elem.click()
        elem = browser.find_element_by_name('viewonline')
        elem.click()
        elem = browser.find_element_by_name("password")
        elem.clear()
        input("Type your password in the browser and then hit return here when you're done")
    element = WebDriverWait(browser, 10).until(EC.title_contains('new topic'))
    elem = browser.find_element_by_name("subject")
    elem.clear()
    elem.send_keys(f"Newbie {args.number} | {args.title.title()} | {whichPT.title()}")
    elem.clear()
    elem = browser.find_element_by_name("message")
    post = readFile(whichThread, 0)
    for line in post:
        elem.send_keys(line)
    return browser.current_url

def readFile(folder, file): #may need more replacements as more files added
    abspath = os.path.abspath(__file__)
    fileDirectory = os.path.dirname(abspath) + '/files/' + folder + '/'
    with open(folder + file, 'r') as f:
        post = list(f)
    for line in post:
        line = line.replace('GAMENUMBER', args.number)
        line = line.replace('GAMETITLE', args.title)
        line = line.replace('PUBLICTHREAD', PUBLICTHREAD)
        line = line.replace('MAFIATHREAD', MAFIATHREAD)
        line = line.replace('ICTHREAD', ICTHREAD)
        line = line.replace('DEADTHREAD', DEADTHREAD)
        line = line.replace('MODTHREAD', MODTHREAD)
        line = line.replace('DESCRIPTION', DESCRIPTION)
        line = line.replace('NUMBEREDPLAYERLIST', NUMBEREDPLAYERLIST.join('\n'))
        line = line.replace('PLAYERLIST', PLAYERLIST.join('\n'))
        line = line.replace('ROLES', pprint.pformat(roles))
        line = line.replace('EVENTS', EVENTS)
        line = line.replace('YOUTUBE', YOUTUBE)
        line = line.replace('DEADPICTURE', DEADPICTURE)
        line = line.replace('DEADTEXT', DEADTEXT)
        line = line.replace('DEADLINK', DEADLINK)
        line = line.replace('DEADTITLE', DEADTITLE)
        line = line.replace('ICPLAYER', ICPLAYER)
        line = line.replace('ICPICTURE', ICPICTURE)
        line = line.replace('ICTEXT', ICTEXT)
        line = line.replace('ICLINK', ICLINK)
        line = line.replace('ICTITLE', ICTITLE)
    return post

def sendRolePM(recipient, role): #if player IC, link to IC thread
    print(f"Sending {recipient} their role")
    browser.get('https://forum.mafiascum.net/ucp.php?i=pm&mode=compose')
    elem = browser.find_element_by_name("username_list")
    elem.clear()
    elem.send_keys(recipient)
    elem = browser.find_element_by_name("subject")
    elem.clear()
    elem.send_keys(f"Newbie {args.number} | {args.title.title()} | Role PM")
    elem = browser.find_element_by_name("message")
    elem.clear()
    post = readFile('roles', role)
    for line in post:
        elem.send_keys(line) 
    elem.submit()
    elem = browser.find_element_by_name("post")
    elem.submit()

def makeGameDescription():
    DOINGWHAT = ''
    if "stuff i found online" in args.title.lower():
        DOINGWHAT = "showcasing cool stuff I found/learned about online via my RSS reader and maybe talking some about why I think it's cool. "
    elif "zoo" in args.title.lower():
        DOINGWHAT = "showing pictures of cute baby zoo animals. "
    elif "cake" in args.title.lower():
        DOINGWHAT = "showing pictures of failed cakes by professional bakers."
    elif "urw" in args.title.lower():
        DOINGWHAT = "[code]" + input("Output of `urwbot, start`: ") + "[/code]"
    else:
        DOINGWHAT = input('Hello. In this game I\'ll be _____')

    IMG = input('Upload an image: ')
    LINK = input('Link: ')
    TITLE = input('Title for link: ')
    EXPLANATION = input(f'Finish this sentence: Such as {TITLE}, ______')
    DESCRIPTION = """[center][thumb=600]{IMG}[/thumb][/center]\n
        \n
        Hello. In this game I'll be  {DOINGWHAT}
        Such as [url={LINK}]{TITLE}[/url]. {EXPLANATION}"""

    return DESCRIPTION

def gameEvents():
    event = "[area=day 1][list][*]___ is lynched with _ scum on ___ wagon.[/list][/area]\n\n"
    townActions = []
    mafiaActions = ['[*][color=red]___[/color] is killing [color=green]___[/color].\n']
    reminders = []
    for k, v in roles.items():
        if v == 'town cop':
            townActions.append(f'[*][color=green]{k}[/color] is copping [color=white]___[/color].\n')
            reminders.append('''Cop didn't submit your night actions:
                            [code]This is just a reminder that you have [countdown]1 day[/countdown] to figure out who you're going to investigate tonight, if anybody.[/code]''')
        elif v == 'town doctor':
            townActions.append(f'[*][color=green]{k}[/color] is protecting [color=white]___[/color].\n')
            reminders.append('''Doc didn't submit your night actions:
                            [code]This is just a reminder that you have [countdown]1 day[/countdown] to figure out who you're going to protect tonight, if anybody.[/code]''')
        elif v == 'town jailkeeper':
            townActions.append(f'[*][color=green]{k}[/color] is jailkeeping [color=white]___[/color].\n')
            reminders.append('''Jailkeeper didn't submit your night actions:
                            [code]This is just a reminder that you have [countdown]1 day[/countdown] to figure out who you're going to jailkeep tonight, if anybody.[/code]''')
        elif v == 'town neapolitan':
            townActions.append(f'[*][color=green]{k}[/color] is checking [color=white]___[/color].\n')
            reminders.append('''Neapolitan didn't submit your night actions:
                            [code]This is just a reminder that you have [countdown]1 day[/countdown] to figure out who you're going to investigate tonight, if anybody.[/code]''')
        elif v == 'town tracker':
            townActions.append(f'[*][color=green]{k}[/color] is tracking [color=white]___[/color].\n')
            reminders.append('''Tracker didn't submit your night actions:
                            [code]This is just a reminder that you have [countdown]1 day[/countdown] to figure out who you're going to track tonight, if anybody.[/code]''')
        elif v == 'mafia roleblocker':
            mafiaActions.append(f'[*][color=#400]{k}[/color] is roleblocking [color=green]___[/color].\n')
            reminders.append('''Roleblocker didn't submit your night actions:
                            [code]This is just a reminder that you have [countdown]1 day[/countdown] to figure out who you're going to kill and/or roleblock tonight, if anybody.[/code]''')
        elif v == 'mafia rolecop':
            mafiaActions.append(f'[*][color=#400]{k}[/color] is rolecopping [color=green]___[/color].\n')
            reminders.append('''Roleblocker didn't submit your night actions:
                            [code]This is just a reminder that you have [countdown]1 day[/countdown] to figure out who you're going to kill and/or rolecop tonight, if anybody.[/code]''')
        elif 'mafia roleblocker' not in roles.values() and 'mafia rolecop' not in roles.values():
            reminders.append('''Roleblocker didn't submit your night actions:
                            [code]This is just a reminder that you have [countdown]1 day[/countdown] to figure out who you're going to kill tonight, if anybody.[/code]''')
    for n in range(1,3):
        event = event + f"[area=night {n}][list]"
            for action in townActions:
                event = event + action
            for action in mafiaActions:
                event = event + action
        event = event + '[/list][/area]\n\n'

        event = event + f"[area=day {n+1}][list][*]___ is lynched with _ scum on ___ wagon.[/list][/area]\n\n"
    return event, '\n\n'.join(reminders)

DESCRIPTION = makeGameDescription()
PUBLICTHREAD = makeOP("public")

EVENTS, NIGHTACTIONREMINDERS = gameEvents()
YOUTUBE = input("Type a youtube video for day 1 lynch: ")
MODTHREAD = makeOP("mod")

#TODO finish making mafia thread template
MAFIAPICTURE = input("Picture for MAFIA thread: ")
MAFIATEXT = input("Text for MAFIA thread: ")
MAFIALINK = input("Link for MAFIA thread: ")
MAFIATITLE = input("Title for MAFIA thread link: ")
MAFIATHREAD = makeOP("mafia")

ICPICTURE = input("Picture for IC thread: ")
ICTEXT = input("Text for IC thread: ")
ICLINK = input("Link for IC thread: ")
ICTITLE = input("Title for IC thread link: ")
ICTHREAD = makeOP("ic")

DEADPICTURE = input("Picture for dead thread: ")
DEADTEXT = input("Text for dead thread: ")
DEADLINK = input("Link for dead thread: ")
DEADTITLE = input("Title for dead thread link: ")
DEADTHREAD = makeOP("dead")

#TODO: set these variables: LINK, TITLE, EXPLANATION, DESCRIPTION]

for player, role in roles: 
    sendRolePM(player, role)
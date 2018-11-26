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

logging.basicConfig(filename='log-mafiaMod.txt', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.debug("Start of program.")

def login(browser, expectedTitle):
    '''Log back in if unexpectedly logged out. Returns browser object '''
    print('\nLogging in.\n')
    browser.get('https://forum.mafiascum.net/ucp.php?mode=login')
    elem = browser.find_element_by_name("username")
    elem.clear()
    if args.username:
        elem.send_keys(args.username)
    else:
        input("Type your username in the browser and then hit return here when you're done.")
    elem = browser.find_element_by_name('autologin')
    elem.click()
    elem = browser.find_element_by_name('viewonline')
    elem.click()
    elem = browser.find_element_by_name("password")
    elem.clear()
    input("Type your password in the browser and then hit return here when you're done")
    elem = WebDriverWait(browser, 10).until(EC.title_contains(expectedTitle))
    return browser

def makeOP(browser, whichThread):
    '''Create the first post in a thread. Returns the URL of the thread that it makes.'''
    print(f"Making {whichThread} thread")
    if whichThread == 'public':
        browser.get('https://forum.mafiascum.net/posting.php?mode=post&f=11')
    else:
        browser.get('https://forum.mafiascum.net/posting.php?mode=post&f=90')
    if 'icon-register' in browser.page_source:
        browser = login(browser, 'new topic')    
    elem = browser.find_element_by_name("subject")
    elem.clear()
    elem.send_keys(f"Newbie {args.number} | {args.title.title()} | {whichPT.title()}")
    elem.clear()
    elem = browser.find_element_by_name("message")
    post = readFile(whichThread, 0)
    for line in post:
        elem.send_keys(line)
    return browser.current_url

def listFiles(folder):
    '''return a list of all filenames in a directory'''
    abspath = os.path.abspath(__file__)
    fileDirectory = os.path.dirname(abspath) + '/files/' + folder + '/'
    files = os.listdir(fileDirectory)
    files.sort()
    print(f'\nFound {len(files)} files in {folder}: {", ".join(files)}')
    return files

def readFile(folder, file): #may need more replacements as more files added
    '''Load a file from a directory, fill in the placeholders with real data, 
    then return a list of the file's lines'''
    print(f'\nLoading ./files/{folder}/{file}\n')
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
        line = line.replace('COLOUREDPLAYERLIST', COLOUREDPLAYERLIST.join('\n'))
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
        line = line.replace('MAFIAPICTURE', MAFIAPICTURE)
        line = line.replace('MAFIATEXT', MAFIATEXT)
        line = line.replace('MAFIALINK', MAFIALINK)
        line = line.replace('MAFIATITLE', MAFIATITLE)
        line = line.replace('MAFIAONEROLE', setups[setup][0])
        line = line.replace('MAFIATWOROLE', setups[setup][1])
        line = line.replace('MAFIAONEPLAYER', MAFIAONEPLAYER)
        line = line.replace('MAFIATWOPLAYER', MAFIATWOPLAYER)
        line = line.replace('MAFIAONECOLOUR', MAFIAONECOLOUR)
        line = line.replace('MAFIATWOCOLOUR', MAFIATWOCOLOUR)
        line = line.replace('SAMPLETOWNPMS', SAMPLETOWNPMS)
        line = line.replace('SAMPLEMAFIAPMS', SAMPLEMAFIAPMS)
    return post

def sendRolePM(browser, recipient, role):
    '''Send a role PM to a player'''
    print(f"\nSending {recipient} their role PM: {role}\n")
    if 'icon-register' in browser.page_source:
        browser = login(browser, 'Compose message')    
    browser.get('https://forum.mafiascum.net/ucp.php?i=pm&mode=compose')
    elem = browser.find_element_by_name("username_list")
    elem.clear()
    elem.send_keys(recipient)
    elem = browser.find_element_by_name("subject")
    elem.clear()
    elem.send_keys(f"Newbie {args.number} | {args.title.title()} | Role PM")
    elem = browser.find_element_by_name("message")
    elem.clear()
    if recipient == ICPLAYER:
        elem.send_keys(f"Hi {recipient}! Thanks so much for ICing. I've made you an [url={ICTHREAD}]IC Thread here[/url]. Have fun!\n\n")
    post = readFile('roles', role)
    for line in post:
        elem.send_keys(line) 
    elem.submit()
    elem = browser.find_element_by_name("post")
    elem.click()

def makeGameDescription():
    '''Create and return the description that goes at the start of the public game'''
    print('\nMaking game description\n')
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
    '''Create a list of what happened during the game for posting in the mod PT'''
    print('\nCreating game events\n')
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

def lockThread(browser, whichThread):
    '''Lock a game thread so only the moderator can post in it.'''
    print(f'\nLocking {whichThread}\n')
    browser.get(whichThread)
    if 'icon-register' in browser.page_source:
        browser = login(browser, f'Newbie {args.number}')
    lock = browser.find_element_by_xpath("//select[@id='quick-mod-select']")
    lock.submit()
    elem = WebDriverWait(browser, 10).until(EC.title_contains('Lock topic'))
    yes = browser.find_element_by_name('confirm')
    yes.click()

def updateThread(browser, whichThread, post):
    '''Add posts to an existing thread.'''
    print(f'\nUpdating {whichThread}\n')
    if 'icon-register' in browser.page_source:
        login(browser, f'Newbie {args.number}')
    button = browser.find_element_by_class_name('buttons')
    button.click()
    elem = WebDriverWait(browser, 10).until(EC.title_contains('Post a reply'))
    textbox = browser.find_element_by_name('message')
    for line in post:
        textbox.send_keys(line)
    button = browser.find_element_by_name('post')
    button.click()

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

#args
parser = argparse.ArgumentParser(description='Setup a newbie game.')
parser.add_argument('setup', metavar='setup', type=str, choices=setups.keys(),
                    help='Have the playerlist copied and ready to go.')
parser.add_argument('number', metavar='gamenumber', type=int, help="Game number")
parser.add_argument('title', metavar="gametitle", type=str, help="Name of the theme")
parser.add_argument('-u', '--username', metavar="username", type=str, help="Moderator's username")
parser.add_argument('totalPlayers', metavar="totalPlayers", type=int, help="How many players", nargs='?', default=9)

args = parser.parse_args()
#args = parser.parse_args(['A1', '1900', 'Popcorn'])
logging.info(f"args: {args}")

if not args.number:
    args.number = input("Enter your game number: ")
if not args.title:
    args.title = input("Enter your game title: ")

# get playerlist
players = []

try: #try to get playerlist from clipboard
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

#shuffle playerlist
shuffledPlayers = players[:]
random.shuffle(shuffledPlayers)

#assign roles
roles = dict(zip(shuffledPlayers,setups[setup]))

for i, role in enumerate(roles):
    print(role, ':', roles[role]) 
    if i == 0:
        MAFIAONEPLAYER = role
    elif i == 1:
        MAFIATWOPLAYER = role

# initialise playerlist related variables
NUMBEREDPLAYERLIST = []
COLOUREDPLAYERLIST = []
PLAYERLIST = []
ICPLAYER = ""

if setup in ('A1', 'A2', 'A3', 'B1', 'B2', 'B3'):
    MAFIAONECOLOUR = 'darkred'
else:
    MAFIAONECOLOUR = 'redorange'

MAFIATWOCOLOUR = 'redorange'

#create sample role PMs for public thread and mafia private thread
SAMPLEMAFIAPMS = ""
SAMPLETOWNPMS = ""
for role in ("mafia goon", "mafia rolecop", "mafia roleblocker"):
    SAMPLEMAFIAPMS += readFile('roles', role)
for role in ("vanilla townie", "town jailkeeper", "town cop", "town neapolitan", "town tracker", "town doctor"):
    SAMPLETOWNPMS += readFile('roles', role)

#create variously formatted playerlist variables to be posted in various threads
for i, player in enumerate(players):
    NUMBEREDPLAYERLIST.append(f"{i+1}) {player}")
    if player == MAFIAONEPLAYER:
        COLOUREDPLAYERLIST.append(f"[color=MAFIAONECOLOUR]{i+1}) {player}, {roles[player]}[/color]")
    elif player == MAFIATWOPLAYER:
        COLOUREDPLAYERLIST.append(f"[color=MAFIATWOCOLOUR]{i+1}) {player}, {roles[player]}[/color]")
    else:
        COLOUREDPLAYERLIST.append(f"[color=CHARTREUSE]{i+1}) {player}[/color]")
    if i == 8:
        PLAYERLIST.append(player.replace(' (IC)', ''))
        ICPLAYER = player
    else:
        PLAYERLIST.append(player.replace(' (SE)', ''))

browser = webdriver.Firefox()

# fill in any variables we need then make the public thread:
DESCRIPTION = makeGameDescription()
PUBLICTHREAD = makeOP(browser, "public")
lockThread(PUBLICTHREAD)

# fill in a few last variables and make the mod thread
EVENTS, NIGHTACTIONREMINDERS = gameEvents()
YOUTUBE = input("Type a youtube video for day 1 lynch: ")
MODTHREAD = makeOP(browser, "mod")

# fill in a few last variables and make the mafia thread
DEADLINE = datetime.datetime.now() + datetime.timedelta(days=2, minutes=15)
DEADLINE = DEADLINE - datetime.timedelta(minutes=DEADLINE.minute % 15, seconds=DEADLINE.second, microseconds=DEADLINE.microsecond)
DEADLINE = DEADLINE.isoformat(sep=" ", timespec="seconds")

MAFIAPICTURE = input("Picture for MAFIA thread: ")
MAFIATEXT = input("Text for MAFIA thread: ")
MAFIALINK = input("Link for MAFIA thread: ")
MAFIATITLE = input("Title for MAFIA thread link: ")
MAFIATHREAD = makeOP(browser, "mafia")

# fill in a few last variables and make the IC thread
ICPICTURE = input("Picture for IC thread: ")
ICTEXT = input("Text for IC thread: ")
ICLINK = input("Link for IC thread: ")
ICTITLE = input("Title for IC thread link: ")
ICTHREAD = makeOP(browser, "ic")

# fill in a few last variables and make the dead thread
DEADPICTURE = input("Picture for dead thread: ")
DEADTEXT = input("Text for dead thread: ")
DEADLINK = input("Link for dead thread: ")
DEADTITLE = input("Title for dead thread link: ")
DEADTHREAD = makeOP(browser, "dead")

publicFiles = listFiles('public')
for file in range(1,len(publicFiles)):
    updateThread(browser, PUBLICTHREAD, readFile(file))

modFiles = listFiles('mod')
for file in range(1,len(modFiles)):
    updateThread(browser, MODTHREAD, readFile(file))

#send out role PMs
for player in players:
    sendRolePM(player, roles[player]) 


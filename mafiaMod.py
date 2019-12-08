#!/usr/bin/python3
# Mod a newbie game

import logging
#logging.disable()
import argparse
import os
import sys
import random
import pprint
import readline
import datetime
import re
import time

try: #try to get playerlist from clipboard
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
except ModuleNotFoundError:
    print('Selenium module not found. Get it from https://pypi.org/project/selenium/ ')
    sys.exit()

#TODO: prepare PM to listmod

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.debug("Start of program.")

def login(browser, url):
    '''Log back in if unexpectedly logged out. Returns browser object '''
    print('\nLogging in.\n')
    browser.get('https://forum.mafiascum.net/ucp.php?mode=login')
    elem = browser.find_element_by_name('autologin')
    elem.click()
    elem = browser.find_element_by_name('viewonline')
    elem.click()
    elem = browser.find_element_by_name("username")
    elem.clear()
    if args.username:
        elem.send_keys(args.username)
    else:
        input("Type your username in the browser and then hit return here when you're done.")
    elem = browser.find_element_by_name("password")
    elem.clear()
    input("Type your password in the browser and then hit return here when you're done")
    elem = WebDriverWait(browser, 60).until(EC.title_contains("Index"))
    browser.get(url)

def makeOP(browser, whichThread, users=None, mods=None):
    '''Create the first post in a thread. Returns the URL of the thread that it makes.'''
    print(f"Making {whichThread} thread")
    if whichThread == 'public':
        url = 'https://forum.mafiascum.net/posting.php?mode=post&f=11'
        whichPT = "pregame"
    else:
        url = 'https://forum.mafiascum.net/posting.php?mode=post&f=90'
        whichPT = whichThread
    browser.get(url)
    if 'icon-register' in browser.page_source:
        logging.debug('need to login')
        login(browser, url)
    elem = browser.find_element_by_name("subject")
    elem.clear()
    elem.send_keys(f"Newbie {GAMENUMBER} | {GAMETITLE} | {whichPT.title()}")
    elem = browser.find_element_by_name("message")
    elem.clear()
    post = readFile(whichThread, '0')
    elem.send_keys(post)
    if users:
        for user in users:
            elem = browser.find_element_by_id('private_users_input')
            elem.send_keys(user)
            elem = browser.find_element_by_id('private_users_add_button')
            elem.click()
            time.sleep(5)
    if mods:
        for mod in mods:
            elem = browser.find_element_by_id('private_mods_input')
            elem.send_keys(mod)
            elem = browser.find_element_by_id('private_mods_add_button')
            elem.click()
            time.sleep(5)
    button = browser.find_element_by_name('post')
    button.click()
    elem = WebDriverWait(browser, 60).until(EC.title_contains(GAMETITLE))
    time.sleep(1)
    threadUrl = browser.current_url
    elem = browser.find_element_by_partial_link_text('Bookmark topic')
    elem.click()
    return threadUrl

def listFiles(folder):
    '''return a list of all filenames in a directory'''
    abspath = os.path.abspath(__file__)
    fileDirectory = os.path.dirname(abspath) + '/files/' + folder + '/'
    files = os.listdir(fileDirectory)
    files.sort()
    print(f'\nFound {len(files)} files in {folder}: {", ".join(files)}')
    return files

def readFile(folder, file, rolePM=False):
    '''Load a file from a directory, then return the file as a string'''
    print(f'\nLoading ./files/{folder}/{file}\n')
    abspath = os.path.abspath(__file__)
    fileDirectory = os.path.dirname(abspath) + '/files/' + folder + '/'
    with open(fileDirectory + file, 'r') as f:
        post = list(f)
    post = ''.join(post)
    logging.debug('preparing post')
    post = preparePost(post, rolePM)
    return post

def preparePost(post, rolePM=False):
    '''fill in the placeholders with real data'''
    placeholders = ['GAMENUMBER', 'GAMETITLE', 'DESCRIPTION', 'SAMPLETOWNPMS', 'SAMPLEMAFIAPMS',
            'MAFIATHREAD', 'PUBLICTHREAD', 'ICTHREAD', 'DEADTHREAD', 'MODTHREAD', 'MASONTHREAD',
            'NUMBEREDPLAYERLIST', 'COLOUREDPLAYERLIST', 'MASONPLAYERLIST', 'PLAYERLIST',
            'ROLES', 'EVENTS', 'YOUTUBE', 'NIGHTACTIONREMINDERS', 'DEADLINE', LISTMOD, GAMEMOD,
            'DEADPICTURE', 'DEADTEXT', 'DEADLINK', 'DEADTITLE', SPECTATORS,
            'MAFIAPICTURE', 'MAFIATEXT', 'MAFIALINK', 'MAFIATITLE',
            'MAFIAONEROLE', 'MAFIAONEPLAYER', 'MAFIAONECOLOUR',
            'MAFIATWOROLE', 'MAFIATWOPLAYER', 'MAFIATWOCOLOUR',
            'MASONPICTURE', 'MASONTEXT', 'MASONTITLE', 'MASONLINK']
    if rolePM:
        placeholders.extend(['MASON1', 'MASON2'])
    for placeholder in placeholders:
        if re.search(placeholder, post):
            logging.debug(f'found {placeholder} ')
            #this doesn't work:
            #post = re.sub(placeholder, f'{placeholder}', post)
            #TODO: find a way to do this without eval
            post = re.sub(placeholder, eval(placeholder), post)
            post = post.replace("via [url=][/url]", "")
            post = post.replace("[url=][/url]", "")
            post = post.replace("[*][url=Mason PT]Mason PT[/url]", "")
    return post

def sendRolePM(browser, recipient, role):
    '''Send a role PM to a player'''
    print(f"\nSending {recipient} their role PM: {role}\n")
    url = 'https://forum.mafiascum.net/ucp.php?i=pm&mode=compose'
    browser.get(url)
    if 'icon-register' in browser.page_source:
        login(browser, url)
    elem = browser.find_element_by_name("username_list")
    elem.clear()
    elem.send_keys(recipient)
    elem = browser.find_element_by_name('add_to')
    elem.click()
    elem = browser.find_element_by_name("subject")
    elem.clear()
    elem.send_keys(f"Newbie {GAMENUMBER} | {GAMETITLE} | Role PM")
    elem = browser.find_element_by_name("message")
    elem.clear()
    post = readFile('roles', role, rolePM=True)
    elem.send_keys(post)
    input('Everything okay?')
    elem = browser.find_element_by_name("post")
    elem.click()

def makeGameDescription():
    '''Create and return the description that goes at the start of the public game'''
    print('\nMaking game description\n')
    DOINGWHAT = ''
    if "stuff i found online" in GAMETITLE.lower():
        DOINGWHAT = "showcasing cool stuff I found/learned about online via my RSS reader and maybe talking some about why I think it's cool. "
    elif "zoo" in GAMETITLE.lower():
        DOINGWHAT = "showing pictures of cute baby zoo animals. "
    elif "cake" in GAMETITLE.lower():
        DOINGWHAT = "showing pictures of failed cakes by professional bakers."
    elif "urw" in GAMETITLE.lower():
        DOINGWHAT = "[code]" + input("Output of `urwbot, start`: ") + "[/code]"
    else:
        DOINGWHAT = input('Hello. In this game I\'ll be _____ ')

    IMG = input('Upload an image: ')
    LINK = input('Link: ')
    TITLE = input('Such as [Title for link],: ')
    EXPLANATION = input(f'Finish this sentence: Such as {TITLE}, ______ ')
    DESCRIPTION = f"""[center][thumb=600]{IMG}[/thumb][/center]\n
        \n
        Hello. In this game I'll be  {DOINGWHAT}
        Such as [url={LINK}]{TITLE}[/url]. {EXPLANATION}"""
    return DESCRIPTION

def gameEvents():
    '''Create a list of what happened during the game for posting in the mod PT'''
    print('\nCreating game events\n')
    event = "[area=day 1][list][*]___ is lynched with _ scum on ___ wagon.[/list][/area]\n\n"
    townActions = []
    mafiaActions = ['[*][color=purple]___[/color] is killing [color=green]___[/color].\n']
    reminders = []
    for k, v in roles.items():
        if role_verbs.get(v):
            if v.startswith('mafia'):
                mafiaActions.append(f'[*][color=indigo]{k}[/color] is {role_verbs[v]}ing [color=green]___[/color].\n')
                reminders.append(f'''{k}, {v} didn't submit their night actions:
                    [code]This is just a reminder that you have [countdown]1 day[/countdown] to figure out who you're going to {role_verbs[v]} kill tonight, if anybody.[/code]''')
            else:
                if role_verbs[v].endswith('e'):
                    townActions.append(f'[*][color=green]{k}[/color] is {role_verbs[v][:-1]}ing [color=white]___[/color].\n')
                else:
                    townActions.append(f'[*][color=green]{k}[/color] is {role_verbs[v]}ing [color=white]___[/color].\n')
                reminders.append(f'''{k}, {v} didn't submit their night actions:
                    [code]This is just a reminder that you have [countdown]1 day[/countdown] to figure out who you're going to {role_verbs[v]} tonight, if anybody.[/code]''')

    for n in range(1,4):
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
        login(browser, whichThread)
    lock = browser.find_element_by_id("quick-mod-select")
    lock.submit()
    elem = WebDriverWait(browser, 60).until(EC.title_contains('Lock topic'))
    yes = browser.find_element_by_name('confirm')
    yes.click()

def updateThread(browser, whichThread, post):
    '''Add posts to an existing thread.'''
    print(f'\nUpdating {whichThread}\n')
    browser.get(whichThread)
    if 'icon-register' in browser.page_source:
        login(browser, whichThread)
    button = browser.find_element_by_class_name('buttons')
    button.click()
    elem = WebDriverWait(browser, 60).until(EC.title_contains('Post a reply'))
    textbox = browser.find_element_by_name('message')
    textbox.send_keys(post)
    time.sleep(5)
    button = browser.find_element_by_name('post')
    button.click()
    WebDriverWait(browser, 60).until(EC.title_contains('Information'))

role_verbs={
    'mafia 1-shot strongman' : 'strongman',
    'mafia roleblocker' : 'roleblock and/or',
    'mafia rolecop' : 'rolecop and/or',
    'town babysitter' : 'babysit',
    'town cop' : 'investigate',
    'town doctor' : 'protect',
    'town follower' : 'follow',
    'town friendly neighbor' : 'inform',
    'town jailkeeper' : 'jailkeep',
    'town neapolitan' : 'investigate',
    'town roleblocker' : 'roleblock',
    'town rolecop' : 'rolecop',
    'town tracker' : 'track',
    'town vanilla cop' : 'vanilla cop'
}

Matrix6 = {
    '1' : ['mafia goon', 'mafia goon', 'town jailkeeper'] + ['vanilla townie'] * 6,
    '2' : ['mafia roleblocker', 'mafia goon', 'town cop', 'town doctor'] + ['vanilla townie'] * 5,
    '3' : ['mafia goon', 'mafia goon', '1-shot bulletproof townie', 'town tracker'] + ['vanilla townie'] * 5,
    'A' : ['mafia roleblocker', 'mafia goon', 'town jailkeeper', '1-shot bulletproof townie'] + ['vanilla townie'] * 5,
    'B' : ['mafia goon', 'mafia goon', 'town cop'] + ['vanilla townie'] * 6,
    'C' : ['mafia goon', 'mafia goon', 'town tracker', 'town doctor'] + ['vanilla townie'] * 5,
}

Nine12 = {
    '1' : ['mafia rolecop', 'mafia goon', 'town vanilla cop', 'town tracker'] + ['vanilla townie'] * 5,
    '2' : ['mafia rolecop', 'mafia goon', 'town follower', 'town tracker'] + ['vanilla townie'] * 5,
    '3' : ['mafia rolecop', 'mafia goon', 'town follower', 'town jailkeeper'] + ['vanilla townie'] * 5,
    '4' : ['mafia 1-shot strongman', 'mafia goon', 'town follower', 'town jailkeeper'] + ['vanilla townie'] * 5,
    '5' : ['mafia 1-shot strongman', 'mafia goon', 'town jailkeeper', 'town babysitter'] + ['vanilla townie'] * 5,
    '6' : ['mafia 1-shot strongman', 'mafia goon', 'town babysitter', 'town roleblocker'] + ['vanilla townie'] * 5,
    '7' : ['mafia rolecop', 'mafia goon', 'town babysitter', 'town roleblocker'] + ['vanilla townie'] * 5,
    '8' : ['mafia rolecop', 'mafia goon', 'town roleblocker', 'town rolecop'] + ['vanilla townie'] * 5,
    '9' : ['mafia rolecop', 'mafia goon', 'town rolecop', 'town doctor'] + ['vanilla townie'] * 5,
    '10' : ['mafia roleblocker', 'mafia goon', 'town rolecop', 'town doctor'] + ['vanilla townie'] * 5,
    '11' : ['mafia roleblocker', 'mafia goon', 'town doctor', 'town vanilla cop'] + ['vanilla townie'] * 5,
    '12' : ['mafia roleblocker', 'mafia goon', 'town vanilla cop', 'town tracker'] + ['vanilla townie'] * 5,
}

TwoD3 = {
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

NewD3 = {
    'A1' : ['mafia roleblocker', 'mafia goon', 'town cop', 'town doctor'] + ['vanilla townie'] * 5,
    'A2' : ['mafia roleblocker', 'mafia goon', 'town jailkeeper', 'town tracker'] + ['vanilla townie'] * 5,
    'A3' : ['mafia roleblocker', 'mafia goon', 'town mason1', 'town mason2'] + ['vanilla townie'] * 5,
    'B1' : ['mafia rolecop', 'mafia goon', 'town tracker', 'town friendly neighbor'] + ['vanilla townie'] * 5,
    'B2' : ['mafia rolecop', 'mafia goon', 'town jailkeeper', 'town friendly neighbor'] + ['vanilla townie'] * 5,
    'B3' : ['mafia rolecop', 'mafia goon', 'town tracker', 'town doctor'] + ['vanilla townie'] * 5,
    'C1' : ['mafia goon', 'mafia goon', 'town cop'] + ['vanilla townie'] * 6,
    'C2' : ['mafia goon', 'mafia goon', 'town jailkeeper'] + ['vanilla townie'] * 6,
    'C3' : ['mafia goon', 'mafia goon', 'town mason1', 'town mason2'] + ['vanilla townie'] * 5,
}

setups = {
    'Matrix6' : Matrix6,
    '9:12' : Nine12,
    '2d3' : TwoD3,
    'NewD3' : NewD3,
}

#args
parser = argparse.ArgumentParser(description='Setup a newbie game.')
parser.add_argument('--setup', metavar='setup', type=str, choices=setups.keys(), default='NewD3',
                    help='Matrix6, 9:12, 2d3, or NewD3 (default)')
parser.add_argument('subsetup', metavar='subsetup', type=str, help='A1, 12, C, etc')
parser.add_argument('number', metavar='gamenumber', type=int, help="Game number")
parser.add_argument('title', metavar="gametitle", type=str, help="Name of the theme")
parser.add_argument('username', metavar="username", type=str, help="Moderator's username")
parser.add_argument('-l', '--listmod', metavar='listmod', type=str, help='Listmod\'s username', default='PenguinPower', nargs='?')
parser.add_argument('totalPlayers', metavar="totalPlayers", type=int, help="How many players", nargs='?', default=9)
parser.add_argument('-s', '--spectators', metavar="spectators", type=str, help="'Spectator1 Spectator2'", nargs='?')

args = parser.parse_args()
args.spectators = args.spectators.split()
#args = parser.parse_args(['A1', '1900', 'Popcorn'])
logging.info(f"args: {args}")

if not args.number:
    args.number = input("Enter your game number: ")
if not args.title:
    args.title = input("Enter your game title: ")

GAMENUMBER = str(args.number)
GAMETITLE = args.title
GAMEMOD = args.username
LISTMOD = args.listmod
if args.spectators:
    SPECTATORS = ', '.join(args.spectators)
else:
    SPECTATORS = ''
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

shuffledPlayers = players[:]
random.shuffle(shuffledPlayers)
subsetup = setups[args.setup][args.subsetup]

roles = dict(zip(shuffledPlayers,subsetup))

ROLES = ""
for k, v in roles.items():
    ROLES += f'{v}: {k}\n'
MASON1 = '[Mason1]'
MASON2 = '[Mason2]'
MASONTHREAD = '[Mason thread]'
MAFIATHREAD = '[Mafia thread]'
PUBLICTHREAD = '[Public thread]'

#create sample role PMs for public thread and mafia private thread
MAFIATHREAD = 'mafia PT' # can't have the mafia link in these
MASONTHREAD = 'mason PT'
SAMPLEMAFIAPMS = ""
SAMPLETOWNPMS = ""
for role in ("mafia goon", "mafia rolecop", "mafia roleblocker"):
    SAMPLEMAFIAPMS += readFile('roles', role)
for role in ("vanilla townie", "town jailkeeper", "town cop", "town mason1", "town tracker", "town doctor", "town friendly neighbor"):
    SAMPLETOWNPMS += readFile('roles', role)

for i, role in enumerate(roles):
    print(role, ':', roles[role])
    if i == 0:
        MAFIAONEPLAYER = role.replace(' (SE)', '')
        MAFIAONEROLE = roles[role]
        if MAFIAONEROLE == 'mafia goon':
          MAFIAONECOLOUR = 'purple'
        else:
          MAFIAONECOLOUR = 'indigo'
    elif i == 1:
        MAFIATWOPLAYER = role.replace(' (SE)', '')
        MAFIATWOROLE = roles[role]
        MAFIATWOCOLOUR = 'purple'
    elif i == 2 and roles[role] == 'town mason1':
        MASON1 = role.replace(' (SE)', '')
    elif i == 3 and roles[role] == 'town mason2':
        MASON2 = role.replace(' (SE)', '')

# initialise playerlist related variables
NUMBEREDPLAYERLIST = []
COLOUREDPLAYERLIST = []
MASONPLAYERLIST = []
PLAYERLIST = []

#create variously formatted playerlist variables to be posted in various threads
for i, player in enumerate(players):
    NUMBEREDPLAYERLIST.append(f"{i+1}) {player}")
    if player.replace(' (SE)', '') == MAFIAONEPLAYER:
        COLOUREDPLAYERLIST.append(f"[color=MAFIAONECOLOUR]{i + 1}) {player}, {roles[player]}[/color]")
    elif player.replace(' (SE)', '') == MAFIATWOPLAYER:
        COLOUREDPLAYERLIST.append(f"[color=MAFIATWOCOLOUR]{i + 1}) {player}, {roles[player]}[/color]")
    else:
        COLOUREDPLAYERLIST.append(f"[color=green]{i + 1}) {player}[/color]")
    if player.replace(' (SE)', '') in (MASON1, MASON2):
        MASONPLAYERLIST.append(f"[color=green]{i + 1} {player}, town mason[/color]")
    else:
        MASONPLAYERLIST.append(f"{i+1}) {player}")
    PLAYERLIST.append(player.replace(' (SE)', ''))

NUMBEREDPLAYERLIST = '\n'.join(NUMBEREDPLAYERLIST)
PLAYERLIST = '\n'.join(PLAYERLIST)
COLOUREDPLAYERLIST = '\n'.join(COLOUREDPLAYERLIST)
MASONPLAYERLIST = '\n'.join(MASONPLAYERLIST)

browser = webdriver.Firefox()

# fill in any variables we need then make the public thread:

DESCRIPTION = makeGameDescription()
DEADLINE = datetime.datetime.now() + datetime.timedelta(days=2, minutes=30)
DEADLINE = DEADLINE - datetime.timedelta(minutes=DEADLINE.minute % 15, seconds=DEADLINE.second, microseconds=DEADLINE.microsecond)
print(f'{datetime.datetime.strftime(DEADLINE, "%Y %j %H:%M:%S")} day 1 starts')
DEADLINE = DEADLINE.isoformat(sep=" ", timespec="seconds")
print(f'[countdown]{DEADLINE}[/countdown]')
PUBLICTHREAD = makeOP(browser, "public")
lockThread(browser, PUBLICTHREAD)

# fill in a few last variables and make the mod thread
EVENTS, NIGHTACTIONREMINDERS = gameEvents()
MODTHREAD = makeOP(browser, "mod", mods=[args.listmod])

#fill in a few last variables and make the mafia thread
MAFIAPICTURE = input("Picture for MAFIA thread: ")
MAFIATEXT = input("Text for MAFIA thread: ")
MAFIALINK = input("Link for MAFIA thread: ")
MAFIATITLE = input("Title for MAFIA thread link: ")
MAFIATHREAD = makeOP(browser, "mafia", users=[MAFIAONEPLAYER, MAFIATWOPLAYER], mods=[args.listmod])

if 'town mason1' in subsetup:
    MASONPICTURE = input("Picture for MASON thread: ")
    MASONTEXT = input("Text for MASON thread: ")
    MASONLINK = input("Link for MASON thread: ")
    MASONTITLE = input("Title for MASON thread link: ")
    MASONTHREAD = makeOP(browser, "mason", users=[MASON1, MASON2], mods=[args.listmod])

# fill in a few last variables and make the dead thread
DEADPICTURE = input("Picture for dead thread: ")
DEADTEXT = input("Text for dead thread: ")
DEADLINK = input("Link for dead thread: ")
DEADTITLE = input("Title for dead thread link: ")
DEADTHREAD = makeOP(browser, "dead", users=args.spectators, mods=[args.listmod])

YOUTUBE = input("Type a youtube video for day 1 lynch: ")
YOUTUBE = YOUTUBE.replace('https://www.youtube.com/watch?v=', '')
modFiles = listFiles('mod')
for file in range(1,len(modFiles)):
    updateThread(browser, MODTHREAD, readFile('mod', str(file)))
    time.sleep(5)

#send out role PMs
for i, player in enumerate(players):
    logging.debug(f'player: {player}, roles: {roles}')
    sendRolePM(browser, PLAYERLIST.split('\n')[i], roles[player])
    time.sleep(5)

publicFiles = listFiles('public')
for file in range(1,len(publicFiles)):
    updateThread(browser, PUBLICTHREAD, readFile('public', str(file)))
    time.sleep(5)

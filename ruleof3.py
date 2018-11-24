#! /usr/bin/python3
# -*- coding: utf-8 -*-
import random, readline

a,s,c = '', '', ''

def getInputs():
	alive = ''
	scum = ''
	while not alive.isdigit():
		alive = input('Alive? ')
	while not scum.isdigit():
		scum = input('Scum? ')
	return int(alive), int(scum)

def combinatorics(a,s,c):
	while c > 0:
		n = random.randint(1,a)
		if n >= s:
			print('town ')
			a = a - 1
			c = c - 1
		else:
			print('scum ')
			a = a - 1
			s = s - 1
			c = c - 1
	again(a,s,c)

def again(a,s,c):
	yes = input("Again? [Y]es/[No] ")
	if yes[0].upper() == 'Y':
		a, s = getInputs()
		c = s
		combinatorics(a,s,c)
	else:
		print("Bye!")
		exit()

a, s = getInputs()
c = s
combinatorics(a,s,c)
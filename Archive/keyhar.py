#Import the library

import pygame
import pygame.midi
import socket
from time import sleep
import random
#import music21

# Constants
CHANNEL = 0
VOLUME = 127
HARP = 46


# Init information
screen = pygame.display.set_mode((640, 480))
pygame.init()
pygame.midi.init()
id = pygame.midi.get_default_output_id()
output = pygame.midi.Output(id, 0)

			
		

def noteon(pitch):
	output.note_on(pitch,VOLUME)
	
def noteoff(pitch):
	output.note_off(pitch,VOLUME)

def arpeggio(root, inversion, minor):
	global duration
	duration = 1
	if inversion == 0:
		chord = [root, root+4-minor, root+7]
	if inversion == 1:
		chord = [root+4-minor, root+7, root+12]
	if inversion == 2:
		chord = [root+7, root+12, root+16-minor]
		
	# Now play the notes.
	noteon(chord[0])
	sleep(.5)
	noteoff(chord[0])
	noteon(chord[1])
	sleep(.5)
	noteoff(chord[1])
	noteon(chord[2])
	sleep(.5)
	noteoff(chord[2])
	noteon(chord[1])
	sleep(.5)
	noteoff(chord[1])
	
def chord(root, inversion, minor):
	if inversion == 0:
		chord = [root, root+4-minor, root+7]
	if inversion == 1:
		chord = [root+4-minor, root+7, root+12]
	if inversion == 2:
		chord = [root+7, root+12, root+16-minor]
			
	# Now play the note.
	noteon(chord[0])
	noteon(chord[1])
	noteon(chord[2])
	sleep(2)
	noteoff(chord[0])
	noteoff(chord[1])
	noteoff(chord[2])
	

def structure(key):
	second = [2, 3, 4, 5, 6]
	third = [6, 8]
	forth = 8
	
	arpeggio(key, 0, random.randint(0,1))
	chord(key+second[random.randint(0, 4)], 1, 0)
	arpeggio(key+third[random.randint(0,1)], random.randint(0,2), 1)
	chord(key+forth, 1, random.randint(0,1))

#structure(random.randint(40, 70))

running = True

screen.fill((0, 0, 0))

while running:
	for events in pygame.event.get():
		if events.type == pygame.KEYDOWN:
			if events.key == 27:
				running = False
				break
			print "Key " + str(events.key) + " being pressed!"
			noteon(events.key)
		elif events.type == pygame.KEYUP:
			if events.key == 27:
				running = False
				break
			print "Key " + str(events.key) + " being released!"
			noteoff(events.key)
		



del output
pygame.midi.quit()
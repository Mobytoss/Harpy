#Import the library

import pygame
import pygame.midi
import socket
import select
from time import sleep
import random
import threading
#import music21

# Constants
CHANNEL = 0
VOLUME = 127
INSTRUMENT = chr(46) #Harp
STATES = [False for x in range(255)]
CLIENTID = ""

clients = [STATES for x in range(32)]

# Init information
screen = pygame.display.set_mode((640, 480))
pygame.init()
pygame.midi.init()
id = pygame.midi.get_default_output_id()
output = pygame.midi.Output(id, 0)
output.set_instrument(ord(INSTRUMENT))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         # Create a socket object
host = socket.gethostname() # Get local machine name
#host = "pi.sk1t.com" # Get hampe's address
port = 5800                # Reserve a port for your service.
			
		

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
	

def mainkey():
	player = ''
	instr = ''
	note = ''
	global running
	while running:
		print "Preparing select next..."
		inputready,outputready,exceptready = select.select(input,[],[]) 
		print "start of input loop, now keyboard events"
		for items in inputready:
			if items == s:
				notein = s.recv(3)
				if notein != '':
					player = ord(notein[0])
					instru = ord(notein[1])
					note = ord(notein[2])
					if clients[player][note] == False:
						if note != 27: noteon(note)
						clients[player][note] = True
					elif clients[player][note] == True:
						noteoff(note)
						clients[player][note] = False
		print "end of input loop, now keyboard events"
		

running = True
s.connect((host, port))
CLIENTID = s.recv(1)	
screen.fill((0, 0, 0))
devices = pygame.midi.get_count()
inputs = [0 for x in range(0,devices)]
inputnum = 0
#unrelated to the above
input = [s]
mainthread = threading.Thread(target=mainkey)
mainthread.start()

while running:
	for events in pygame.event.get():
		if events.type == pygame.KEYDOWN:
			key = chr(events.key)
			if events.key == 27:
				running = False
				s.sendall(CLIENTID + INSTRUMENT + key)
				s.close
				break
			print "Key " + str(events.key) + " being pressed!"
			#noteon(events.key)
			s.sendall(CLIENTID + INSTRUMENT + key)
		elif events.type == pygame.KEYUP:
			key = chr(events.key)
			s.sendall(CLIENTID + INSTRUMENT + key)
			print "Key " + str(events.key) + " being released!"
			#noteoff(events.key)




		



del output
pygame.midi.quit()
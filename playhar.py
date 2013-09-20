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
pygame.init()
pygame.midi.init()
port = pygame.midi.get_default_output_id()
output = pygame.midi.Output(port, 0)
output.set_instrument(HARP)

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 1987                 # Reserve a port for your service.


			
		

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



s.connect((host, port))


#byte = []
#file = open("chopin.mid", 'rb')
#print file
#while 1:
#	byte.append(file.read(1))
#	if not byte:
#		break
#file.close()

#for x in byte:
#	if byte[x] is 0x9 or 0x8: s.send(byte[x+1])

for x in range(0, 60):
	print str(60-x) + ' was sent...'
	s.send(str(60-x))
	sleep(.5)
	s.send(str(60-x))

s.close 
del output
pygame.midi.quit()
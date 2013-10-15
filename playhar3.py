#Import the library

import pygame
import pygame.midi
import socket
from time import sleep
import random
import select
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
id = pygame.midi.get_default_input_id()
input = 0
output.set_instrument(HARP)

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

running = True
s.connect((host, port))
screen.fill((0, 0, 0))
devices = pygame.midi.get_count()
inputs = [0 for x in range(0,devices)]
inputcount = 0
for n in range(0, devices):
	info = pygame.midi.get_device_info(n)
	if info[2] == 1:
		inputs[inputcount] = n
		inputcount +=1
		print str(inputcount) + ". - " + info[1]
dchoice = raw_input('Choose MIDI device: ')
inputnum = int(dchoice) - 1
print "The ID of this device is " + str(inputs[inputnum])
input = pygame.midi.Input(inputs[inputnum])

while running:
	inputready,outputready,exceptready = select.select(input,output,[]) 
	if input.poll():
		messages = input.read(1000)
		for events in messages:
			key = chr(events[0][1])
			velo = events[0][2]
			if velo > 0:
				if key == 0:
					thekey = str(27)
					running = False
					s.sendall(thekey)
					s.close
					break
				print "Key " + str(ord(key)) + " being pressed!"
				#noteon(key)
				s.sendall(key)
			elif velo == 0:
				s.sendall(key)
				print "Key " + str(ord(key)) + " being released!"
				#noteoff(key)
				
input.close()
del input
del output
pygame.midi.quit()
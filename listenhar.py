#Import the library

import pygame
import pygame.midi
import socket
from time import sleep
import random

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

# Socket information
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 1987))

def noteon(pitch):
	output.note_on(pitch,VOLUME)
	
def noteoff(pitch):
	output.note_off(pitch,VOLUME)
	

s.listen(1)
state = [False for x in range(120)]
c, addr = s.accept()     # Establish connection with client.
print 'Got connection from', addr
while state[1] == False:
	buffer = c.recv(3)
	print buffer + ' was received...\n'
	if buffer != '':
		note = int(buffer)
		if state[note] == False:
			if note != 1: noteon(note)
			state[note] = True
		elif state[note] == True:
			noteoff(note)
			state[note] = False
		
   
# And close
c.close()
del output
pygame.midi.quit()
#Import the library

import pygame
import pygame.midi
import socket
import select
import threading
from time import sleep
import random

# Constants
CHANNEL = 0
VOLUME = 127
HARP = 46
HOST = ''
PORT = 5800

# Init MIDI information
pygame.init()
pygame.midi.init()
port = pygame.midi.get_default_output_id()
midoutput = pygame.midi.Output(port, 0)
midoutput.set_instrument(HARP)

# Socket information
connections = []
threads = []
running = True
clientid = 1

# Functions

def console():
	global running
	while (running):
		getinput = raw_input(">") 
		if getinput == "/exit":
			for ac in connections:
				try:
					ac[0].close()
					connections.remove(ac)
				except:
					print str(ac[0]) + " already closed, ignoring..."
			running = False
			return 0
		elif getinput == "/connections":
			for ac in connections:
				print str(ac[1])
		else: print "Command '" + getinput + "' unknown"
			
		
 
##### Main
mainthread = threading.Thread(target=console)
mainthread.start()
listener = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listener.bind((HOST,PORT))
listener.listen(3)
input = [listener]
output = []



# Main loop
while running:
	inputready,outputready,exceptready = select.select(input,output,[]) 
	for trigger in inputready:
		if trigger == listener:
			conn, addr = listener.accept() 
			connections.append((conn, addr))
			input.append(conn)
			conn.send(chr(clientid))
			clientid += 1
			print "New connection: " + str(conn)
			#output.append(conn)
		else: 
			buffer = "\0\0\0"
			buffer = trigger.recv(3)
			print buffer + ' was received...\n'
			if buffer != '':
				note = ord(buffer[2])
				if note == 27:
					trigger.close()
				else:	
					for client in connections:
						client[0].send(buffer)
del midoutput
pygame.midi.quit()					
##### End of Main
		
   

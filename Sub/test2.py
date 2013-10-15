import struct
import pygame
import pygame.midi
from time import sleep

CHANNEL = 0
VOLUME = 127
HARP = 46

pygame.init()
pygame.midi.init()
id = pygame.midi.get_default_output_id()
output = pygame.midi.Output(id, 0)
output.set_instrument(HARP)

file = open("C:\Users\Toby\Documents\GitHub\Harpy\Sub\kavinsky-nightcall.mid", "rb")

def readmid(bytenum):
	chars = ''
	output = ''
	for c in range(1, bytenum+1):
		chars += 'c'
	bytes = struct.unpack(chars, file.read(bytenum))
	for c in range(0, bytenum):
		output += str(ord(bytes[c]))+' '
	return output	

title = struct.unpack("s"*4, file.read(4))
size = struct.unpack(">L", file.read(4))
formats = struct.unpack(">H", file.read(2))
numtrk = struct.unpack(">H", file.read(2))
ticks = struct.unpack(">H", file.read(2))
trackstart = struct.unpack("s"*4, file.read(4))

def noteon(pitch):
	output.note_on(pitch,VOLUME)
	
def noteoff(pitch):
	output.note_off(pitch,VOLUME)

print title
print size
print formats
print numtrk
print ticks
print trackstart
nextchar = '\x00'
output.note_on(64,100)
sleep(2)
output.note_off(64,100)
while 1:
	sleep(0.01)
	filebyte = file.read(1)
	if len(filebyte) == 1:
		nextchar = struct.unpack("c", filebyte)
		print nextchar
		for hexi in range (0x90, 0xA0):
			if nextchar[0] == chr(hexi):
				nextnote = struct.unpack("c", file.read(1))
				#nextvelo = struct.unpack("c", file.read(1))
				notenum = ord(nextnote[0])
				output.note_on(int(notenum),100)#ord(nextvelo[0]))
				print "Note on for " + str(ord(nextnote[0])) + " on channel " + str(hexi-0x90) + " with volume "# + str(ord(nextvelo[0]))
		for hexi in range (0x80, 0x90):
			if nextchar[0] == chr(hexi):
				nextnote = struct.unpack("c", file.read(1))
				#nextvelo = struct.unpack("c", file.read(1))
				notenum = ord(nextnote[0])
				output.note_off(int(notenum),100)#ord(nextvelo[0]))
				print "Note off for " + str(ord(nextnote[0])) + " on channel " + str(hexi-0x90) + " with volume "# + str(ord(nextvelo[0]))
	else:
		break
print "End of file..."



file.close()
del output
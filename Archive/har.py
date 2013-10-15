#Import the library

from midiutil.MidiFile import MIDIFile
import random

# Create the MIDIFile Object with 1 track
MyMIDI = MIDIFile(1)

# Tracks are numbered from zero. Times are measured in beats.

track = 0   
time = 0

# Add track name and tempo.
MyMIDI.addTrackName(track,time,"Sample Track")
MyMIDI.addTempo(track,time,120)

# Add a note. addNote expects the following information:
track = 0
channel = 0
duration = 1
volume = 100

def note(pitch, time):
	MyMIDI.addNote(track,channel,pitch,time,duration,volume)

def arpeggio(root, inversion, minor):
	global duration
	duration = 1
	if inversion == 0:
		chord = [root, root+4-minor, root+7]
	if inversion == 1:
		chord = [root+4-minor, root+7, root+12]
	if inversion == 2:
		chord = [root+7, root+12, root+16-minor]
			
	global time 
	# Now add the note.
	note(chord[0], time+0)
	note(chord[1], time+1)
	note(chord[2], time+2)
	note(chord[1], time+3) 
	time +=4
	
def chord(root, inversion, minor):
	global duration
	duration = 4
	if inversion == 0:
		chord = [root, root+4-minor, root+7]
	if inversion == 1:
		chord = [root+4-minor, root+7, root+12]
	if inversion == 2:
		chord = [root+7, root+12, root+16-minor]
			
	global time 
	# Now add the note.
	note(chord[0], time)
	note(chord[1], time)
	note(chord[2], time)
	note(chord[1], time) 
	time +=4

def structure(key):
	second = [2, 3, 4, 5, 6]
	third = [6, 8]
	forth = 8
	
	arpeggio(key, 0, random.randint(0,1))
	chord(key+second[random.randint(0, 4)], 1, 0)
	arpeggio(key+third[random.randint(0,1)], random.randint(0,2), 1)
	chord(key+forth, 1, random.randint(0,1))

structure(random.randint(40, 70))

# And write it to disk.
binfile = open("output.mid", 'wb')
MyMIDI.writeFile(binfile)
binfile.close()
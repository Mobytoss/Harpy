import io
import struct

file = open("kavinsky-nightcall.mid", "rb")

def readmid(bytenum):
	chars = ''
	output = ''
	for c in range(1, bytenum+1):
		chars += 'c'
	bytes = struct.unpack(chars, file.read(bytenum))
	for c in range(0, bytenum):
		output += str(ord(bytes[c]))+' '
	return output


title = file.read(4)
size = readmid(4)
formats = readmid(2)
numtrk = readmid(2)
ticks = readmid(2)
trackstart = file.read(4)



print title
print size
print formats
print numtrk
print ticks
print trackstart
for c in range(100):
	print readmid(4)



file.close()

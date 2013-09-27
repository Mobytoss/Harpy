import struct

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



print title
print size
print formats
print numtrk
print ticks
print trackstart
print struct.unpack(">L", file.read(4))
print struct.unpack(">H", file.read(2))
print struct.unpack(">H", file.read(2))
for c in range(5):
	print struct.unpack("cc", file.read(2))
print struct.unpack(">H", file.read(2))
for c in range(11):
	print struct.unpack("cc", file.read(2))
print struct.unpack("s"*4, file.read(4))
print struct.unpack(">L", file.read(4))
test = file.read(4894)
print struct.unpack("s"*4, file.read(4))
print struct.unpack(">L", file.read(4))
test = file.read(1528)
print struct.unpack("s"*4, file.read(4))
print struct.unpack(">L", file.read(4))
test = file.read(2014)
print struct.unpack("s"*4, file.read(4))
print struct.unpack(">L", file.read(4))
nextchar = '\x00'
while 1:
	filebyte = file.read(1)
	if len(filebyte) == 1:
		nextchar = struct.unpack("c", filebyte)
		for hexi in range (0x80, 0x8F):
			if nextchar[0] == chr(hexi):
				print "Note found for channel " + str(hexi-0x80) + " - value is " + nextchar[0]
	else:
		break
print "End of file..."



file.close()

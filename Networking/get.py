import socket
import struct

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         # Create a socket object
host = "nikhoward.co.uk" # raw_input("Enter hostname > ")
tree = "computer-services-norwich.gif" # raw_input("Enter directories/filename > ")
port = 80
s.connect((host, port))
header = "GET /"+tree+" HTTP/1.1\nHost: " + host + "\n\r\n\r"
s.send(header)
msg = s.recv(4128)
msgbytes = s.recv(8400)
newvar = list(msgbytes)
for n in range(192):
	buff = ord(newvar[13+n])
	buff = 0xFF - buff
	newvar[13+n] = chr(buff)
msgbytes = ''.join(newvar)
file = open("computer-services-norwich.gif", 'wb+')
file.write(msgbytes)
file.seek(3)
version = file.read(3)
width = struct.unpack('h',file.read(2))
height = struct.unpack('h',file.read(2))
bytebuff = struct.unpack('c',file.read(1))
unpacked = ord(bytebuff[0])
globaltab = (unpacked & (128>>1)) != 0
colours = ((unpacked >> 4) & ~8) + 1
sorted = (unpacked & (8>>1)) != 0
tablesize = 2**((unpacked & ~240) +1)
bytebuff = struct.unpack('c', file.read(1))
bgcolour = ord(bytebuff[0]) 
bytebuff = struct.unpack('c', file.read(1))
aspectratio = (ord(bytebuff[0]) + 15) / 64
globcolour = []

for n in range(tablesize):
	globcolour.append(file.read(3))
junk = file.read(9)
dimensions = struct.unpack('hhhh', file.read(8))
localtab = ord(file.read(1)) > 0
lzwsize = ord(file.read(1))
datasize = ord(file.read(1))
size = 0
while datasize != 0:
	size += datasize
	file.seek(file.tell() + datasize)
	datasize = ord(file.read(1))

#print header
print "GIF file format, version " + version
print "Image height/width: " + str(width[0]) + "x" + str(height[0])
#print screen descriptor
print "Global colour table present: " + str(globaltab)
print "Number of colour bits: " + str(colours)
print "Sorted table: " + str(sorted)
print "Table size: " + str(tablesize)
print "Background colour: " + str(bgcolour)
print "Aspect ratio: " + str(aspectratio)
#print global colour table
for n in range(tablesize):
	buff = struct.unpack("ccc", globcolour[n])
	print "Colour #" + str(n) + ": " + str(ord(buff[0])) + " / " + str(ord(buff[1])) + " / " + str(ord(buff[2]))
#print image descriptor
print "Image start co-ords are " + str(dimensions[0]) + ", " + str(dimensions[1]) + " and end co-ords " + str(dimensions[2]) + ", " + str(dimensions[3])
print "Local colour table present: " + str(localtab)
print "Minimum size of LZW chunks is " + str(lzwsize)
print "Image size: " + str(size)

file.close()
s.close()
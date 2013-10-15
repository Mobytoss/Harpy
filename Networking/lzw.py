import struct

def encode(data):
	strbuff = data[0] 
	nxtchar = ''
	datalen = len(data)
	datatab = {}
	index = 1
	code = 256
	encstr = ""
	while index < datalen:
		nxtchar = data[index]
		if strbuff+nxtchar in datatab:
			strbuff += nxtchar
		else:
			datatab[strbuff+nxtchar] = code
			if strbuff in datatab:
				encstr += struct.pack('h', datatab[strbuff])
			else:
				encstr += strbuff
			strbuff = nxtchar
			code += 1
		index +=1
	#print datatab
	#print encstr
	file = open("code.input.bin", 'wb')
	file.write(encstr)
	file.close()
	return encstr
	
def decode(data):
	w = ''
	index = 0
	datatab = {}
	output = ''
	for i in range(0,256):
		datatab.append(chr(i), chr(i))
		index = i
	for k in data:
		if k in datatab:
			output += de = datatab[k]
			w + 
			
			
			
			
#stringy = "CatOhCat&CatInTheHatAndTheRat"
#stringy = "AndAndAndAndAndAndAndAndAndAndAndAndAndAndAndAndAndAndAndAndAndAndAndAnd"	
file = open("code.input.bin")
stringy = file.read(0xFFFF)
print decode(stringy)
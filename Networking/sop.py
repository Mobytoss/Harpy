import sys
import socket
import select



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         # Create a socket object
host = socket.gethostname()
port = 1234
s.bind((host, port))
s.listen(3)

inputs = [s]
running = True


while running:
	inputbuffer,outputbuffer,errorbuffer = select.select(inputs,[],[])
	
	for ready in inputbuffer:
		if ready == s:
			client, addr = s.accept()
			inputs.append(client)
		else:
			keyin = ready.recv(1024)
			if keyin == "/exit":
				running = False
				break
			elif keyin == "":
				i=1
			else:
				print keyin
	
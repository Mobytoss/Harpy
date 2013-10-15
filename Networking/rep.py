import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         # Create a socket object
host = socket.gethostname()
port = 1234
s.connect((host, port))
input = ""
while input != "/exit":
	input = raw_input("> ")
	s.send(input)

s.close()
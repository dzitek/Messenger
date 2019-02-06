import getopt
import sys
import threading
import socket



def client(hostAddr, portNo):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((hostAddr, int(portNo)))
	listenerFunc(sock)

def server(portNo):
	serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	serversocket.bind(('', portNo))
	serversocket.listen(5)
	soc, addr = serversocket.accept()
	listenerFunc(soc)	

def listenerFunc(soc):
	listener = Listener(soc)
	listener.start()
	while True:
		sendMsgStdin(soc, 1024)

def sendMsgStdin(soc, len):
	message = sys.stdin.readline()
	if message:
		soc.send(message.encode())
	else:
		soc.close()
		sys.exit()

def receiveMessage(soc, len):
	returnMessage = soc.recv(len).decode()
	if returnMessage:
		print("message:" + returnMessage)
	else:
		print("closing connection")
		soc.close()
		sys.exit()


class Listener(threading.Thread):
	def __init__(self,socket):
		threading.Thread.__init__(self)
		self.socket_ = socket

	def run(self):
		while True:
			returnMessage = self.socket_.recv(1024).decode()
			if returnMessage:
				print("message:" + returnMessage)
			else:
				print("closing")
				self.socket_.close()
				sys.exit()


args = sys.argv

if len(args) > 0:
	if (args[1] == "-l"):
		server(int(args[2]))
	else:
		client("localhost", int(args[1]))
		
else:
	print("error encountered")
	exit(1)
soc.close()
sock.close()


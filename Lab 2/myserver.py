import sys
from ex2utils import Server

ip = sys.argv[1]
port = int(sys.argv[2])

class myServer(Server):

    def onStart(self):
        print("Server has started")
    
    def onConnect(self, socket):
        print("User has connected")

    def onDisconnect(self, socket):
        print("User has disconnected")

server = myServer()

# Start server
server.start(ip, port)
import sys
from ex2utils import Server

ip = sys.argv[1]
port = int(sys.argv[2])

class myServer(Server):

    def __init__(self):
        super(myServer, self).__init__()
        self.users = 0

    def onStart(self):
        print("Server has started")
    
    def onConnect(self, socket):
        self.users += 1
        print(f"User has connected. Currently, {self.users} {'user is' if self.users == 1 else 'users are'} connected.")

    def onDisconnect(self, socket):
        self.users -= 1
        print(f"User has disconnected. Currently, {self.users} {'user is' if self.users == 1 else 'users are'}  connected.")

    def onMessage(self, socket, message):
        print("A User has sent a message")
        message = message.split()
        command = message[0]
        arguments = message[1:]

        print(f"command: {command}, arguments: {arguments}")
        return True


server = myServer()

# Start server
server.start(ip, port)
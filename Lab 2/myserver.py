import sys
from ex2utils import Server

ip = sys.argv[1]
port = int(sys.argv[2])

class myServer(Server):

    def __init__(self):
        super(myServer, self).__init__()
        self.users = set({})
        self.userCount = 0

    def onStart(self):
        print("Server has started")
    
    def onConnect(self, socket):
        self.userCount += 1
        socket.send(("Welcome to the chatroom! Please give yourself a name by typing /setname <name>.").encode())
        print(f"User has connected. Currently, {self.userCount} {'user is' if self.userCount == 1 else 'users are'} connected.")

    def onDisconnect(self, socket):
        self.userCount -= 1
        print(f"User has disconnected. Currently, {self.userCount} {'user is' if self.userCount == 1 else 'users are'}  connected.")

    def onMessage(self, socket, message):
        print("A User has sent a message")
        if message[0] == "/":
            message = message.split()
            command = message[0].replace("/", "")
            arguments = message[1:]

            print(f"command: {command}, arguments: {arguments}")
        
        return True


server = myServer()

# Start server
server.start(ip, port)
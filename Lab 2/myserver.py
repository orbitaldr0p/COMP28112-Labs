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
        if message[0] == "/":
            print("A user has sent a command")
            message = message.split()
            command = message[0].replace("/", "")
            arguments = message[1:]
            match command:
                case "help":
                    self.help(socket)
                case "setname":
                    self.setName(socket, arguments)
                case _:
                    self.invalid(socket)
        else:
            print("A user has sent a message")
        return True

    def invalid(self, socket):
        socket.send(("Invalid command. Type /help to get a list of commands.").encode())

    def help(self, socket):
        commands = "Available Commands:\n"\
                "/setname <username>: sets your current name in the system \n"\
                "/whisper <username> <message>: sends a message to the specified user \n"\
                "/list: lists the users that are currently online\n"\
                "/quit: exists the system \n"\
                "type something without using a command to send it to the entire system \n"\
                .encode()
        socket.send(commands)


    def setName(self,socket, arguments):
        print("setName")

server = myServer()

# Start server
server.start(ip, port)
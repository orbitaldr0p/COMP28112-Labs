import sys
from ex2utils import Server

if len(sys.argv) != 3:
    print("Usage: python ./myserver.py <ip address> <port>")
    sys.exit()

ip = sys.argv[1]
port = int(sys.argv[2])


class myServer(Server):

    def __init__(self):
        super(myServer, self).__init__()
        self.users = {}
        self.userCount = 0
        self.registeredUserCount = 0

    def onStart(self):
        print("Server has started")

    def onConnect(self, socket):
        self.userCount += 1
        socket.send(
            (
                "Welcome to the server! Please give yourself a name by typing /setname <name>."
            ).encode()
        )
        print(
            f"User has connected. Currently, {self.userCount} {'user is' if self.userCount == 1 else 'users are'} connected."
        )

    def onDisconnect(self, socket):
        self.userCount -= 1
        if socket in self.users:
            self.registeredUserCount -= 0
            quitMessage = f"{self.users[socket]} has disconnected. Currently, {self.userCount} {'user is' if self.userCount == 1 else 'users are'} connected."
            print(quitMessage)
            # self.broadcast(quitMessage)
            # WHY DOES BROADCAST CAUSE PROBLEMS HERE BUT WORKS FINE EVERYWHERE ELSE??????
            del self.users[socket]
        else:
            print(
                f"User has disconnected. Currently, {self.userCount} {'user is' if self.userCount == 1 else 'users are'} connected."
            )

    def onMessage(self, socket, message):
        if message[0] == "/":
            print("A user has sent a command")
            message = message.split()
            command = message[0].replace("/", "")
            arguments = message[1:]
            if command == "help":
                self.help(socket)
            elif command == "setname":
                self.setName(socket, arguments)
            elif command == "list":
                self.list(socket)
            elif command == "whisper":
                self.whisper(socket, arguments)
            elif command == "quit":
                self.quit(socket)
                return False
            else:
                self.invalid(socket)
        else:
            print("A user has sent a message")
            self.postMessage(socket, message)
        return True

    def invalid(self, socket):
        socket.send("Invalid command. Type /help to get a list of commands.".encode())

    def help(self, socket):
        commands = (
            "Available Commands:\n"
            "/setname <username>: sets your current name in the system \n"
            "/whisper <username> <message>: sends a message to the specified user \n"
            "/list: lists the users that are currently online\n"
            "/quit: exits the system \n"
            "/help: shows the list of valid commands \n"
            "type something without using a command to send it to everyone in the entire system \n".encode()
        )
        socket.send(commands)

    def setName(self, socket, arguments):
        if len(arguments) > 1:
            socket.send("Your username can't contain spaces!".encode())
        elif len(arguments) == 0:
            socket.send("You didn't enter a username.".encode())
        else:
            if arguments[0] in self.users.values():
                socket.send("That username is already taken!".encode())
            elif socket in self.users:
                socket.send("You have already chosen a username!".encode())
            else:
                self.registeredUserCount += 1
                socket.send(f"Your username is set to {arguments[0]}.".encode())
                self.users[socket] = arguments[0]
                self.broadcast(
                    f"{arguments[0]} Has just joined the server. Currently, {self.registeredUserCount} {'registered user is' if self.userCount == 1 else 'registered users are'} connected."
                )

    def list(self, socket):
        online = "\n".join(list(self.users.values()))
        socket.send(f"Currently online users:\n{online}".encode())

    def whisper(self, socket, arguments):
        if socket in self.users:
            if len(arguments) == 0:
                socket.send("You have not specified who the recipient is".encode())
            elif len(arguments) == 1:
                socket.send("You have not specified the message to send.".encode())
            else:
                receiver = arguments[0]
                message = " ".join(arguments[1:])
                receiverSocket = None
                for key, value in self.users.items():
                    if value == receiver:
                        receiverSocket = key
                        break
                if receiverSocket == socket:
                    socket.send("You can't whisper to yourself.".encode())
                elif receiverSocket is not None:
                    socket.send("Message Sent.".encode())
                    receiverSocket.send(
                        f"Private message from {self.users[socket]}: {message}".encode()
                    )
                else:
                    socket.send(
                        "The user you are whispering to does not exist.".encode()
                    )
        else:
            socket.send("You have not assigned yourself a name yet.".encode())

    def quit(self, socket):
        socket.send("Quitting out.".encode())
        socket.close()

    def postMessage(self, socket, message):
        if socket in self.users:
            msg = f"{self.users[socket]}: {message}"
            self.broadcast(msg)
        else:
            socket.send("You have not assigned yourself a name yet.".encode())

    def broadcast(self, msg):
        for i in self.users:
            i.send(msg.encode())


server = myServer()

# Start server
server.start(ip, port)

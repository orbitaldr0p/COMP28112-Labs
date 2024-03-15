"""
    1. cd into the directory containing myserver.py and myclient.py.
    2. Run the server by running python ./myserver.py <ip> <port>
    3. open three or more additional terminals and run python ./myclient.py <ip> <port> where the ip and port is the same as the server's
    4. You will be prompted to use /setname to give yourself a name, do so.
    5. Enter the command /help to get a list of all commands available. 
    6. To send a message to everyone in the server, just type in the message without running any commands
    7. Run /list to get a list of all users that are online
    8. Run /whisper <recipient> <message> to send a private message to the recipient
    9. Run /quit to disconnect from the server and exit the client.
"""

import sys
from ex2utils import Client

state = 1


class myClient(Client):

    def __init__(self):
        super(myClient, self).__init__()

    def onMessage(self, socket, message):
        print(message)
        return True

    def onDisconnect(self, socket):
        global state
        print("Disconnected from server")
        state = 0


if len(sys.argv) != 3:
    print("Usage: python ./myclient.py <ip address> <port>")
    sys.exit()

# Parse the IP address and port you wish to connect to.
ip = sys.argv[1]
port = int(sys.argv[2])

# Create an IRC client.
client = myClient()

# Start server
client.start(ip, port)

while True:
    if state == 0:
        break
    message = input("")
    if message.strip() == "":
        continue
    client.send(message.encode())

client.stop()

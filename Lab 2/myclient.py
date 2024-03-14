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
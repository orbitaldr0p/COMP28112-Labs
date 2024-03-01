import im
import sys
import time

class Client:
    # Colours
    RED = "\033[38;2;231;130;132m"
    GREEN = "\033[38;2;166;209;137m"
    SKY = "\033[38;2;153;209;219m"
    YELLOW = "\033[38;2;229;200;144m"
    RESET = "\033[0m"
    

    def __init__(self):
        token = None
        messageCount = None
        try:
            print("Connecting to UoM Services...")
            self.server = im.IMServerProxy("https://web.cs.manchester.ac.uk/p93974lc/comp28112_ex1/IMserver.php")
            self.server.keys()
        except:
            print(f"{self.RED}Connection to UoM Services failed.{self.RESET} \nAttempting localhost connection...")
            try:
                self.server = im.IMServerProxy("http://localhost:8080/")
                self.server.keys()
            except:
                print(f"{self.RED}Connection to localhost failed.{self.RESET} \nBailing out.")
                sys.exit()
        print("Connection Established")

    # helper functions -------------------------------------------------------------------------------
    def setStatus(self, status):
        self.server['status'] = status.encode('UTF-8')
    
    def getStatus(self):
        return self.keyContentExtract('status')

    def setTurn(self, token):
        self.server['turn'] = token.encode('UTF-8')

    def getTurn(self):
        return self.keyContentExtract('turn')

    def keyContentExtract(self, key):
        return str(self.server[key].decode('utf-8').strip())

    def leave(self):
        self.setStatus('closing')
        sys.exit()

    def closeServer(self):
        self.server.clear()
        sys.exit()

    # ------------------------------------------------------------------------------------------------

    def connect(self):
        if self.getStatus() == 'closing':
            self.server.clear()
        if len(self.server.keys()) == 1:
            self.setStatus('0')
        if self.getStatus() == '0':
            print("User 1 Connected!")
            self.setStatus('User1Connecting')
            self.token = '1'
            self.waitForUser2()
        elif self.getStatus() == 'User1Connected':
            print("User 2 Connected!")
            self.setStatus('ready')
            self.token = '2'
            self.main()
        elif self.getStatus() == 'User1Connecting':
            print("Another user is currently connecting, please try again in 1 second.")
            sys.exit()
        elif self.getStatus() == 'ready':
            print("There are already two users! Try again later.")
            sys.exit()
        else:
            sys.exit()

    def waitForUser2(self):
        try:
            self.setStatus('User1Connected')
            print("Waiting for user 2 to connect.")
            countdown = 10
            while self.getStatus() != 'ready':
                print("Timing out in", countdown, "seconds.",  end='\r')
                time.sleep(1)
                countdown -= 1
                if countdown <= 0:
                    print("User 2 connection timed out! Exiting...")
                    self.closeServer()
            print("                                                          ", end='\r')
            print("User 2 connected!")
            self.setTurn(self.token)
            self.main();
        except KeyboardInterrupt:
            print(f"{self.RED}\nKeyboard Interrupt detected, closing connection to server...{self.RESET}")
            self.closeServer()
            
    def sendMessage(self):
        try:
            self.server['message'] = ''
            countdown = 10
            if self.getStatus() == 'ready':
                message = input(f"{self.SKY}Enter a message: {self.RESET}")
                if self.getStatus() != 'closing':
                    if message == '' or message == '\n':
                        print(f"{self.RED}You can't send an empty message!{self.RESET}")
                        return
                    self.server['message'] = message
                    self.setStatus('messageSent')
                    print(f"{self.YELLOW}Waiting for other user to receive message.{self.RESET}")
                    while self.getStatus() != 'messageReceived':
                        print("Timing out in", countdown, "seconds.",  end='\r')
                        time.sleep(1)
                        countdown -= 1
                        if countdown <= 0:
                            print("Connection timed out! Quitting the server...")
                            self.leave()
                    print("                                                          ", end='\r')
                    print("Other user has received message.")
                    self.setStatus('ready')
                    return
                print(f"{self.RED}\nOther user has disconnected. Shutting down the server...{self.RESET}")
                self.closeServer()
        except KeyboardInterrupt:
            print(f"{self.RED}\nKeyboard Interrupt detected, closing connection to server...{self.RESET}")
            self.leave()

    def receiveMessage(self):
        try:
            while self.getStatus() != 'closing':
                if self.getStatus() == 'messageSent':
                    print(f"{self.YELLOW}Other user has sent a message:{self.RESET}\n"+self.keyContentExtract('message'))
                    self.setStatus('messageReceived')
                    self.setTurn(self.token)
                    return
                time.sleep(0.5)
            print(f"{self.RED}\nOther user has disconnected. Shutting down the server...{self.RESET}")
            self.closeServer()
        except KeyboardInterrupt:
            print(f"{self.RED}\nKeyboard Interrupt detected, closing connection to server...{self.RESET}")
            self.leave()

    def main(self):
        print(f"{self.GREEN}===================================================================")
        print(f"Welcome to the Simple Messaging System for Healthcare Professionals.{self.RESET}")
        try:
            while self.getStatus() != 'closing':
                if self.getTurn() == self.token:
                    self.sendMessage()
                else:
                    self.receiveMessage()
                time.sleep(0.5)
            print(f"{self.RED}\nOther user has disconnected. Shutting down the server...{self.RESET}")
            self.closeServer()
        except KeyboardInterrupt:
            print(f"{self.RED}\nKeyboard Interrupt detected, closing connection to server...{self.RESET}")
            self.leave()


client = Client()
client.connect()


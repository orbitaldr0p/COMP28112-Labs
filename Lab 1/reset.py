import im
import sys

try:
    print("Connecting to UoM Services...")
    server = im.IMServerProxy("https://web.cs.manchester.ac.uk/p93974lc/comp28112_ex1/IMserver.php")
    server.keys()
except:
    print("Connection to school systems failed. \nAttempting localhost connection...")
    try:
        server = im.IMServerProxy("http://localhost:8080/")
        server.keys()
    except:
        print("Connection to localhost failed. \nBailing out.")
        sys.exit()
print("Connection Established, clearing...")
server.clear()
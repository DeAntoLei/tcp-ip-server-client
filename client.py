# client.py application
# Sends messages with random message types to a server every 1 second until it receives end-of-messssge character
# Simulates the functionality of an MQTT client that publishes and subscribes to a topic using TCP/IP protocol
# The client terminates if it fails to establish a connection, if publishing or subscribing actions fail 
# or if 15 message are exchanged succesfully with the server

import sys, random, time, socket, pickle

# Definition of constants
TCP_IP = "127.0.0.1"
TCP_PORT = 5010
BUFFER_SIZE = 4096
CLIENT_MESSAGE_TYPES = ["onBody", "offBody", "brfChange", "enuEvent"]

class message:
    def __init__(self, *args):
        if len(args) != 0:
            self.seqNum = args[0]
            self.msgType = args[1]
            self.timestamp = time.time()
            if len(args) == 3:
                self.deviceId = args[2]
        else:
            self.seqNum = 0
            self.msgType = ""
            self.timestamp = time.time()

# Function that securely establishes a connection to a server
def connect():
    global sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print ("Connecting to %s:%d ..." % (TCP_IP, TCP_PORT))
    try:
        sock.connect((TCP_IP, TCP_PORT))
    except:
        raise Exception("Connection to %s:%d failed" % (TCP_IP, TCP_PORT))

# Function that closes a connection to a server
def closeConnection():
    global isConnected
    print ("Closing socket")
    sock.close()
    isConnected = False

# Function that enables the client to send a message to a server 
# It simulates the case when a client publishes to a topic by sending a message to a connected server
def publishMessage(msg):
    try:
        sock.send(msg)
    except:
        raise Exception("Exception in sock.send()")

# Function that securely receives data from an active server-client connection 
# It simulates the reception of a message by the broker, on a topic the client is subscribed to 
def getSubscriptionMessage():
    try:
        return sock.recv(BUFFER_SIZE)
    except:
        raise Exception("Exception from blocking sock.recv()")
 
# Socket initialization
sock = None
isConnected = False

try:
    # Establishing server-client connection
    connect()
    
    isConnected = True
    print ("Connection established")
    time.sleep(1)
    
    msgSeqNum = 0        
    response = message()
    while isConnected and response.msgType != "terminate":
        msgSeqNum += 1
        msg = message(msgSeqNum, CLIENT_MESSAGE_TYPES[random.randint(0,3)], random.randint(0, 1000))
        print ("Sending message #%d %s from %d to server at %d" % (msg.seqNum, msg.msgType, msg.deviceId, msg.timestamp))
           
        try:
            # Sending a message to the server
            publishMessage(pickle.dumps(msg))
            
            # Server response reception
            response = pickle.loads(getSubscriptionMessage())
            print ("Received message #%d %s from server at %d" % (response.seqNum, response.msgType, response.timestamp))
        except Exception as e:
            print (e)
            closeConnection()
            break
            
        time.sleep(1)
        
    time.sleep(1)
except Exception as e:
    print (e)

# Client termination    
print ("Client application will be terminated...")
sys.exit()

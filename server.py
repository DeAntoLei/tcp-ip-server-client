# server.py application
# Receives client messages and responds with random message types
# Simulates the funtionality of an MQTT broker using TCP/IP protocol and sockets
# The server can serve only 1 connection. Only terminates if socket binding fails
# Waits infinitely for a client to connect to its socket

import sys, random, time, socket, pickle

# Definition of constants
TCP_IP = "127.0.0.1"
TCP_PORT = 5010
BUFFER_SIZE = 4096
SERVER_MESSAGE_TYPES = ["erc", "drc", "res"]

class message:
    def __init__(self, *args):
        self.seqNum = args[0]
        self.msgType = args[1]
        self.timestamp = time.time()
        if len(args) == 3:
            self.deviceId = args[2]

# Function that securely binds a socket to an address
def bind():
    global sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print ("Binding to %s:%d ..." % (TCP_IP, TCP_PORT))
    try:
        sock.bind((TCP_IP, TCP_PORT))
    except socket.error as msg:
        raise Exception("Bind to %s:%d failed" % (TCP_IP, TCP_PORT), msg[0], msg[1])
    
# Function that securely receives data from an active server-client connection 
# It simulates the reception of a message, published by a client to a topic, on the broker side 
def recvTopicInfo():
    try:
        return conn.recv(BUFFER_SIZE)
    except:
        raise Exception ("Exception from conn.recv()")

# Function that securely sends data through an accepted connection
# It simulates the state where the broker forwards a message on a topic to a subscribed client
def serveTopicSubscription(msg):
    try:
        conn.send(msg)
    except:
        raise Exception ("Exception from conn.send()")

# Socket initialization
sock = None

try:
    # Socket binding
    bind()
    # Server is enabled to accept 1 connection
    sock.listen()

    while True:
        print ("Waiting for a connection client...")
        # The server accepts a connection
        conn, addr = sock.accept()
        print ("Connected to a client at ", addr[0])
        
        # Message exchange between server and client
        msgSeqNum = 0
        while True:
            try:
                # Client message reception
                data = pickle.loads(recvTopicInfo())
                print ("Received message from client: ", data.deviceId, data.seqNum, data.msgType, data.timestamp)
            
                # Server response
                msgSeqNum += 1
                if data.seqNum < 15:
                    response = message(msgSeqNum, SERVER_MESSAGE_TYPES[random.randint(0,2)])                
                else:
                    response = message(msgSeqNum, "terminate")
                print ("Response message to client: ", response.seqNum, response.msgType, response.timestamp)
                serveTopicSubscription(pickle.dumps(response))
            except Exception as e:
                print (e)
                break
            
        print ("Closing connection")
        conn.close()
except Exception as e:
    print (e)

# Server termination
print ("Server application will be terminated...")
sys.exit()

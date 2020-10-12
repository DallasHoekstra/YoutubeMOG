import socket
from _thread import *
import sys
from player import Player
import pickle



server = "192.168.0.11"
port = 5555
this_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    this_socket.bind((server, port))
except socket.error as error:
    str(error)

this_socket.listen(2)
print("Server started, waiting for a connection")

players = [Player(0,0,50,50,(255,0,0)), Player(100,100,50,50,(0,0,255))]

newPlayerID = 0
def threaded_client(connection, playerID):
    global newPlayerID
    print(playerID)
    connection.send(pickle.dumps(players[playerID]))
    reply = ""
    while True:
        try:
            # Update players position. Can you do this buffered?
            data = pickle.loads(connection.recv(2048))
            players[playerID] = data

            if not data:
                print("Disconnected")
                break
            else: 
                if playerID == 1:
                    reply = players[0]
                else:
                    reply = players[1]
                print("Received: ", data)
                print("Sending: ", reply)
                print("PlayerID# ", playerID)

            connection.sendall(pickle.dumps(reply))
        except:
            break
    print("Lost Connection")
    newPlayerID -= 1
    connection.close()

def read_position(string):
    position = string.split(",")
    return int(position[0]), int(position[1])

def make_position(tuple):
    return str(tuple[0]) + "," + str(tuple[1])


while True:
    # object, ip address
    connection, address = this_socket.accept()
    print("Connected to: ", address)
    
    start_new_thread(threaded_client, (connection, newPlayerID))
    newPlayerID += 1
    



import socket
from _thread import *
import pickle
from game import Game


server = "192.168.0.11"
port = 5555
this_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    this_socket.bind((server, port))
except socket.error as error:
    str(error)

this_socket.listen(2)
print("Server started, waiting for a connection")

# Client IP addresses
connected = set()

# dictionary of games
games = {}

# unique ID for games
idCount = 0



def threaded_client(connection, playerID, gameID):
    global idCount
    connection.send(str.encode(str(playerID)))

    reply = ""
    while True:
        try:
            data = connection.recv(4096).decode()
            
            if gameID in games:
                game = games[gameID]

                if not data:
                    print("No Data")
                    break
                else:
                    if data == "reset":
                        print("Reseting game ", gameID)
                        game.resetWent()
                    elif data != "get":
                        game.play(playerID, data)
                    
                    connection.sendall(pickle.dumps(game))
            else:
                print("Game ID not found in games list: ", gameID)
                break
        except:
            break
        
    print("Lost Connection")
    try:
        del games[gameID]
        print("Game closed ", gameID)
    except:
        print("Failed to close game ", gameID)
    idCount -= 1
    print("Next game will be ", gameID)
    connection.close()    



while True:
    # object, ip address
    connection, address = this_socket.accept()
    print("Connected to: ", address)

    idCount += 1
    playerID = 0
    gameID = (idCount - 1)//2
    if idCount % 2 == 1:
        games[gameID] = Game(gameID)
        #connection.send(pickle.dumps(games[gameID]))
        print(games[gameID])
        print("Creating a new game, waiting for second player.")
    else:
        games[gameID].ready = True
        playerID = 1
    
    start_new_thread(threaded_client, (connection, playerID, gameID))
    
    



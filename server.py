import socket
from _thread import *
from game import Player , Ball
import pickle
import pygame

server = "" # change IP here
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")


players = [Player(0,250,20,120,(255,0,0)), Player(480,250, 20,120, (0,0,255))]
ball = Ball(250, 250,10,10,(0,0,0))

def threaded_client(conn, player,ball):
    conn.send(pickle.dumps((players[player], ball)))
    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            players[player] = data[0]

            ball.move(players) # update ball position
            
            if not data:
                print("Disconnected")
                break
            else:
                # send data player and ball to client
                if player == 1:
                    reply = (players[0],ball)
                else:
                    reply = (players[1],ball)

                print("Received: ", data)
                print("Sending : ", reply)

            conn.sendall(pickle.dumps(reply))
        except:
            print(f"Error: {e}")
            break

    print("Lost connection")
    conn.close()

currentPlayer = 0
while True:
    
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, currentPlayer,ball))
    currentPlayer += 1

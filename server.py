# import socket
# from _thread import start_new_thread
# from game import Player, Ball, Score
# import pickle
# import pygame

# server = "127.0.0.1"
# port = 5555
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.bind((server, port))
# s.listen(2)
# print("Waiting for a connection, Server Started")

# SCREEN_WIDTH = 500
# SCREEN_HEIGHT = 500

# players = [
#     Player(
#         0, SCREEN_HEIGHT // 2 - 60, 20, 120, (255, 0, 0), SCREEN_WIDTH, SCREEN_HEIGHT
#     ),
#     Player(
#         SCREEN_WIDTH - 20,
#         SCREEN_HEIGHT // 2 - 60,
#         20,
#         120,
#         (0, 0, 255),
#         SCREEN_WIDTH,
#         SCREEN_HEIGHT,
#     ),
# ]
# ball = Ball(
#     SCREEN_WIDTH // 2 - 5,
#     SCREEN_HEIGHT // 2 - 5,
#     10,
#     10,
#     (0, 0, 0),
#     SCREEN_WIDTH,
#     SCREEN_HEIGHT,
# )
# score = Score()


# def threaded_client(conn, player):
#     conn.send(pickle.dumps((players[player], ball, score)))
#     while True:
#         try:
#             data = pickle.loads(conn.recv(2048))
#             players[player] = data[0]
#             ball.move(players, score)
#             if not data:
#                 break
#             if player == 1:
#                 reply = (players[0], ball, score)
#             else:
#                 reply = (players[1], ball, score)
#             conn.sendall(pickle.dumps(reply))
#         except Exception as e:
#             break
#     conn.close()


# currentPlayer = 0
# while True:
#     conn, addr = s.accept()
#     start_new_thread(threaded_client, (conn, currentPlayer))
#     currentPlayer += 1

import socket
from _thread import start_new_thread
from game import Player, Ball, Score
import pickle
import pygame

server = "127.0.0.1"
port = 5555
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((server, port))
s.listen(2)
print("Waiting for a connection, Server Started")

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

players = [
    Player(
        0, SCREEN_HEIGHT // 2 - 60, 20, 120, (255, 0, 0), SCREEN_WIDTH, SCREEN_HEIGHT
    ),
    Player(
        SCREEN_WIDTH - 20,
        SCREEN_HEIGHT // 2 - 60,
        20,
        120,
        (0, 0, 255),
        SCREEN_WIDTH,
        SCREEN_HEIGHT,
    ),
]
ball = Ball(
    SCREEN_WIDTH // 2 - 5,
    SCREEN_HEIGHT // 2 - 5,
    10,
    10,
    (0, 0, 0),
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
)
score = Score()


def threaded_client(conn, player):
    clock = pygame.time.Clock()
    conn.send(pickle.dumps((players[player], ball, score)))
    while True:
        clock.tick(60)
        try:
            data = pickle.loads(conn.recv(2048))
            players[player] = data[0]
            ball.move(players, score)
            if not data:
                break
            if player == 1:
                reply = (players[0], ball, score)
            else:
                reply = (players[1], ball, score)
            conn.sendall(pickle.dumps(reply))
        except Exception as e:
            break
    conn.close()


currentPlayer = 0
while True:
    conn, addr = s.accept()
    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1

import socket
from _thread import start_new_thread
from game import *
import pickle
import threading
import pygame

server = "127.0.0.1"
port = 5555
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((server, port))
s.listen()
print("Waiting for a connection, Server Started")

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 800

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
    50,
    50,
    (0, 0, 0),
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
)
score = Score()

list_player = List_Player()

player_slots_lock = threading.Lock()
player_slots = [False, False]


def threaded_client(conn, player_slot):
    global players, ball, score
    clock = pygame.time.Clock()
    try:
        conn.send(pickle.dumps((players[player_slot], ball, score)))
        while True:
            clock.tick(60)
            data = conn.recv(2048)
            if not data:
                break
            received_player = pickle.loads(data)
            players[player_slot] = received_player
            if (players[0].connected() and players[1].connected()):
                ball.move(players, score)

            other_player = 1 - player_slot
            reply = (players[other_player], ball, score)
            conn.sendall(pickle.dumps(reply))
    except Exception as e:
        print(f"Player {player_slot} error: {e}")
    finally:
        with player_slots_lock:
            player_slots[player_slot] = False
        print(f"Player {player_slot} disconnected")
        conn.close()


while True:
    conn, addr = s.accept()
    with player_slots_lock:
        slot = None
        for i in range(len(player_slots)):
            if not player_slots[i]:
                player_slots[i] = True
                slot = i
                break
        if slot is None:
            try:
                conn.send(pickle.dumps("FULL"))
            except:
                pass
            conn.close()
            print("Server full - connection rejected")
            continue
        
    print(f"Connected to {addr} as player {slot}")
    if score.score_player_1 >= 2 or score.score_player_2 >= 2:
        ball.x = SCREEN_WIDTH // 2 - ball.width // 2
        ball.y = SCREEN_HEIGHT // 2 - ball.height // 2
        players[0].y = SCREEN_HEIGHT // 2 - players[0].height // 2
        players[1].y = SCREEN_HEIGHT // 2 - players[1].height // 2
        score.score_player_1 = 0
        score.score_player_2 = 0
    start_new_thread(threaded_client, (conn, slot))
import socket
from _thread import start_new_thread
from game import *
import pickle
import threading
import pygame
import time, random

server = "127.0.0.1"
port = 5555
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((server, port))
s.listen()
print("Waiting for a connection, Server Started")

SCREEN_WIDTH = 960
SCREEN_HEIGHT = 600

players = [
    Player(
        0,
        SCREEN_HEIGHT // 2 - 60,
        20,
        120,
        (255, 0, 0),
        SCREEN_WIDTH,
        SCREEN_HEIGHT,
        "img/Paddle.png",
    ),
    Player(
        SCREEN_WIDTH - 20,
        SCREEN_HEIGHT // 2 - 60,
        20,
        120,
        (0, 0, 255),
        SCREEN_WIDTH,
        SCREEN_HEIGHT,
        "img/Paddle.png",
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
event_interval = 15
event_duration = 15
event_active = False
current_rule = "normal"


def threaded_client(conn, player_slot):
    global players, ball, score
    global event_timer, event_interval, event_duration, event_active, current_rule
    clock = pygame.time.Clock()

    try:
        event_timer = time.time()
        conn.send(pickle.dumps((players[player_slot], ball, score, current_rule)))
        while True:
            clock.tick(120)
            now = time.time()
            if now - event_timer >= event_interval:
                ball.countdown_event = ""
            elif now - event_timer > 14:
                ball.countdown_event = "1"
            elif now - event_timer > 13:
                ball.countdown_event = "2"
            elif now - event_timer > 12:
                ball.countdown_event = "3"

            if not event_active and now - event_timer >= event_interval:
                event_active = True
                event_timer = now
                current_rule = "paddle_score"
                print("event on")
            elif event_active and now - event_timer >= event_duration:
                event_active = False
                event_timer = now
                current_rule = "normal"
                print("normal on")
            data = conn.recv(2048)
            if not data:
                break
            received_player = pickle.loads(data)
            players[player_slot] = received_player
            if players[0].ready and players[1].ready:
                ball.move(players, score, current_rule)
                # if (score.score_player_1 != last_score_1) or (
                #     score.score_player_2 != last_score_2
                # ):
                #     players[0].skill = False
                #     players[1].skill = False
                #     last_score_1 = score.score_player_1
                #     last_score_2 = score.score_player_2
            # if players[0].skill or players[1].skill:
            #     ball.smart_skill()
            # else:
            #     ball.ability = False

            if score.score_player_1 >= 2 or score.score_player_2 >= 2:
                players[0].ready = False
                players[0].name = ""
                # players[0].skill = False
                players[1].ready = False
                players[1].name = ""
                # players[1].skill = False

            other_player = 1 - player_slot
            reply = (players[other_player], ball, score, current_rule)
            conn.sendall(pickle.dumps(reply))

    except Exception as e:
        print(f"Player {player_slot} error: {e}")
    finally:
        with player_slots_lock:
            player_slots[player_slot] = False
        print(f"Player {player_slot} disconnected")
        score.score_player_1 = 2
        score.score_player_2 = 2
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
        event_timer = 0
        now = 0
        current_rule = "normal"
        event_active = False
        ball.countdown_event = ""

    start_new_thread(threaded_client, (conn, slot))

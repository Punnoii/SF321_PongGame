import socket
from _thread import start_new_thread
from game import *
import pickle
import threading
import pygame
import time, random

server = "10.4.12.102"  # Server IP
port = 5555
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((server, port))
s.listen()
print("Waiting for a connection, Server Started")

SCREEN_WIDTH = 960
SCREEN_HEIGHT = 600
ball_lock = threading.Lock()

players = [
    Player(
        0, SCREEN_HEIGHT // 2 - 60, 30, 120, (255, 0, 0), SCREEN_WIDTH, SCREEN_HEIGHT
    ),
    Player(
        SCREEN_WIDTH - 30,
        SCREEN_HEIGHT // 2 - 60,
        30,
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
event_interval = 15
event_interval = 20
event_duration = 20
event_active = False
current_rule = "normal"
ball.current_rule = current_rule
event_on = ["event_sukuna", "event_gojo"]
event_done = True
nowevent = ""


def threaded_client(conn, player_slot):
    global players, ball, score, event_on, event_done, nowevent
    global event_timer, event_interval, event_duration, event_active, current_rule
    clock = pygame.time.Clock()

    try:
        event_timer = time.time()
        if event_done:
            randevent = random.choice(event_on)
            nowevent = randevent
        randevent = nowevent
        event_done = False
        conn.send(
            pickle.dumps((players[player_slot], ball, score, current_rule, randevent))
        )
        while True:
            data = conn.recv(2048)
            if not data:
                break
            received_player = pickle.loads(data)
            players[player_slot] = received_player
            with ball_lock:
                if players[0].ready and players[1].ready:
                    ball.move(players, score, current_rule)
                    clock.tick(60)
                    now = time.time()
                    if event_done:
                        randevent = random.choice(event_on)
                        nowevent = randevent
                    randevent = nowevent
                    event_done = False
                    if current_rule == "normal":
                        if now - event_timer >= event_interval:
                            ball.countdown_event = ""
                        elif now - event_timer > (event_interval - 1):
                            ball.countdown_event = "1"
                        elif now - event_timer > (event_interval - 2):
                            ball.countdown_event = "2"
                        elif now - event_timer > (event_interval - 3):
                            ball.countdown_event = "3"
                        elif now - event_timer > (event_interval - 4):
                            ball.countdown_event = "4"
                        elif now - event_timer > (event_interval - 5):
                            ball.countdown_event = "5"
                    else:
                        if now - event_timer >= event_duration:
                            ball.countdown_event = ""
                        elif now - event_timer > (event_duration - 1):
                            ball.countdown_event = "1"
                        elif now - event_timer > (event_duration - 2):
                            ball.countdown_event = "2"
                        elif now - event_timer > (event_duration - 3):
                            ball.countdown_event = "3"
                        elif now - event_timer > (event_duration - 4):
                            ball.countdown_event = "4"
                        elif now - event_timer > (event_duration - 5):
                            ball.countdown_event = "5"

                    if now - event_timer >= event_interval:
                        ball.countdown_event = ""
                    elif now - event_timer > 19:
                        ball.countdown_event = "1"
                    elif now - event_timer > 18:
                        ball.countdown_event = "2"
                    elif now - event_timer > 17:
                        ball.countdown_event = "3"
                    elif now - event_timer > 16:
                        ball.countdown_event = "4"
                    elif now - event_timer > 15:
                        ball.countdown_event = "5"
                    if not event_active and now - event_timer >= event_interval:
                        event_active = True
                        event_timer = now
                        current_rule = randevent
                        ball.current_rule = current_rule
                        print("------------------")
                        print(current_rule)
                        print("------------------")
                    elif event_active and now - event_timer >= event_duration:
                        event_active = False
                        event_timer = now
                        current_rule = "normal"
                        ball.current_rule = current_rule
                        print("normal on")
                        event_done = True
            if score.score_player_1 >= 7 or score.score_player_2 >= 7:
                players[0].ready = False
                players[0].name = ""
                players[1].ready = False
                players[1].name = ""

            other_player = 1 - player_slot
            reply = (players[other_player], ball, score, current_rule, randevent)
            conn.sendall(pickle.dumps(reply))
            
    except Exception as e:
        print(f"Player {player_slot} error: {e}")
    finally:

        with player_slots_lock:
            player_slots[player_slot] = False
        # print(f"Player {player_slot} disconnected, waiting 10 seconds.")

        # disconnect_time = time.time()
        # while time.time() - disconnect_time < 10:
        #     remaining_time = 10 - int(time.time() - disconnect_time)
        #     print(
        #         f"{remaining_time} sec remaining for player {player_slot} to reconnect."
        #     )
        #     time.sleep(1)
        #     with player_slots_lock:
        #         if player_slots[player_slot]:
        #             print(f"Player {player_slot} reconnected in time!")
        #             break
        # else:
        #     print(f"Player {player_slot} did not reconnect in time.")
            score.score_player_1 = 8
            score.score_player_2 = 8

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

    if score.score_player_1 >= 7 or score.score_player_2 >= 7:
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

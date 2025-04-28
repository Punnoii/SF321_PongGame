import pygame
from network import Network
from game import *
import random

pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=1024)
pygame.init()
pygame.mixer.init()

enter_sound = pygame.mixer.Sound("sound/enter.mp3")
eventSukuna_sound = pygame.mixer.Sound("sound/event_sukuna.mp3")
eventGojo_sound = pygame.mixer.Sound("sound/event_gojo.mp3")
background_sound = pygame.mixer.Sound("sound/background.mp3")

eventGojo_sound.set_volume(0.05)
eventSukuna_sound.set_volume(0.05)

SCREEN_WIDTH = 960
SCREEN_HEIGHT = 600

win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong Client")

basic_font = pygame.font.Font("Merienda.ttf", 30)

enter_sound.set_volume(0.3)

accent_color = (0, 0, 0)
button_hover_color = (0, 255, 0)
button_color = (0, 200, 0)
button_text_color = (255, 255, 255)


start_button = pygame.Rect(SCREEN_WIDTH // 2 - 125, SCREEN_HEIGHT // 2 + 25, 250, 233)
play_button = pygame.Rect(SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 - 35, 300, 178)
next_button = pygame.Rect(SCREEN_WIDTH // 2 - 50, (SCREEN_HEIGHT // 2) + 100, 100, 115)
back_button = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 150, 300, 178)

start_img = pygame.transform.scale(
    pygame.image.load("img/start_button.png"), (250, 233)
)
start_hover = pygame.transform.scale(
    pygame.image.load("img/start_button.png"), (270, 252)
)
next_img = pygame.transform.scale(pygame.image.load("img/next.png"), (100, 129))
next_hover = pygame.transform.scale(pygame.image.load("img/next.png"), (120, 154))
logo = pygame.transform.scale(pygame.image.load("img/Logo.png"), (250, 187))
background_main = pygame.transform.scale(
    pygame.image.load("img/background.png"), (SCREEN_WIDTH, SCREEN_HEIGHT)
)
background_fight = pygame.transform.scale(
    pygame.image.load("img/pong_background.png"), (SCREEN_WIDTH, SCREEN_HEIGHT)
)
background_lobby = pygame.transform.scale(
    pygame.image.load("img/background_lobby.png"), (SCREEN_WIDTH, SCREEN_HEIGHT)
)
background_wait = pygame.transform.scale(
    pygame.image.load("img/waitting.png"), (SCREEN_WIDTH, SCREEN_HEIGHT)
)
background_skill_sukuna = pygame.transform.scale(
    pygame.image.load("img/background_event_sukuna.png"), (SCREEN_WIDTH, SCREEN_HEIGHT)
)
background_skill_gojo = pygame.transform.scale(
    pygame.image.load("img/background_event_gojo.png"), (SCREEN_WIDTH, SCREEN_HEIGHT)
)
background_fullserver = pygame.transform.scale(
    pygame.image.load("img/fullserver.png"), (SCREEN_WIDTH, SCREEN_HEIGHT)
)
background_no_player_connect = pygame.transform.scale(
    pygame.image.load("img/background_other_player_disconnect.png"),
    (SCREEN_WIDTH, SCREEN_HEIGHT),  # pun adding
)
background_input = pygame.transform.scale(
    pygame.image.load("img/background_input.png"), (SCREEN_WIDTH, SCREEN_HEIGHT)
)
play_again = pygame.transform.scale(pygame.image.load("img/play_again.png"), (300, 101))
play_again_hover = pygame.transform.scale(
    pygame.image.load("img/play_again.png"), (320, 107)
)
victory_img = pygame.transform.scale(
    pygame.image.load("img/victory.png"), (SCREEN_WIDTH, SCREEN_HEIGHT)
)
defeat_img = pygame.transform.scale(
    pygame.image.load("img/defeat.png"), (SCREEN_WIDTH, SCREEN_HEIGHT)
)
event_sukuna = pygame.transform.scale(
    pygame.image.load("img/event_sukuna.png"), (500, 276)  # 1.81
)
event_gojo = pygame.transform.scale(
    pygame.image.load("img/event_gojo.png"), (500, 180)  # 2.77
)

def rand_win():
    winner_sounds = pygame.mixer.Sound(f"sound/win_sound{random.randint(1,3)}.mp3")
    winner_sounds.set_volume(0.05)
    winner_sounds.play()
def rand_lose():
    loser_sounds = pygame.mixer.Sound(f"sound/lose_sound{random.randint(1,3)}.mp3")
    loser_sounds.set_volume(0.05)
    loser_sounds.play()

background_sound.play(-1)


def start_screen():
    background_sound.set_volume(0.05)
    rand_win()
    rand_lose()
    while True:
        win.blit(background_main, (0, 0))
        win.blit(logo, (30, start_button.y // 10))
        mouse = pygame.mouse.get_pos()
        if start_button.collidepoint(mouse):
            win.blit(start_hover, (start_button.x - 10, start_button.y - 10))
        else:
            win.blit(start_img, (start_button.x, start_button.y))
        pygame.display.update()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                return False
            if e.type == pygame.MOUSEBUTTONDOWN and start_button.collidepoint(e.pos):
                enter_sound.play()
                return True


def name_input_screen():
    active = False
    text_input = ""
    backspace_held = False
    backspace_start = backspace_last = 0
    toggle = True
    last_toggle = pygame.time.get_ticks()
    input_box = pygame.Rect((SCREEN_WIDTH // 4) - 10, (SCREEN_HEIGHT // 2) - 5, 500, 40)

    while True:
        win.blit(background_input, (0, 0))
        pygame.draw.rect(
            win, (200, 200, 200) if not active else (255, 255, 255), input_box, 2
        )
        now = pygame.time.get_ticks()
        if now - last_toggle >= 500:
            toggle = not toggle
            last_toggle = now
        disp = text_input + ("_" if active and toggle else "")
        txt = basic_font.render(disp, True, accent_color)
        win.blit(txt, (input_box.x + 5, input_box.y))
        mouse = pygame.mouse.get_pos()
        if next_button.collidepoint(mouse):
            win.blit(next_hover, (next_button.x - 10, next_button.y - 10))
        else:
            win.blit(next_img, (next_button.x, next_button.y))
        pygame.display.update()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                return None
            if e.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(e.pos):
                    active = True
                else:
                    active = False
                if next_button.collidepoint(e.pos) and text_input.strip():
                    enter_sound.play()
                    return text_input.strip()
            if e.type == pygame.KEYDOWN and active:
                if e.key == pygame.K_BACKSPACE:
                    if not backspace_held:
                        backspace_held = True
                        backspace_start = backspace_last = now
                        text_input = text_input[:-1]
                    elif now - backspace_start >= 400 and now - backspace_last >= 50:
                        text_input = text_input[:-1]
                        backspace_last = now
                elif e.key == pygame.K_RETURN and text_input.strip():
                    return text_input.strip()
                elif len(text_input) < 15 and e.unicode.isprintable():
                    text_input += e.unicode
            if e.type == pygame.KEYUP and e.key == pygame.K_BACKSPACE:
                backspace_held = False


def lobby_screen(name):
    while True:
        win.blit(background_lobby, (0, 0))
        info = basic_font.render(f"Player: {name}", True, (255, 255, 255))
        win.blit(info, (SCREEN_WIDTH // 2 - info.get_width() // 2, 300))
        mouse = pygame.mouse.get_pos()
        if next_button.collidepoint(mouse):
            win.blit(next_hover, (next_button.x - 10, next_button.y - 10))
        else:
            win.blit(next_img, (next_button.x, next_button.y))
        pygame.display.update()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                return False
            if e.type == pygame.MOUSEBUTTONDOWN and next_button.collidepoint(e.pos):
                enter_sound.play()
                return True


def show_server_full_screen():
    screen_width, screen_height = win.get_size()
    play_again_rect = play_again.get_rect(
        bottomright=(screen_width - 10, screen_height - 10)
    )
    while True:
        win.blit(background_fullserver, (0, 0))
        mouse = pygame.mouse.get_pos()
        if play_again_rect.collidepoint(mouse):
            win.blit(
                play_again_hover,
                play_again.get_rect(
                    bottomright=(screen_width - 20, screen_height - 20)
                ),
            )
        else:
            win.blit(play_again, play_again_rect)
        pygame.display.update()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                return False
            if e.type == pygame.MOUSEBUTTONDOWN and play_again_rect.collidepoint(e.pos):
                return True


def show_other_player_disconnect_screen():
    screen_width, screen_height = win.get_size()
    play_again_rect = play_again.get_rect(
        bottomright=(screen_width - 10, screen_height - 10)
    )
    while True:
        win.blit(background_no_player_connect, (0, 0))
        mouse = pygame.mouse.get_pos()
        if play_again_rect.collidepoint(mouse):
            win.blit(
                play_again_hover,
                play_again.get_rect(
                    bottomright=(screen_width - 20, screen_height - 20)
                ),
            )
        else:
            win.blit(play_again, play_again_rect)
        pygame.display.update()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                return False
            if e.type == pygame.MOUSEBUTTONDOWN and play_again_rect.collidepoint(e.pos):
                return True


event_start_time = None
fade_done = False


def redraw_window(player, player2, ball, score, current_rule, randevent):
    global event_start_time, fade_done

    win.blit(background_fight, (0, 0))

    if player.color == (255, 0, 0):
        r_txt = f"{player.name}: {score.score_player_1}"
        b_txt = f"{player2.name}: {score.score_player_2}"
    else:
        r_txt = f"{player2.name}: {score.score_player_1}"
        b_txt = f"{player.name}: {score.score_player_2}"

    rt = basic_font.render(r_txt, True, (255, 0, 0))
    bt2 = basic_font.render(b_txt, True, (0, 0, 255))
    win.blit(rt, (10, 10))
    win.blit(bt2, (SCREEN_WIDTH - bt2.get_width() - 10, 10))

    if not (player.ready and player2.ready):
        win.blit(background_wait, (0, 0))
        if score.score_player_1 >= 8 or score.score_player_2 >= 8:
            if show_other_player_disconnect_screen():
                return
    else:
        background_sound.set_volume(0)
        if ball.countdown_event != "" and not fade_done:
            if current_rule == "normal":
                if randevent == "event_sukuna":
                    if event_start_time is None:
                        event_start_time = pygame.time.get_ticks()
                    if eventSukuna_sound.get_num_channels() == 0 and not fade_done:
                        eventSukuna_sound.play(fade_ms=500)
                    fade_surface = pygame.Surface((500, 276), pygame.SRCALPHA)
                    current_time = pygame.time.get_ticks()
                    elapsed_time = (current_time - event_start_time) / 1000

                    if elapsed_time <= 1:
                        alpha = int(255 * (elapsed_time / 1))
                    elif elapsed_time <= 4:
                        alpha = 255
                    else:
                        fade_time = elapsed_time - 4
                        alpha = max(255 - int(fade_time * 255 / 2), 0)

                    fade_surface.set_alpha(alpha)
                    fade_surface.blit(event_sukuna, (0, 0))
                    win.blit(
                        fade_surface,
                        ((SCREEN_WIDTH // 2) - 250, SCREEN_HEIGHT // 2 - 107),
                    )

                    if elapsed_time > 6:
                        fade_done = True
                elif randevent == "event_gojo":
                    if event_start_time is None:
                        event_start_time = pygame.time.get_ticks()
                    if eventGojo_sound.get_num_channels() == 0 and not fade_done:
                        eventGojo_sound.play(fade_ms=500)
                    fade_surface = pygame.Surface((500, 276), pygame.SRCALPHA)
                    current_time = pygame.time.get_ticks()
                    elapsed_time = (current_time - event_start_time) / 1000

                    if elapsed_time <= 1:
                        alpha = int(255 * (elapsed_time / 1))
                    elif elapsed_time <= 4:
                        alpha = 255
                    else:
                        fade_time = elapsed_time - 4
                        alpha = max(255 - int(fade_time * 255 / 2), 0)

                    fade_surface.set_alpha(alpha)
                    fade_surface.blit(event_gojo, (0, 0))
                    win.blit(
                        fade_surface,
                        ((SCREEN_WIDTH // 2) - 250, SCREEN_HEIGHT // 2 - 107),
                    )

                    if elapsed_time > 6:
                        fade_done = True

                countdown = basic_font.render(ball.countdown_event, True, (255, 215, 0))
                win.blit(
                    countdown, (SCREEN_WIDTH // 2 - countdown.get_width() // 2, 80)
                )

        if current_rule == "event_sukuna":
            win.blit(background_skill_sukuna, (0, 0))
            ball.changeBall = "event_sukuna"
            if ball.countdown_event != "":
                countdown = basic_font.render(ball.countdown_event, True, (255, 215, 0))
                win.blit(
                    countdown, (SCREEN_WIDTH // 2 - countdown.get_width() // 2, 80)
                )
            win.blit(rt, (10, 10))
            win.blit(bt2, (SCREEN_WIDTH - bt2.get_width() - 10, 10))
            alert = basic_font.render("event", True, (255, 215, 0))
            win.blit(alert, (SCREEN_WIDTH // 2 - alert.get_width() // 2, 50))
            event_start_time = None
            fade_done = False
        if current_rule == "event_gojo":
            player.vel = 3
            win.blit(background_skill_gojo, (0, 0))
            ball.changeBall = "event_gojo"
            if ball.countdown_event != "":
                countdown = basic_font.render(ball.countdown_event, True, (255, 215, 0))
                win.blit(
                    countdown, (SCREEN_WIDTH // 2 - countdown.get_width() // 2, 80)
                )
            win.blit(rt, (10, 10))
            win.blit(bt2, (SCREEN_WIDTH - bt2.get_width() - 10, 10))
            alert = basic_font.render("event", True, (255, 215, 0))
            win.blit(alert, (SCREEN_WIDTH // 2 - alert.get_width() // 2, 50))
            event_start_time = None
            fade_done = False

        player.draw(win)
        player2.draw(win)
        ball.draw(win)

    pygame.display.update()

sound_running = True
def show_winner_screen(player, score):
    global sound_running
    eventSukuna_sound.set_volume(0)
    eventGojo_sound.set_volume(0)
    screen_width, screen_height = win.get_size()
    play_again_rect = play_again.get_rect(
        bottomright=(screen_width - 10, screen_height - 10)
    )

    is_winner = False
    if player.color == (255, 0, 0):
        is_winner = score.score_player_1 >= 7
    else:
        is_winner = score.score_player_2 >= 7

    while True:
        if is_winner:
            win.blit(victory_img, (0, 0))
            if sound_running:
                rand_win()
                sound_running = False
        else:
            win.blit(defeat_img, (0, 0))
            if sound_running:
                rand_lose()
                sound_running = False
        mouse = pygame.mouse.get_pos()
        if play_again_rect.collidepoint(mouse):
            win.blit(
                play_again_hover,
                play_again.get_rect(
                    bottomright=(screen_width - 20, screen_height - 20)
                ),
            )
        else:
            win.blit(play_again, play_again_rect)

        pygame.display.update()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                return False
            if e.type == pygame.MOUSEBUTTONDOWN:
                return True


def main(player_name):
    net = Network()
    init = net.getP()
    if init == "FULL":
        if not show_server_full_screen():
            return
        else:
            return
    if not init:
        return
    player, ball, score, current_rule, randevent = init
    player.name = player_name
    player.ready = True
    clock = pygame.time.Clock()
    while True:
        clock.tick(60)
        response = net.send(player)
        if not response:
            break
        player2, ball, score, current_rule, randevent = response

        event_list = pygame.event.get()
        for e in event_list:
            if e.type == pygame.QUIT:
                net.close()
                pygame.quit()
                return
        player.move(event_list)
        ball.move([player, player2], score, current_rule)
        redraw_window(player, player2, ball, score, current_rule, randevent)
        if current_rule == "normal":
            player.vel = 10
            player2.vel = 10
            ball.changeBall = "normal"
        if score.score_player_1 >= 7 or score.score_player_2 >= 7:
            if show_winner_screen(player, score):
                return


while True:
    if not start_screen():
        break
    name = name_input_screen()
    if not name:
        break
    if not lobby_screen(name):
        break
    main(name)

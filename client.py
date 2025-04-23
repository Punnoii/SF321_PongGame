import pygame
from network import Network
from game import *

pygame.init()
pygame.mixer.init()

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


start_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 25, 250, 233)
play_button = pygame.Rect(SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 - 35, 300, 178)
next_button = pygame.Rect(SCREEN_WIDTH // 2 - 50, (SCREEN_HEIGHT // 2) + 100, 100, 115)
back_button = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 150, 300, 178)

start_img = pygame.transform.scale(
    pygame.image.load("img/start_button.png"), (250, 233)
)
start_hover = pygame.transform.scale(
    pygame.image.load("img/start_button.png"), (270, 252)
)
next_img = pygame.transform.scale(pygame.image.load("img/next.png"), (100, 115))
next_hover = pygame.transform.scale(pygame.image.load("img/next.png"), (120, 138))


def start_screen():
    background = pygame.transform.scale(
        pygame.image.load("img/background.png"), (SCREEN_WIDTH, SCREEN_HEIGHT)
    )
    while True:
        logo = pygame.transform.scale(pygame.image.load("img/Logo.png"), (500, 240))
        win.blit(background, (0, 0))
        win.blit(logo, (start_button.x - 120, start_button.y // 10))
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
    background = pygame.transform.scale(
        pygame.image.load("img/background_input.png"), (SCREEN_WIDTH, SCREEN_HEIGHT)
    )

    while True:
        win.blit(background, (0, 0))
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
    background = pygame.transform.scale(
        pygame.image.load("img/background_lobby.png"), (SCREEN_WIDTH, SCREEN_HEIGHT)
    )
    while True:
        win.blit(background, (0, 0))
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
    while True:
        win.fill((135, 206, 250))
        msg = basic_font.render("Server Full", True, (255, 0, 0))
        win.blit(msg, (SCREEN_WIDTH // 2 - msg.get_width() // 2, 100))
        sub = basic_font.render("Please try again later.", True, (255, 255, 255))
        win.blit(sub, (SCREEN_WIDTH // 2 - sub.get_width() // 2, 200))
        mouse = pygame.mouse.get_pos()
        if back_button.collidepoint(mouse):
            win.blit(next_hover, (back_button.x - 10, back_button.y - 10))
        else:
            win.blit(next_img, (back_button.x, back_button.y))
        pygame.display.update()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                return False
            if e.type == pygame.MOUSEBUTTONDOWN and back_button.collidepoint(e.pos):
                return True


def redraw_window(player, player2, ball, score):
    win.fill((255, 255, 255))
    SKILL_DISPLAY_TIME = 1000
    skill_color = (255, 255, 0)
    bg = pygame.transform.scale(
        pygame.image.load("img/pong_background.png"), (SCREEN_WIDTH, SCREEN_HEIGHT)
    )
    win.blit(bg, (0, 0))
    if player.color == (255, 0, 0):
        r_txt = f"{player.name}: {score.score_player_1}"
        b_txt = f"{player2.name}: {score.score_player_2}"
    else:
        r_txt = f"{player2.name}: {score.score_player_1}"
        b_txt = f"{player.name}: {score.score_player_2}"
    # if ball.ability:
    #     skill_text = basic_font.render("E", True, skill_color)
    #     tx = SCREEN_WIDTH // 2 - skill_text.get_width() // 2
    #     ty = SCREEN_HEIGHT // 2 - skill_text.get_height() // 2
    #     win.blit(skill_text, (tx, ty))
    rt = basic_font.render(r_txt, True, (255, 0, 0))
    bt2 = basic_font.render(b_txt, True, (0, 0, 255))
    win.blit(rt, (10, 10))
    win.blit(bt2, (SCREEN_WIDTH - bt2.get_width() - 10, 10))
    if not (player.ready and player2.ready):
        w = pygame.transform.scale(
            pygame.image.load("img/waitting.png"), (SCREEN_WIDTH, SCREEN_HEIGHT)
        )
        win.blit(w, (0, 0))
    else:
        player.draw(win)
        player2.draw(win)
        ball.draw(win)
    pygame.display.update()


def show_winner_screen(player, player2, score):
    play_again = pygame.Rect(SCREEN_WIDTH // 2 - 225, SCREEN_HEIGHT // 2, 200, 115)

    victory_img = pygame.transform.scale(
        pygame.image.load("img/victory.png"), (SCREEN_WIDTH, SCREEN_HEIGHT)
    )
    defeat_img = pygame.transform.scale(
        pygame.image.load("img/defeat.png"), (SCREEN_WIDTH, SCREEN_HEIGHT)
    )
    play_again_img = pygame.transform.scale(
        pygame.image.load("img/play_again.png"), (200, 115)
    )
    play_again_img_hover = pygame.transform.scale(
        pygame.image.load("img/play_again.png"), (220, 127)
    )
    screen_width, screen_height = win.get_size()
    play_again_rect = play_again_img.get_rect(
        bottomright=(screen_width - 10, screen_height - 10)
    )

    is_winner = False
    if player.color == (255, 0, 0):
        is_winner = score.score_player_1 >= 2
    else:
        is_winner = score.score_player_2 >= 2

    while True:
        if is_winner:
            win.blit(victory_img, (0, 0))
        else:
            win.blit(defeat_img, (0, 0))

        mouse = pygame.mouse.get_pos()
        if play_again_rect.collidepoint(mouse):
            win.blit(
                play_again_img_hover,
                play_again_img.get_rect(
                    bottomright=(screen_width - 20, screen_height - 20)
                ),
            )
        else:
            win.blit(play_again_img, play_again_rect)

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
    player, ball, score = init
    player.name = player_name
    player.ready = True
    clock = pygame.time.Clock()
    while True:
        clock.tick(120)
        response = net.send(player)
        if not response:
            break
        player2, ball, score = response
        redraw_window(player, player2, ball, score)

        if score.score_player_1 >= 2 or score.score_player_2 >= 2:
            if show_winner_screen(player, player2, score):
                return
        event_list = pygame.event.get()
        for e in event_list:
            if e.type == pygame.QUIT:
                pygame.quit()
                return
        player.move(event_list)
        ball.move([player, player2], score)


while True:
    if not start_screen():
        break
    name = name_input_screen()
    if not name:
        break
    if not lobby_screen(name):
        break
    main(name)

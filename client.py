import pygame
from network import Network
from game import *

pygame.init()
pygame.mixer.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 800
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Client")

basic_font = pygame.font.SysFont("comicsans", 30)
accent_color = (0, 0, 0)
button_font = pygame.font.SysFont("comicsans", 40)
button_color = (0, 200, 0)
button_hover_color = (0, 255, 0)
button_text_color = (255, 255, 255)

start_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 60)
next_button_rect = pygame.Rect(
    SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 100, 200, 60
)
start_button = pygame.Rect(SCREEN_WIDTH // 1.5, SCREEN_HEIGHT // 2, 300, 178)


def draw_start_screen():
    background = pygame.image.load("Welcome.png")
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    start_button_image = pygame.image.load("start_button.png")
    start_button_image = pygame.transform.scale(start_button_image, (300, 178))
    start_button_hover_image = pygame.transform.scale(start_button_image, (320, 190))
    win.blit(background, (0, 0))
    win.blit(start_button_image, (start_button.x, start_button.y))

    mouse_pos = pygame.mouse.get_pos()
    if start_button.collidepoint(mouse_pos):
        win.blit(start_button_hover_image, (start_button.x - 10, start_button.y - 10))
    else:
        win.blit(start_button_image, (start_button.x, start_button.y))
    pygame.display.update()


def start_screen():
    run = True
    while run:
        draw_start_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    run = False


def name_input_screen():
    input_box = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 30, 300, 60)
    active = False
    user_text = ""
    run = True
    cursor_visible = True
    last_toggle = pygame.time.get_ticks()
    toggle_interval = 500

    while run:
        current_time = pygame.time.get_ticks()
        if current_time - last_toggle >= toggle_interval:
            cursor_visible = not cursor_visible
            last_toggle = current_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return ""
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = True
                else:
                    active = False
                if next_button_rect.collidepoint(event.pos):
                    if user_text.strip() != "":
                        run = False
            if event.type == pygame.KEYDOWN and active:
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                elif event.key == pygame.K_RETURN:
                    if user_text.strip() != "":
                        run = False
                else:
                    user_text += event.unicode

        win.fill((30, 30, 30))
        prompt_text = basic_font.render("Enter your name:", True, (255, 255, 255))
        win.blit(
            prompt_text,
            (
                SCREEN_WIDTH // 2 - prompt_text.get_width() // 2,
                SCREEN_HEIGHT // 2 - 100,
            ),
        )

        display_text = user_text
        if active and cursor_visible:
            display_text += "_"

        pygame.draw.rect(
            win, (255, 255, 255) if active else (200, 200, 200), input_box, 2
        )
        text_surface = basic_font.render(display_text, True, (255, 255, 255))
        win.blit(text_surface, (input_box.x + 5, input_box.y + 5))

        mouse_pos = pygame.mouse.get_pos()
        if next_button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(win, button_hover_color, next_button_rect)
        else:
            pygame.draw.rect(win, button_color, next_button_rect)
        next_text = button_font.render("Next", True, button_text_color)
        win.blit(
            next_text,
            (
                next_button_rect.centerx - next_text.get_width() // 2,
                next_button_rect.centery - next_text.get_height() // 2,
            ),
        )
        pygame.display.flip()

    return user_text


def lobby_screen(player_name):
    run = True
    while run:
        win.fill((128, 128, 128))
        title_font = pygame.font.SysFont("comicsans", 60)
        title_text = title_font.render("Lobby", True, (255, 255, 255))
        win.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))

        name_text = basic_font.render(
            "Your Name: " + player_name, True, (255, 255, 255)
        )
        win.blit(name_text, (SCREEN_WIDTH // 2 - name_text.get_width() // 2, 200))

        mouse_pos = pygame.mouse.get_pos()
        if start_button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(win, button_hover_color, start_button_rect)
        else:
            pygame.draw.rect(win, button_color, start_button_rect)
        join_text = button_font.render("Join Room", True, button_text_color)
        win.blit(
            join_text,
            (
                start_button_rect.centerx - join_text.get_width() // 2,
                start_button_rect.centery - join_text.get_height() // 2,
            ),
        )
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    run = False
    main(player_name)


def redraw_window(screen, player, player2, ball, score):
    screen.fill((255, 255, 255))
    background = pygame.image.load("pong_background.png")
    background = pygame.transform.scale(
        background, (SCREEN_WIDTH, SCREEN_HEIGHT + BAR_HEIGHT)
    )
    win.blit(background, (0, 0))

    pygame.draw.rect(screen, (200, 200, 200), (0, 0, SCREEN_WIDTH, BAR_HEIGHT))

    info_font = pygame.font.SysFont("comicsans", 24)
    if player.color == (255, 0, 0):
        red_info = f"{player.name} - {score.score_player_1}"
        blue_info = f"{player2.name} - {score.score_player_2}"
    else:
        red_info = f"{player2.name} - {score.score_player_1}"
        blue_info = f"{player.name} - {score.score_player_2}"
    red_text = info_font.render(red_info, True, (255, 0, 0))
    blue_text = info_font.render(blue_info, True, (0, 0, 255))
    screen.blit(red_text, (10, 10))
    screen.blit(blue_text, (SCREEN_WIDTH - blue_text.get_width() - 10, 10))

    if not (player.connected() and player2.connected()):
        waiting_font = pygame.font.SysFont("comicsans", 40)
        waiting_text = waiting_font.render("Waiting for Player...", True, (255, 0, 0))
        screen.blit(
            waiting_text,
            (
                SCREEN_WIDTH // 2 - waiting_text.get_width() // 2,
                (SCREEN_HEIGHT + BAR_HEIGHT) // 2 - waiting_text.get_height() // 2,
            ),
        )
    else:
        player.draw(screen)
        player2.draw(screen)
        ball.draw(screen)
        if not ball.active and ball.countdown_number != "":
            countdown_text = basic_font.render(
                str(ball.countdown_number), True, accent_color
            )
            countdown_rect = countdown_text.get_rect(
                center=(SCREEN_WIDTH / 2, (SCREEN_HEIGHT + BAR_HEIGHT) // 2 + 50)
            )
            screen.blit(countdown_text, countdown_rect)
    pygame.display.update()


def show_winner_screen(win, player, player2, score):
    waiting = True
    while waiting:
        win.fill((0, 0, 0))

        if score.score_player_1 >= 2:
            winner_name = player.name if player.color == (255, 0, 0) else player2.name
        else:
            winner_name = player2.name if player.color == (255, 0, 0) else player.name

        winner_font = pygame.font.SysFont("comicsans", 50)
        winner_text = winner_font.render(f"{winner_name} Wins!", True, (255, 255, 255))

        win.blit(
            winner_text,
            (
                SCREEN_WIDTH // 2 - winner_text.get_width() // 2,
                SCREEN_HEIGHT // 2 - 100,
            ),
        )

        mouse_pos = pygame.mouse.get_pos()
        if start_button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(win, button_hover_color, start_button_rect)
        else:
            pygame.draw.rect(win, button_color, start_button_rect)

        button_text = button_font.render("Play Again", True, button_text_color)
        win.blit(
            button_text,
            (
                start_button_rect.centerx - button_text.get_width() // 2,
                start_button_rect.centery - button_text.get_height() // 2,
            ),
        )

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    run_game_flow()
                    return


def main(player_name):
    network = Network()
    player, ball, score = network.getP()
    player.ready = True
    player.name = player_name
    clock = pygame.time.Clock()
    game_over = False
    run = True
    while run:
        clock.tick(60)
        player2, ball, score = network.send((player, ball, score))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        if score.score_player_1 >= 2 or score.score_player_2 >= 2:
            game_over = True

        if not game_over:
            player.move()
            redraw_window(win, player, player2, ball, score)
        else:
            game_over = False
            show_winner_screen(win, player, player2, score)

        player.move()
        redraw_window(win, player, player2, ball, score)


def run_game_flow():
    start_screen()
    player_name = name_input_screen()
    lobby_screen(player_name)


while True:
    run_game_flow()

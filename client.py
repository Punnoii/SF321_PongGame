# ---------------------------------------ver1..Byปั้น-----------------------------------------------
# import pygame
# from network import Network
# from game import Player, Ball, Score

# pygame.init()
# SCREEN_WIDTH = 500
# SCREEN_HEIGHT = 500
# win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# pygame.display.set_caption("Client")


# def redraw_window(screen, player, player2, ball, score):
#     screen.fill((255, 255, 255))
#     if not (player.connected() and player2.connected()):
#         font = pygame.font.SysFont("comicsans", 40)
#         text = font.render("Waiting for Player...", True, (255, 0, 0))
#         screen.blit(
#             text,
#             (
#                 SCREEN_WIDTH // 2 - text.get_width() // 2,
#                 SCREEN_HEIGHT // 2 - text.get_height() // 2,
#             ),
#         )
#     else:
#         player.draw(screen)
#         player2.draw(screen)
#         ball.draw(screen)
#         font = pygame.font.SysFont("comicsans", 30)
#         red_text = font.render(f"Red: {score.score_player_1}", True, (255, 0, 0))
#         blue_text = font.render(f"Blue: {score.score_player_2}", True, (0, 0, 255))
#         screen.blit(red_text, (10, 10))
#         screen.blit(blue_text, (SCREEN_WIDTH - blue_text.get_width() - 10, 10))
#     pygame.display.update()


# def main():
#     network = Network()
#     player, ball, score = network.getP()
#     player.ready = True
#     clock = pygame.time.Clock()
#     run = True
#     while run:
#         clock.tick(60)
#         player2, ball, score = network.send((player, ball, score))
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 run = False
#                 pygame.quit()
#         player.move()
#         redraw_window(win, player, player2, ball, score)


# def menu_screen():
#     clock = pygame.time.Clock()
#     run = True
#     while run:
#         clock.tick(60)
#         win.fill((128, 128, 128))
#         font = pygame.font.SysFont("comicsans", 60)
#         text = font.render("Click to Play!", True, (255, 0, 0))
#         win.blit(
#             text,
#             (
#                 SCREEN_WIDTH // 2 - text.get_width() // 2,
#                 SCREEN_HEIGHT // 2 - text.get_height() // 2,
#             ),
#         )
#         pygame.display.update()
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 run = False
#                 pygame.quit()
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 run = False
#     main()


# while True:
#     menu_screen()

# ---------------------------------------ver1..Byปั้น-----------------------------------------------
# ---------------------------------------ver2..นับเวลา-----------------------------------------------

# import pygame
# from network import Network
# from game import *

# pygame.init()
# SCREEN_WIDTH = 500
# SCREEN_HEIGHT = 500
# win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# pygame.display.set_caption("Client")

# basic_font = pygame.font.SysFont("comicsans", 30)
# accent_color = (0, 0, 0)


# def redraw_window(screen, player, player2, ball, score):
#     screen.fill((255, 255, 255))
#     if not (player.connected() and player2.connected()):
#         font = pygame.font.SysFont("comicsans", 40)
#         text = font.render("Waiting for Player...", True, (255, 0, 0))
#         screen.blit(
#             text,
#             (
#                 SCREEN_WIDTH // 2 - text.get_width() // 2,
#                 SCREEN_HEIGHT // 2 - text.get_height() // 2,
#             ),
#         )
#     else:
#         player.draw(screen)
#         player2.draw(screen)
#         ball.draw(screen)
#         font = pygame.font.SysFont("comicsans", 30)
#         red_text = font.render(f"Red: {score.score_player_1}", True, (255, 0, 0))
#         blue_text = font.render(f"Blue: {score.score_player_2}", True, (0, 0, 255))
#         screen.blit(red_text, (10, 10))
#         screen.blit(blue_text, (SCREEN_WIDTH - blue_text.get_width() - 10, 10))
#         if not ball.active and ball.countdown_number != "":
#             countdown_text = basic_font.render(
#                 str(ball.countdown_number), True, accent_color
#             )
#             countdown_rect = countdown_text.get_rect(
#                 center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50)
#             )
#             screen.blit(countdown_text, countdown_rect)
#     pygame.display.update()


# def main():
#     network = Network()
#     player, ball, score = network.getP()
#     player.ready = True
#     clock = pygame.time.Clock()
#     run = True
#     while run:
#         clock.tick(60)

#         player2, ball, score = network.send((player, ball, score))
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 run = False
#                 pygame.quit()
#         player.move()
#         redraw_window(win, player, player2, ball, score)


# def menu_screen():
#     clock = pygame.time.Clock()
#     run = True
#     while run:
#         clock.tick(60)
#         win.fill((128, 128, 128))
#         font = pygame.font.SysFont("comicsans", 60)
#         text = font.render("Click to Play!", True, (255, 0, 0))
#         win.blit(
#             text,
#             (
#                 SCREEN_WIDTH // 2 - text.get_width() // 2,
#                 SCREEN_HEIGHT // 2 - text.get_height() // 2,
#             ),
#         )
#         pygame.display.update()
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 run = False
#                 pygame.quit()
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 run = False
#     main()


# while True:
#     menu_screen()

# ---------------------------------------ver2..นับเวลา-----------------------------------------------

# --------------------------------------ver3..เพิ่มปุ่มเริ่ม----------------------------------------------

import pygame
from network import Network
from game import *

pygame.init()

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Client")

basic_font = pygame.font.SysFont("comicsans", 30)
accent_color = (0, 0, 0)
button_font = pygame.font.SysFont("comicsans", 40)
button_color = (0, 200, 0)
button_hover_color = (0, 255, 0)
button_text_color = (255, 255, 255)
button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 60)


def draw_lobby():
    win.fill((128, 128, 128))

    title_font = pygame.font.SysFont("comicsans", 60)
    title_text = title_font.render("Pong Show", True, (255, 255, 255))
    win.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))

    mouse_pos = pygame.mouse.get_pos()
    if button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(win, button_hover_color, button_rect)
    else:
        pygame.draw.rect(win, button_color, button_rect)

    button_text = button_font.render("Start Game", True, button_text_color)
    win.blit(
        button_text,
        (
            button_rect.centerx - button_text.get_width() // 2,
            button_rect.centery - button_text.get_height() // 2,
        ),
    )

    pygame.display.update()


def redraw_window(screen, player, player2, ball, score):
    screen.fill((255, 255, 255))

    if not (player.connected() and player2.connected()):
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render("Waiting for Player...", True, (255, 0, 0))
        screen.blit(
            text,
            (
                SCREEN_WIDTH // 2 - text.get_width() // 2,
                SCREEN_HEIGHT // 2 - text.get_height() // 2,
            ),
        )
    else:
        player.draw(screen)
        player2.draw(screen)
        ball.draw(screen)

        font = pygame.font.SysFont("comicsans", 30)
        red_text = font.render(f"Red: {score.score_player_1}", True, (255, 0, 0))
        blue_text = font.render(f"Blue: {score.score_player_2}", True, (0, 0, 255))
        screen.blit(red_text, (10, 10))
        screen.blit(blue_text, (SCREEN_WIDTH - blue_text.get_width() - 10, 10))

        if not ball.active and ball.countdown_number != "":
            countdown_text = basic_font.render(
                str(ball.countdown_number), True, accent_color
            )
            countdown_rect = countdown_text.get_rect(
                center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50)
            )
            screen.blit(countdown_text, countdown_rect)

    pygame.display.update()


def main():
    network = Network()
    player, ball, score = network.getP()
    player.ready = True

    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(60)
        player2, ball, score = network.send((player, ball, score))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        player.move()
        redraw_window(win, player, player2, ball, score)


def lobby_screen():
    run = True
    while run:
        draw_lobby()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    run = False

    main()


while True:
    lobby_screen()

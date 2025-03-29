import pygame
from network import Network
from game import *

pygame.init()

width = 500
height = 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

def redrawWindow(screen, player, player2, ball, score):
    screen.fill((255, 255, 255))
    
    if not (player.connected() and player2.connected()):
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render("Waiting for Player...", 1, (255, 0, 0))
        win.blit(text, (width//2 - text.get_width()//2, height//2 - text.get_height()//2))
    else:
        player.draw(screen)
        player2.draw(screen)
        ball.draw(screen)
        
        font = pygame.font.SysFont("comicsans", 30)
        text = font.render(f"Red: {score.score_player_1}", True, (255, 0, 0))
        text_2 = font.render(f"Blue: {score.score_player_2}", True, (0, 0, 255))
        win.blit(text, (10, 10))
        win.blit(text_2, (width - text_2.get_width() - 10, 10))
    
    pygame.display.update()

def main():
    run = True
    n = Network()
    p, ball, score = n.getP()
    p.ready = True
    clock = pygame.time.Clock()
    
    while run:
        clock.tick(60)
        data = n.send((p, ball, score))
        p2, ball, score = data
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        p.move()
        redrawWindow(win, p, p2, ball, score)

def menu_screen():  
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(60)
        win.fill((128, 128, 128))
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Click to Play!", 1, (255, 0, 0))
        win.blit(text, (100, 200))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

    main()

while True:
    menu_screen()


while True:
    menu_screen()

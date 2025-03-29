import pygame
from network import Network
from game import Player , Ball
pygame.init()

width = 500
height = 500
win = pygame.display.set_mode((width, height))

pygame.display.set_caption( "Client" )

# def draw_score(screen, player1, player2):
#     font = pygame.font.Font(None, 40)  # กำหนดฟอนต์ขนาด 40
#     score_text = f"{player1.score} - {player2.score}"  # รูปแบบคะแนน 1 - 2
#     text = font.render(score_text, True, (0, 0, 0))  # สีดำ
#     screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, 20))  # แสดงตรงกลางจอ


def redrawWindow(screen,player, player2,ball):
    screen.fill((255,255,255))
    # add if else
    if not(player.connected() and player2.connected()):
        font = pygame.font.Font(None, 80)
        text = font.render("Waiting for Player...", 1, (255,0,0), True)
        win.blit(text, (width/2 - text.get_width()/2 , height/2 - text.get_height()/2))
    else:
        player.draw(screen)
        player2.draw(screen)
        ball.draw(screen)
        # draw_score(screen, player, player2)
    
    pygame.display.update()

def main():
    run = True
    n = Network()
    print("Debug: getP() returned:", n.getP())
    if n.getP() is None:
        raise ValueError("Error: getP() returned None. Check the network connection.")
    p , ball = n.getP() # รับ player ball ไป server
    
    p.ready = True 
    clock = pygame.time.Clock()
    
    while run:
        clock.tick(60)
        data = n.send((p, ball))  # send player and ball to server
        p2, ball = data  # resive data from server
        
        print(f"Player 1 Score: {p.score} | Player 2 Score: {p2.score}", end='\r')
         
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        p.move()
        redrawWindow(win, p, p2 , ball)

def menu_screen():  
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(60)
        win.fill((128, 128, 128))
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Click to Play!", 1, (255,0,0))
        win.blit(text, (100,200))
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

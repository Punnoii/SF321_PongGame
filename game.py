import pygame
import sys
import random


class Player:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = pygame.Rect(x, y, width, height)
        self.vel = 5
        self.ready = False
        self.screen_width = 500
        self.screen_height = 500

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.y -= self.vel

        if keys[pygame.K_DOWN]:
            self.y += self.vel

        # scope of Player
        if self.y < 0:
            self.y = 0
        if self.y >= self.screen_height - self.height:
            self.y = self.screen_height - self.height

        self.update()

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)
        
    # check connect
    def connected(self):
        return self.ready


class Ball:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = pygame.Rect(x, y, width, height)
        self.speed_x = random.choice((1, -1))  # ความเร็วเริ่มต้นในแกน X
        self.speed_y = random.choice((1, -1))  # ความเร็วเริ่มต้นในแกน Y
        self.screen_width = 500
        self.screen_height = 500

    def update(self):
        self.rect.topleft = (self.x, self.y)  # อัปเดตตำแหน่งของ rect

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def move(self, players, score):

        self.x += self.speed_x
        self.y += self.speed_y

        if self.y <= 0 or self.y >= self.screen_height:
            self.speed_y *= -1

        if self.rect.colliderect(players[0].rect):
            self.speed_x = 1  # เปลี่ยนทิศทางแกน x เมื่อชน

        if self.rect.colliderect(players[1].rect):
            self.speed_x = -1  # เปลี่ยนทิศทางแกน x เมื่อชน

        if self.x <= 0 :
            score.p_2_hit_score()
            print(f"Player 1 Score: {score.score_player_2}")
            self.ball_start()
        elif self.x >= self.screen_width:
            score.p_1_hit_score()
            print(f"Player 0 Score: {score.score_player_1}")
            self.ball_start()
            
            
        self.update()

    def ball_start(self):
        self.x = 250
        self.y = 250
        self.speed_x = random.choice((1, -1))
        self.speed_y = random.choice((1, -1))

class Score:
    def __init__(self,score_1,score_2):
        self.score_player_1 = score_1
        self.score_player_2 = score_2
    def p_1_hit_score(self):
        self.score_player_1 += 1
    def p_2_hit_score(self):
        self.score_player_2 += 1

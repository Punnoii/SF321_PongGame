import pygame
import sys
import random

class Player():
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = pygame.Rect(x,y,width,height)
        self.vel = 3
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
        if self.y < 0 :
            self.y = 0
        if self.y >= self.screen_height - self.height:
            self.y = self.screen_height - self.height
        
        
        self.update()

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)
    
    # check connect 
    def connected(self):
        return self.ready
    
class Ball():
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = pygame.Rect(x,y,width,height)
        self.speed_x = random.choice((1, -1))  # ความเร็วเริ่มต้นในแกน X
        self.speed_y = random.choice((1, -1))  # ความเร็วเริ่มต้นในแกน Y
        self.screen_width = 500
        self.screen_height = 500
        
    def update(self):
        self.rect.topleft = (self.x, self.y)  # อัปเดตตำแหน่งของ rect
    
    def draw(self , screen):
        pygame.draw.rect(screen, self.color, self.rect)
        
    def move(self,players):
        
        self.x += self.speed_x
        self.y += self.speed_y
        
        if self.y <= 0 or self.y >= self.screen_height :
            self.speed_y *= -1 
        if self.x <= 0 or self.x >= self.screen_width :
            self.ball_start()
            
        for player in players:
            if self.rect.colliderect(player.rect):
                self.speed_x *= -1  # เปลี่ยนทิศทางแกน x เมื่อชน
                break
        
            
        self.update()
        
    def ball_start(self):
        self.x = 250
        self.y = 250
        self.speed_x = random.choice((1,-1))
        self.speed_y = random.choice((1,-1))
        
        

    
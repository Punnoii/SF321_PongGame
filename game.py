import pygame
import random

POINT_ZONE_HEIGHT = 80

class Player:
    def __init__(self, x, y, width, height, color, screen_width, screen_height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = pygame.Rect(x, y, width, height)
        self.vel = 5
        self.ready = False
        self.screen_width = screen_width
        self.screen_height = screen_height

    def draw(self, screen, y_offset=0):
        pygame.draw.rect(screen, self.color, (self.x, self.y + y_offset, self.width, self.height))

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.y -= self.vel
        if keys[pygame.K_DOWN]:
            self.y += self.vel

        if self.y < POINT_ZONE_HEIGHT:
            self.y = POINT_ZONE_HEIGHT
        elif self.y > self.screen_height - self.height:
            self.y = self.screen_height - self.height

        self.update()

    def update(self):
        self.rect.topleft = (self.x, self.y)

    def connected(self):
        return self.ready


class Ball:
    def __init__(self, x, y, width, height, color, screen_width, screen_height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.radius = width // 2
        self.rect = pygame.Rect(x, y, width, height)
        self.speed_x = random.choice((1, -1))
        self.speed_y = random.choice((1, -1))
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.active = True
        self.score_time = 0
        self.countdown_number = ""
    def update(self):
        if self.active:
            self.x += self.speed_x
            self.y += self.speed_y
            self.rect.center = (self.x, self.y)
        else:
            self.update_countdown()

    def update_countdown(self):
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.score_time

        if elapsed < 1000:
            self.countdown_number = "3"
        elif elapsed < 2000:
            self.countdown_number = "2"
        elif elapsed < 3000:
            self.countdown_number = "1"
        else:
            self.active = True
            self.countdown_number = ""

    def draw(self, screen, y_offset=0):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y + y_offset)), self.radius)

    def move(self, players, score):
        if self.active:
            if self.rect.top <= POINT_ZONE_HEIGHT or self.rect.bottom >= self.screen_height:
                self.speed_y *= -1

            if self.rect.colliderect(players[0].rect):
                self.speed_x = abs(self.speed_x)
            if self.rect.colliderect(players[1].rect):
                self.speed_x = -abs(self.speed_x)

            if self.rect.left <= 0:
                score.p_2_hit_score()
                self.reset_ball()
            elif self.rect.right >= self.screen_width:
                score.p_1_hit_score()
                self.reset_ball()

        self.update()

    def reset_ball(self):
        if self.active:
            self.active = False
            self.score_time = pygame.time.get_ticks()
            self.x = self.screen_width // 2
            self.y = self.screen_height // 2
            self.rect.center = (self.x, self.y)
            self.speed_x = random.choice((1, -1))
            self.speed_y = random.choice((1, -1))
            self.countdown_number = ""


class Score:
    def __init__(self, score_1=0, score_2=0):
        self.score_player_1 = score_1
        self.score_player_2 = score_2

    def p_1_hit_score(self):
        self.score_player_1 += 1

    def p_2_hit_score(self):
        self.score_player_2 += 1
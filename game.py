import pygame
import random

pygame.init()
pygame.mixer.init()
hit_sound = pygame.mixer.Sound("pong.ogg")
score_sound = pygame.mixer.Sound("score.ogg")

BAR_HEIGHT = 50


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
        self.name = ""
        self.image = pygame.image.load("Paddle.png")
        self.image = pygame.transform.scale(self.image, (width, height))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.y -= self.vel
        if keys[pygame.K_DOWN]:
            self.y += self.vel
        if self.y < BAR_HEIGHT:
            self.y = BAR_HEIGHT
        elif self.y > self.screen_height - self.height:
            self.y = self.screen_height - self.height
        self.update()

    def update(self):
        self.rect.topleft = (self.x, self.y)

    def connected(self):
        return self.ready

    def __getstate__(self):
        state = self.__dict__.copy()
        if "image" in state:
            del state["image"]
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.image = pygame.image.load("Paddle.png")
        self.image = pygame.transform.scale(self.image, (self.width, self.height))


class Ball:
    def __init__(self, x, y, width, height, color, screen_width, screen_height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = pygame.Rect(x, y, width, height)
        self.speed_x = random.choice((1, -1))
        self.speed_y = random.choice((1, -1))
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.active = True
        self.score_time = 0
        self.countdown_number = ""
        self.image = pygame.image.load("Ball.png")
        self.image = pygame.transform.scale(self.image, (width, height))

    def update(self):
        if self.active:
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y
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

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def move(self, players, score):
        if self.active:
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y

            if self.rect.top <= BAR_HEIGHT or self.rect.bottom >= self.screen_height:
                self.speed_y *= -1
                hit_sound.play()

            if self.rect.colliderect(players[0].rect):
                self.speed_x = abs(self.speed_x)
                hit_sound.play()

            elif self.rect.colliderect(players[1].rect):
                self.speed_x = -abs(self.speed_x)
                hit_sound.play()

            if self.rect.left <= 0:
                score.p_2_hit_score()
                self.reset_ball()
            elif self.rect.right >= self.screen_width:
                score.p_1_hit_score()
                self.reset_ball()
        else:
            self.update_countdown()

    def reset_ball(self):
        if self.active:
            self.active = False
            self.score_time = pygame.time.get_ticks()
            self.rect.center = (self.screen_width // 2, self.screen_height // 2)
            self.speed_x = random.choice((1, -1))
            self.speed_y = random.choice((1, -1))
            self.countdown_number = ""

    def __getstate__(self):
        state = self.__dict__.copy()
        if "image" in state:
            del state["image"]
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.image = pygame.image.load("Ball.png")
        self.image = pygame.transform.scale(self.image, (self.width, self.height))


class Score:
    def __init__(self, score_1=0, score_2=0):
        self.score_player_1 = score_1
        self.score_player_2 = score_2

    def p_1_hit_score(self):
        self.score_player_1 += 1
        score_sound.play()

    def p_2_hit_score(self):
        self.score_player_2 += 1
        score_sound.play()

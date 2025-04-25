import pygame
import random

pygame.init()
pygame.mixer.init()
enter_sound = pygame.mixer.Sound("sound/enter.mp3")


def randSound():
    hit_sound = pygame.mixer.Sound(f"sound/attack{random.randint(1,5)}.mp3")
    hit_sound.set_volume(0.3)
    hit_sound.play()


def randDeath():
    death_sound = pygame.mixer.Sound(f"sound/death{random.randint(1,2)}.mp3")
    death_sound.set_volume(0.3)
    death_sound.play()


BAR_HEIGHT = 50


class Player:
    def __init__(self, x, y, width, height, color, screen_width, screen_height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = pygame.Rect(x, y, width, height)
        self.vel = 10
        self.ready = False
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.id = 0
        self.name = ""
        self.image = pygame.image.load("img/Paddle.png")
        self.image = pygame.transform.scale(self.image, (width, height))
        self.skill = False
        self.last_skill_time = 0
        self.skill_cooldown = 15000
        self.skill_announced = False
        self.skill_ready = False
        self.button_press = False

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def move(self, event_list):
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.last_skill_time
        self.skill_ready = elapsed > self.skill_cooldown
        for event in event_list:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                if current_time - self.last_skill_time > self.skill_cooldown:
                    self.last_skill_time = current_time
                    self.skill = True
                    print("Skill used")
                    self.skill_ready = False
                else:
                    print("Skill on cooldown")

        if self.skill and not self.skill_announced:
            self.skill_announced = True

        if not self.skill and self.skill_announced:
            self.skill_announced = False

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
        self.image = pygame.image.load("img/Paddle.png")
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
        self.ready = False
        self.active = True
        self.score_time = 0
        self.countdown_number = ""
        self.last_speedup_time = pygame.time.get_ticks()
        self.speed_multiplier = 1.0
        self.ability = False

        self.image = pygame.image.load("img/kunai.png")
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
        if self.active and not self.ability:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_speedup_time > 1000:
                self.speed_multiplier += 0.01
                self.last_speedup_time = current_time
                self.speed_x *= 1.1
                self.speed_y *= 1.1

            self.rect.x += int(self.speed_x)
            self.rect.y += int(self.speed_y)

            if self.rect.top <= BAR_HEIGHT or self.rect.bottom >= self.screen_height:
                self.speed_y *= -1
                randSound()

            if self.rect.colliderect(players[0].rect):
                self.speed_x = abs(self.speed_x)
                diff = (self.rect.centery - players[0].rect.centery) / (
                    players[0].rect.height / 2
                )
                self.speed_y = diff * 5
                randSound()

            elif self.rect.colliderect(players[1].rect):
                self.speed_x = -abs(self.speed_x)
                diff = (self.rect.centery - players[1].rect.centery) / (
                    players[1].rect.height / 2
                )
                self.speed_y = diff * 5
                randSound()

            if self.rect.left <= 0:
                score.p_2_hit_score()
                for player in players:
                    player.skill = False
                self.reset_ball()
            elif self.rect.right >= self.screen_width:
                score.p_1_hit_score()
                for player in players:
                    player.skill = False
                self.reset_ball()
        elif self.active and (self.ability):
            current_time = pygame.time.get_ticks()
            if current_time - self.last_speedup_time > 1000:
                self.speed_multiplier += 0.01
                self.last_speedup_time = current_time
                self.speed_x *= 1.1
                self.speed_y *= 1.1

            self.rect.x += int(self.speed_x)
            self.rect.y += int(self.speed_y)

            if self.rect.top <= BAR_HEIGHT or self.rect.bottom >= self.screen_height:
                self.speed_y *= -1
                randSound()

            if self.rect.left <= 0:
                self.speed_x = abs(self.speed_x)
                randSound()

            if self.rect.right >= self.screen_width:
                self.speed_x = -abs(self.speed_x)
                randSound()

            if self.rect.colliderect(players[0].rect):
                score.p_2_hit_score()
                randDeath()
                for player in players:
                    player.skill = False
                self.reset_ball()

            elif self.rect.colliderect(players[1].rect):
                score.p_1_hit_score()
                randDeath()
                for player in players:
                    player.skill = False
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
            self.speed_multiplier = 1.0
            self.last_speedup_time = pygame.time.get_ticks()
            self.countdown_number = ""
            self.ability = False

    def smart_skill(self):
        self.ability = True

    def __getstate__(self):
        state = self.__dict__.copy()
        if "image" in state:
            del state["image"]
        if "original_image" in state:
            del state["original_image"]
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.image = pygame.image.load("img/kunai.png")
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.original_image = self.image


class Score:
    def __init__(self, score_1=0, score_2=0):
        self.score_player_1 = score_1
        self.score_player_2 = score_2

    def p_1_hit_score(self):
        self.score_player_1 += 1
        randDeath()

    def p_2_hit_score(self):
        self.score_player_2 += 1
        randDeath()


class List_Player:
    def __init__(self):
        self.list_player = []

    def add_player(self, name):
        self.list_player.append(name)

    def remove_player(self, name):
        self.list_player.remove(name)

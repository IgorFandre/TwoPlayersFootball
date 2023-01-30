import pygame
from pygame.color import THECOLORS
from PARAMETERS import *


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((60, 60))
        self.image.fill(THECOLORS['white'])
        self.rect = self.image.get_rect()
        self.rect.center = WIDTH // 2, HEIGHT // 2
        self.move_x = STOP
        self.move_y = STOP

    def update(self) -> None:
        self.rect.x += self.move_x
        self.rect.y += self.move_y
        if self.rect.bottom < GROUND:
            self.move_y += 1
        else:
            self.move_y = int(-STOP_KOEF * self.move_y)
            self.rect.bottom = GROUND
        if (self.rect.right >= WIDTH and self.move_x > 0) or\
           (self.rect.left <= 0 and self.move_x < 0):
            self.move_x = int(-STOP_KOEF * self.move_x)
        if self.rect.top < 0 and self.move_y < 0:
            self.move_y = int(-STOP_KOEF * self.move_y)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((100, 200))
        self.image.fill(THECOLORS['green'])
        self.rect = self.image.get_rect()
        self.rect.center = 200, GROUND - 80
        self.move_x = STOP
        self.move_y = STOP
        self.orientation = RIGHT
        self.kick = False

    def update(self) -> None:
        self.rect.x += self.move_x
        self.rect.y += self.move_y
        if self.rect.bottom < GROUND:
            self.move_y += 1
        else:
            self.move_y = 0
            self.rect.bottom = GROUND
        if (self.rect.right >= WIDTH and self.move_x > 0) or\
           (self.rect.left <= 0 and self.move_x < 0):
            self.move_x = 0
            if self.rect.right >= WIDTH:
                self.rect.right = WIDTH
            else:
                self.rect.right = 50


class Leg(pygame.sprite.Sprite):
    def __init__(self, player: Player):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((60, 80))
        self.image.fill(THECOLORS['green'])
        self.image.set_alpha(100)
        self.rect = self.image.get_rect()
        if player.orientation == LEFT:
            self.rect.bottomright = player.rect.bottomleft
        else:
            self.rect.bottomleft = player.rect.bottomright


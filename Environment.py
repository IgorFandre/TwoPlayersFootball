import pygame
from pygame.color import THECOLORS

from PARAMETERS import *


class Gate(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((150, 330))
        self.image.fill(THECOLORS['yellow'])
        self.image.set_alpha(70)
        self.rect = self.image.get_rect()
        self.rect.bottomright = WIDTH, GROUND


class Barier(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((170, 70))
        self.image.fill(THECOLORS['yellow'])
        self.rect = self.image.get_rect()
        self.rect.bottomright = WIDTH + 10, GROUND - 320
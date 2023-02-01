import pygame
from pygame.color import THECOLORS

from PARAMETERS import *
from Environment import Barier


def set_base_map(env_sprites: pygame.sprite.Group) -> None:
    grass_barier = Barier()
    grass_barier.image = pygame.Surface((WIDTH, 200))
    grass_barier.image.fill(THECOLORS['darkgreen'])
    grass_barier.rect = grass_barier.image.get_rect()
    grass_barier.rect.centerx = WIDTH // 2
    grass_barier.rect.top = GROUND

    l_gate_barier = Barier()
    r_gate_barier = Barier()
    r_gate_barier.rect.bottomleft = (-10, r_gate_barier.rect.bottomleft[1])

    env_sprites.add(l_gate_barier)
    env_sprites.add(r_gate_barier)
    env_sprites.add(grass_barier)


def map_0(env_sprites: pygame.sprite.Group) -> None:
    # default map
    pass


def map_1(env_sprites: pygame.sprite.Group) -> None:
    big_barier_1 = Barier()
    big_barier_2 = Barier()
    big_barier_1.image = pygame.Surface((100, 100))
    big_barier_2.image = pygame.Surface((100, 100))
    big_barier_1.image.fill(THECOLORS['purple'])
    big_barier_2.image.fill(THECOLORS['purple'])
    big_barier_1.rect = big_barier_1.image.get_rect()
    big_barier_2.rect = big_barier_2.image.get_rect()
    big_barier_1.rect.center = WIDTH // 2 + 400, GROUND - 500
    big_barier_2.rect.center = WIDTH // 2 - 400, GROUND - 500

    env_sprites.add(big_barier_1)
    env_sprites.add(big_barier_2)


def map_2(env_sprites: pygame.sprite.Group) -> None:
    big_barier = Barier()
    big_barier.image = pygame.Surface((400, 100))
    big_barier.image.fill(THECOLORS['purple'])
    big_barier.rect = big_barier.image.get_rect()
    big_barier.rect.center = WIDTH // 2, GROUND - 270

    env_sprites.add(big_barier)

# Make here your own maps and add them in main.py (68 - 83 lines)
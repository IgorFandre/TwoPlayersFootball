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

    def set_right_player(self) -> None:
        self.image.fill(THECOLORS['blue'])
        self.rect.center = WIDTH - self.rect.center[0], 700

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

    def collide_ball(self, ball: Ball, left: bool, above: bool):
        new_vel_x = 2 * self.move_x - ball.move_x
        if new_vel_x >= 45:
            ball.move_x = 45
        elif new_vel_x <= -45:
            ball.move_x = -45
        else:
            ball.move_x = new_vel_x
        if left:
            ball.rect.left = self.rect.right
        else:
            ball.rect.right = self.rect.left

        if above:
            new_vel_y = int(STOP_KOEF * 2 * self.move_y - ball.move_y)
            if new_vel_y >= 45:
                ball.move_y = 45
            elif new_vel_y <= -45:
                ball.move_y = -45
            else:
                ball.move_y = new_vel_y
            if left:
                ball.rect.left = self.rect.right
            else:
                ball.rect.right = self.rect.left


class Leg(pygame.sprite.Sprite):
    def __init__(self, player: Player):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((60, 80))
        self.image.fill(THECOLORS['green'])
        self.image.set_alpha(100)
        self.rect = self.image.get_rect()
        self.orientation = player.orientation
        if self.orientation == LEFT:
            self.rect.bottomright = player.rect.bottomleft
        else:
            self.rect.bottomleft = player.rect.bottomright

    def make_kick(self, ball: Ball) -> None:
        if self.rect.colliderect(ball):
            if self.orientation == LEFT:
                ball.move_x = max(-45, ball.move_x - 30)
            else:
                ball.move_x = min(45, ball.move_x + 30)
            ball.move_y = max(-45, ball.move_y - 30)

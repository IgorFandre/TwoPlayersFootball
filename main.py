import sys
import pygame
from pygame.color import THECOLORS

from MovingObjects import Player, Ball, Leg
from Environment import Gate, Barier
from PARAMETERS import *

if __name__ == '__main__':
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    l_score = 0
    r_score = 0
    pygame.display.set_caption(f"My Game. Score: {r_score} : {l_score}")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('arial', 20)

    moving_objects = pygame.sprite.Group()
    env_sprites = pygame.sprite.Group()
    gate_spites = pygame.sprite.Group()
    l_player = Player()
    r_player = Player()
    r_player.orientation = LEFT
    r_player.image.fill(THECOLORS['blue'])
    r_player.rect.center = WIDTH - l_player.rect.center[0], 700
    ball = Ball()
    l_gate_barier = Barier()
    r_gate_barier = Barier()
    r_gate_barier.rect.bottomleft = -10, r_gate_barier.rect.bottomleft[1]
    big_barier_1 = Barier()
    big_barier_2 = Barier()
    grass_barier = Barier()
    big_barier_1.image = pygame.Surface((100, 100))
    big_barier_2.image = pygame.Surface((100, 100))
    grass_barier.image = pygame.Surface((WIDTH, 200))
    big_barier_1.image.fill(THECOLORS['purple'])
    big_barier_2.image.fill(THECOLORS['purple'])
    grass_barier.image.fill(THECOLORS['darkgreen'])
    big_barier_1.rect = big_barier_1.image.get_rect()
    big_barier_2.rect = big_barier_2.image.get_rect()
    grass_barier.rect = grass_barier.image.get_rect()
    big_barier_1.rect.center = WIDTH // 2 + 400, GROUND - 650
    big_barier_2.rect.center = WIDTH // 2 - 400, GROUND - 650
    grass_barier.rect.centerx = WIDTH // 2
    grass_barier.rect.top = GROUND
    l_gate = Gate()
    r_gate = Gate()
    r_gate.rect.bottomleft = 0, GROUND
    moving_objects.add(ball)
    moving_objects.add(l_player)
    moving_objects.add(r_player)

    env_sprites.add(l_gate_barier)
    env_sprites.add(r_gate_barier)
    env_sprites.add(big_barier_1)
    env_sprites.add(big_barier_2)
    env_sprites.add(grass_barier)

    gate_spites.add(l_gate)
    gate_spites.add(r_gate)

    running = True
    while running:
        # working on fps
        clock.tick(FPS)

        # checking buttons
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_w:
                    l_player.move_y = -20
                if event.key == pygame.K_s:
                    l_player.rect.y = 700
                if event.key == pygame.K_d:
                    l_player.move_x = RIGHT
                    l_player.orientation = RIGHT
                if event.key == pygame.K_a:
                    l_player.move_x = LEFT
                    l_player.orientation = LEFT
                if event.key == pygame.K_c:
                    l_player.kick = True
                if event.key == pygame.K_u:
                    r_player.move_y = -20
                if event.key == pygame.K_j:
                    r_player.rect.y = 700
                if event.key == pygame.K_k:
                    r_player.move_x = RIGHT
                    r_player.orientation = RIGHT
                if event.key == pygame.K_h:
                    r_player.move_x = LEFT
                    r_player.orientation = LEFT
                if event.key == pygame.K_m:
                    r_player.kick = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a and l_player.move_x == LEFT:
                    l_player.move_x = STOP
                elif event.key == pygame.K_d and l_player.move_x == RIGHT:
                    l_player.move_x = STOP

                if event.key == pygame.K_h and r_player.move_x == LEFT:
                    r_player.move_x = STOP
                elif event.key == pygame.K_k and r_player.move_x == RIGHT:
                    r_player.move_x = STOP

                if event.key == pygame.K_c:
                    l_player.kick = False
                if event.key == pygame.K_m:
                    r_player.kick = False

        # save relationships between players and ball
        l_left = l_player.rect.center[0] <= ball.rect.center[0]
        r_left = r_player.rect.center[0] < ball.rect.center[0]

        # upd positions
        ball.update()
        moving_objects.update()

        # checks for objects
        if l_player.rect.collidepoint(ball.rect.center):
            new_vel = 2 * l_player.move_x - ball.move_x
            if new_vel >= 45:
                ball.move_x = 45
            elif new_vel <= -45:
                ball.move_x = -45
            else:
                ball.move_x = new_vel
            if l_left:
                ball.rect.left = l_player.rect.right
            else:
                ball.rect.right = l_player.rect.left
        if r_player.rect.collidepoint(ball.rect.center):
            new_vel = 2 * r_player.move_x - ball.move_x
            if new_vel >= 40:
                ball.move_x = 40
            elif new_vel <= -40:
                ball.move_x = -40
            else:
                ball.move_x = new_vel
            if r_left:
                ball.rect.left = r_player.rect.right
            else:
                ball.rect.right = r_player.rect.left

        for barier in env_sprites:
            if barier.rect.colliderect(ball.rect):
                if barier.rect.left <= ball.rect.centerx <= barier.rect.right:
                    if ball.rect.centery > barier.rect.centery:
                        ball.rect.top = barier.rect.bottom
                        if ball.move_y < 0:
                            ball.move_y *= -1
                    else:
                        ball.rect.bottom = barier.rect.top
                        if ball.move_y > 0:
                            ball.move_y *= -1
                elif barier.rect.left > ball.rect.left:
                    ball.rect.right = barier.rect.left
                    if ball.move_x > 0:
                        ball.move_x *= -1
                elif l_player.rect.right > barier.rect.right:
                    l_player.rect.left = barier.rect.right
                    if ball.move_x < 0:
                        ball.move_x *= -1
            if barier.rect.colliderect(l_player.rect):
                if barier.rect.left <= l_player.rect.centerx <= barier.rect.right:
                    if l_player.rect.centery > barier.rect.centery:
                        l_player.rect.top = barier.rect.bottom
                    else:
                        l_player.rect.bottom = barier.rect.top
                    l_player.move_y = 0
                elif barier.rect.left > l_player.rect.left:
                    l_player.rect.right = barier.rect.left
                elif l_player.rect.right > barier.rect.right:
                    l_player.rect.left = barier.rect.right
            if barier.rect.colliderect(r_player.rect):
                if barier.rect.left <= r_player.rect.centerx <= barier.rect.right:
                    if r_player.rect.centery > barier.rect.centery:
                        r_player.rect.top = barier.rect.bottom
                    else:
                        r_player.rect.bottom = barier.rect.top
                    r_player.move_y = 0
                elif barier.rect.left > r_player.rect.left:
                    r_player.rect.right = barier.rect.left
                elif r_player.rect.right > barier.rect.right:
                    r_player.rect.left = barier.rect.right

        if r_gate.rect.collidepoint(ball.rect.center):
            r_score += 1
            pygame.display.set_caption(f"My Game. Score: {l_score} : {r_score}")
            ball.rect.center = WIDTH // 2, HEIGHT // 2
            ball.move_x = 0
            ball.move_y = 0
            l_player.rect.center = 100, GROUND - 80
            r_player.rect.center = 1500, GROUND - 80
        if l_gate.rect.collidepoint(ball.rect.center):
            l_score += 1
            pygame.display.set_caption(f"My Game. Score: {l_score} : {r_score}")
            ball.rect.center = WIDTH // 2, HEIGHT // 2
            ball.move_x = 0
            ball.move_y = 0
            l_player.rect.center = 100, GROUND - 80
            r_player.rect.center = 1500, GROUND - 80

        # working with screen
        screen.fill(THECOLORS["black"])


        # making kicks
        if l_player.kick or r_player.kick:
            legs = pygame.sprite.Group()
            if l_player.kick:
                l_leg = Leg(l_player)
                if l_leg.rect.colliderect(ball):
                    if l_player.orientation == LEFT:
                        ball.move_x = max(-45, ball.move_x - 30)
                    else:
                        ball.move_x = min(45, ball.move_x + 30)
                    ball.move_y = max(-45, ball.move_y - 30)
                legs.add(l_leg)
            if r_player.kick:
                r_leg = Leg(r_player)
                r_leg.image.fill(THECOLORS["blue"])
                if r_leg.rect.colliderect(ball):
                    if r_player.orientation == LEFT:
                        ball.move_x = max(-45, ball.move_x - 30)
                    else:
                        ball.move_x = min(45, ball.move_x + 30)
                    ball.move_y = max(-45, ball.move_y - 30)
                legs.add(r_leg)
            legs.draw(screen)
        # for debug
        '''
        text_left_1 = font.render(f"l_player(green): move_x = {l_player.move_x}", True, THECOLORS['white'])
        screen.blit(text_left_1, (20, 20))

        text_left_2 = font.render(f"r_player(blue): move_x = {r_player.move_x}", True, THECOLORS['white'])
        screen.blit(text_left_2, (20, 50))

        text_right_1 = font.render(f"ball: move_x = {ball.move_x}", True, THECOLORS['white'])
        screen.blit(text_right_1, (500, 20))

        text_right_2 = font.render(f"move_y = {ball.move_y}", True, THECOLORS['white'])
        screen.blit(text_right_2, (530, 50))
        '''

        # draw the objects
        moving_objects.draw(screen)
        gate_spites.draw(screen)
        env_sprites.draw(screen)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

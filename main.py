import sys
import pygame
from pygame.color import THECOLORS

import Maps
from MovingObjects import Player, Ball, Leg
from Environment import Gate
from PARAMETERS import *

if __name__ == '__main__':
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(f"My Game. Score: {0} : {0}")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('arial', 20)

    moving_objects = pygame.sprite.Group()
    env_sprites = pygame.sprite.Group()
    gate_sprites = pygame.sprite.Group()

    l_score = 0
    r_score = 0

    l_player = Player()
    r_player = Player()
    r_player.set_right_player()
    ball = Ball()
    moving_objects.add(ball)
    moving_objects.add(l_player)
    moving_objects.add(r_player)

    l_gate = Gate()
    r_gate = Gate()
    r_gate.rect.bottomleft = (0, GROUND)
    gate_sprites.add(l_gate)
    gate_sprites.add(r_gate)

    # bool for playing game
    running = True

    # choosing map
    number_map = 0
    while not number_map:
        pygame.time.delay(1)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4,
                                 pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]:
                    number_map = (event.key - 48)
                if event.key == pygame.K_ESCAPE:
                    running = False
                    number_map = -1
            if event.type == pygame.QUIT:
                running = False
                number_map = -1

    Maps.set_base_map(env_sprites)

    if number_map == 2:
        Maps.map_1(env_sprites)
    elif number_map == 3:
        Maps.map_2(env_sprites)
    elif number_map == 4:
        pass
    elif number_map == 5:
        pass
    elif number_map == 6:
        pass
    elif number_map == 7:
        pass
    elif number_map == 8:
        pass
    elif number_map == 9:
        pass

    # playing game
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
        l_left = l_player.rect.centerx <= ball.rect.centerx
        l_above_player = l_player.rect.top <= ball.rect.centery
        r_left = r_player.rect.centerx < ball.rect.centerx
        r_above_player = r_player.rect.top <= ball.rect.centery

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

        make_start_position = False
        if r_gate.rect.collidepoint(ball.rect.center):
            r_score += 1
            make_start_position = True
        if l_gate.rect.collidepoint(ball.rect.center):
            l_score += 1
            make_start_position = True
        if make_start_position:
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
                l_leg.make_kick(ball)
                legs.add(l_leg)
            if r_player.kick:
                r_leg = Leg(r_player)
                r_leg.image.fill(THECOLORS["blue"])
                r_leg.make_kick(ball)
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
        gate_sprites.draw(screen)
        env_sprites.draw(screen)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

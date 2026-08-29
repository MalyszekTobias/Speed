import time as czas
from random import random
import Assets
import pygame
from pygame import *
from app import particle

import random as ran

from map_handler import names


class Player:
    def __init__(self, display):
        self.display = display
        self.display.objects.append(self)
        self.offset = 60
        self.cam = self.display.camera

        self.g = 0.6
        self.regular_max_speed = 8
        self.boosted_max_speed = 16
        self.max_speed = self.regular_max_speed
        self.max_fall_speed = -20
        self.regular_jump = 16
        self.boosted_jump = 23
        self.jump_length = self.regular_jump
        self.air_acceleration = 0.4
        self.ground_acceleration = 1
        self.acceleration = self.air_acceleration
        self.air_friction = 0.1
        self.ground_friction = 0.5
        self.gravity = True
        self.wall_and_ceiling_bounce = 6
        self.floor_bounce = 5
        self.min_bounce = 5
        self.bounce_block_power = 2
        self.energy_conservation = 0.7
        self.bouncy_mode = True
        self.jump_recovery_from_all_direction_bounces = False
        self.jump_amount = 1
        self.jump_speed_boost = 4
        self.speed_correction = 1

        self.hook_x = None
        self.hook_y = None
        self.hook_size = 20
        self.hooked = False
        self.hook_speed = 40
        self.hook_power = 3
        self.hook_length = 520
        self.hook_vel_up = 0
        self.hook_vel_left = 0
        self.hook_reeling = False
        self.hook_buffer = False

        self.magnet_strength = 30
        self.magnet_polarity = 0
        self.numb_magnet_radius = 100

        self.width = self.display.tile_size + 10
        self.height = self.width
        self.character = self.display.game.character # 0 is runner, 1 is bouncer, 2 is hooker, 3 is magneter, 4 is rocketeer, 9 is debugger

        self.colors = [[30, 200, 30], [200, 30, 30], [200, 200, 30], [60, 60, 200], [200, 150, 50], None, None, None, None, [200, 200, 200]]
        self.trail_colors = [[20, 90, 20], [90, 20, 20], [90, 90, 20], [30, 30, 90], [110, 70, 20], None, None, None, None, [90, 90, 90]]
        self.names = ['The Runner', 'The Bouncer', 'The Hooker', 'The Magneter', None, None, None, None, 'The Debugger']
        if self.character == 0:
            # runner can run along the floor and jump twice, pretty normal stuff
            self.bouncy_mode = False
            self.max_speed, self.regular_max_speed = 9,9
            self.sprites = [pygame.image.load("Assets/Sprites/green_left.png"), pygame.image.load("Assets/Sprites/green_right.png")]
        if self.character == 1:
            # bouncer bounces from every block, has 1 jump in the air after bouncing from a white floor
            self.bouncy_mode = True
            self.gravity = True
            self.g = 0.6
            self.min_bounce = 5
            self.wall_and_ceiling_bounce = 5
            self.floor_bounce = 5
            self.sprites = [pygame.image.load("Assets/Sprites/red_left.png"), pygame.image.load("Assets/Sprites/red_right.png")]
        if self.character == 2:
            # hooker has a grappling hook
            self.bouncy_mode = True
            self.g = 0.9
            self.max_fall_speed, self.max_speed, self.regular_max_speed = -15, 15, 15
            self.speed_correction = 10
            self.jump_speed_boost = 0
            self.jump_amount = 0
            self.sprites = [pygame.image.load("Assets/Sprites/yellow_left.png"), pygame.image.load("Assets/Sprites/yellow_right.png")]
        if self.character == 3:
            # magneter can be attracted or repelled from the cursor
            self.bouncy_mode = False
            self.sprites = [pygame.image.load("Assets/Sprites/teal_left.png"), pygame.image.load("Assets/Sprites/teal_right.png")]
        if self.character == 9:
            self.bouncy_mode = False
            self.gravity = False
            self.air_acceleration = 2
            self.ground_acceleration = 2
            self.max_speed = self.boosted_max_speed
            self.sprites = [pygame.image.load("Assets/Sprites/teal_left.png"), pygame.image.load("Assets/Sprites/teal_right.png")]
        # magneter will get attracted to the mouse, no jump, no gravity
        # rocketeer will have a rocket to perform rocketboosts away from the mouse

        self.player_color, self.trail_color = self.colors[self.character], self.trail_colors[self.character]

        for s in range(len(self.sprites)):
            self.sprites[s] = pygame.transform.scale(self.sprites[s], (self.width, self.height))
            self.sprite_rect = self.sprites[s].get_rect()
            self.sprite_rect.x,self.sprite_rect.y = 0, 0
        self.sprite = self.sprites[1]
        self.x = self.display.spawn_cords[0]
        self.y = self.display.spawn_cords[1]
        self.sprite_rect.x, self.sprite_rect.y = self.x, self.y
        self.vel_up = 0
        self.vel_left = 0
        self.cumulative_vel_down = 0
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.jump = False
        self.grounded = False
        self.hug_left = False
        self.hug_right = False
        self.touching_up = False
        self.archive_cords = [self.x, self.y]
        self.jumps_left = self.jump_amount
        self.just_started = True
        self.won = False

    def reset(self, restart): #Resets the parameters of the player to the starting ones, restart means it also restarts the level
        if restart:
            self.display.game.countdown = 59
            self.display.game.pause_sum = 0
            self.display.game.start_time = czas.time_ns() // 1000000
            self.display.game.countdown_text.hidden = False
        self.display.particles = []
        self.x = self.display.spawn_cords[0]
        self.y = self.display.spawn_cords[1]
        self.vel_up = 0
        self.vel_left = 0
        self.cumulative_vel_down = 0
        self.jump = False
        self.grounded = False
        self.hug_left = False
        self.hug_right = False
        self.touching_up = False
        self.archive_cords = [self.x, self.y]
        self.jumps_left = self.jump_amount
        self.hook_vel_up = 0
        self.hook_vel_left = 0
        self.hook_reeling = False
        self.hook_x = None
        self.hook_y = None
        self.hooked = False
        self.sprite = self.sprites[1]

        self.won = False

    def collision(self, list, block: list) -> bool:
        if self.vertical_collision(list[1], list[3], block[1], block[3]) and self.horizontal_collision(list[0], list[2],
                                                                                                       block[0],
                                                                                                       block[2]):
            return True
        return False
    # Checks if two objects share a horizontal line:
    def vertical_collision(self, y1, h1, y2, h2):

        if y2 + h2 < y1:
            return False
        if y1 + h1 < y2:
            return False
        return True  # checks
    # Checks if two objects share a vertical line:
    def horizontal_collision(self, x1, w1, x2, w2):
        if x2 + w2 < x1:
            return False
        if x1 + w1 < x2:
            return False
        return True
    def nudge(self, direction: str, block: list, blockType):
        if self.bouncy_mode:
            bounceMulti = 1
            if self.character == 2:
                bounceMulti = 0

            if blockType == 4:
                r, c = block[1] // self.display.tile_size, block[0] // self.display.tile_size
                bouncable = False
                if self.x < block[0]:
                    if self.display.current_map[r][c - 1] == 4:
                        bouncable = True
                elif self.x + self.width > block[0] + block[2]:
                    if self.display.current_map[r][c + 1] == 4:
                        bouncable = True
                else:
                    bouncable = True
                if bouncable:
                    bounceMulti = 1.5
            if self.jump_recovery_from_all_direction_bounces:
                self.jumps_left = self.jump_amount

            if direction == 'down':
                self.y = block[1] - self.height
                if self.vel_up < -self.min_bounce * bounceMulti:
                    self.vel_up *= -self.energy_conservation
                    if bounceMulti == 1.5:
                        self.vel_up += self.cumulative_vel_down / 5
                elif self.vel_up < 0:
                    self.vel_up = self.min_bounce * bounceMulti


                if bounceMulti == 1:
                    self.jumps_left = self.jump_amount
                return

            elif direction == 'up':
                if block[1] <= -51:
                    bounceMulti = 0
                self.y = self.archive_cords[1]

                if self.vel_up > self.min_bounce * bounceMulti:
                    self.vel_up *= -self.energy_conservation * bounceMulti
                elif self.vel_up > 0:
                    self.vel_up = -self.min_bounce * bounceMulti

                self.touching_up = True
                return

        else:
            if direction == 'down':
                self.y = block[1] - self.height - 1
                r,c = block[1] // self.display.tile_size, block[0] // self.display.tile_size
                bouncable = False
                if blockType == 4:
                    if self.x < block[0]:
                        if self.display.current_map[r][c - 1] == 4:
                            bouncable = True
                    elif self.x + self.width > block[0] + block[2]:
                        if self.display.current_map[r][c + 1] == 4:
                            bouncable = True
                if bouncable and self.vel_up <= -5:
                    if self.cumulative_vel_down > 1:
                        self.vel_up = self.cumulative_vel_down * 0.4
                        self.y = block[1] - self.height - 1

            elif direction == 'up':
                self.y = block[1] + block[3] + 1
                self.vel_up = 0
                return

        if direction == 'left':
            self.x = block[0] + block[2] + 1
            self.vel_left = 0
            return
        elif direction == 'right':
            self.x = block[0] - self.width - 1
            self.vel_left = 0
            return
    def corner(self, block: list):
        mapx, mapy = block[0] // self.display.tile_size, block[1] // self.display.tile_size


        right, down = False, False
        c = self.x + self.width - block[0]
        d = self.y + self.height - block[1]
        if block[0] + block[2] - self.x < c:
            c = block[0] + block[2] - self.x
            right = True
            if self.hug_left:
                return 'left'
        elif self.hug_right:
            return 'right'
        if block[1] + block[3] - self.y < d:
            d = block[1] + block[3] - self.y
            down = True
            if self.is_capped():
                return 'up'
        elif self.is_founded():
            return 'down'
        a, b = abs(self.x - self.archive_cords[0]), abs(self.y - self.archive_cords[1])
        try:
            if c / a < d / b:
                if right:
                    return 'left'
                else:
                    return 'right'
            else:
                if down:
                    return 'up'
                else:
                    return 'down'
        except:
            pass
    def detection(self, block: list):
        # keep track of whether the player is on the ground or in the ait
        if self.horizontal_collision(self.archive_cords[0], self.width, block[0], block[2]):
            if self.archive_cords[1] + self.height < block[1]:
                return 'down'  # going down
            else:
                return 'up'
        elif self.vertical_collision(self.archive_cords[1], self.height, block[1], block[3]):
            if self.archive_cords[0] + self.width < block[0]:
                return 'right'  # going right
            else:
                return 'left'
        else:
            return self.corner(block)
    def collision_finder(self, act_or_not: bool, entity):
        if entity == 'p':
            y = self.y
            x = self.x
            w = self.width
            h = self.height
        elif entity == 'h':
            y = self.hook_y
            x = self.hook_x
            w = 1
            h = 1
            if self.hook_reeling:
                return

        for row in range(int(y // self.display.tile_size - 1), int(y // self.display.tile_size + 3)):
            if not self.won:
                for column in range(int(x // self.display.tile_size - 1), int(x // self.display.tile_size + 3)):
                    try:
                        if not self.display.current_map[row][column] in (0, 5, 6, 7, 8, 9):
                            block = (column * self.display.tile_size, row * self.display.tile_size, self.display.tile_size,
                                     self.display.tile_size)
                            if self.collision((x, y, w, h), block):
                                if act_or_not:
                                    if entity == 'p':
                                        if self.nudge(self.detection(block), block, self.display.current_map[row][column]) == True and self.character == 0:
                                            self.vel_up = self.min_bounce * 3
                                            self.jumps_left = 1
                                        # pygame.draw.rect(self.display.screen, (200, 0, 0), (block[0] + self.cam,block[1],block[2],block[3]))
                                    elif entity == 'h':
                                        self.hooked = True
                                        self.hook_vel_left, self.hook_vel_up = 0, 0
                                        pygame.draw.rect(self.display.screen, (200, 100, 200), (block[0] + self.cam, block[1], block[2], block[3]))
                                else:
                                    return True
                        elif self.display.current_map[row][column] == 5:
                            block = (column * self.display.tile_size, row * self.display.tile_size, self.display.tile_size,
                                     self.display.tile_size)
                            if self.collision((x, y, w, h), block) and entity == 'p':
                                print('Your time: ', self.display.game.getTimer())
                                self.reset(False)
                                self.won = True
                                break

                    except:
                        pass
        return False

    def create_particle(self, size, color, x, y, velRight, velUp, g, lifetime, shrink):
        self.particle = particle.Particle(self.display, size / 2, color, x, y, velRight, velUp, g, lifetime, shrink)
        self.display.particles.append(self.particle)
    def tick(self):
        self.delta = self.display.game.delta_time
        if self.just_started:
            self.just_started = False
            self.reset(True)
            self.display.game.timer_text.hidden = True
        self.cam = self.display.camera
        if self.is_founded(source='render') and not self.bouncy_mode:
            self.vel_up = 0
        current_color = []
        self.current_trail_color = []
        for i in range(3):
            if self.player_color[i] == max(self.player_color):
                current_color.append(int(self.player_color[i] - 70 * (1 - self.jumps_left)))
                self.current_trail_color.append(int(self.trail_color[i] - 30 * (1 - self.jumps_left)))
            else:
                current_color.append(int(self.player_color[i] + 40 * (1 - self.jumps_left)))
                self.current_trail_color.append(int(self.trail_color[i] + 20 * (1 - self.jumps_left)))

        if self.character == 2:
            current_color, self.current_trail_color = self.player_color, self.trail_color
        self.sprite_rect.y = self.y
        self.sprite_rect.x = self.display.camera + self.x

            # pygame.draw.rect(self.display.screen, current_color, (self.x - 1, self.y - 1, self.width + 2, self.height + 2))
        self.display.screen.blit(self.sprite, self.sprite_rect)
        if self.character == 3:
            pygame.draw.circle(self.display.screen, (255, 255, 255), (self.display.camera + self.x + self.width / 2, self.y + self.height/2), self.numb_magnet_radius, 3)
            mousepos = mouse.get_pos()
            x_offset, y_offset = self.x + self.width / 2 + self.cam - mousepos[0], self.y + self.width / 2 - mousepos[1]
            distance = (x_offset ** 2 + y_offset ** 2) ** 0.5
            if distance > self.numb_magnet_radius and self.magnet_polarity != 0 and self.character == 3:
                self.magnetize(mousepos, distance, x_offset, y_offset)

        if self.display.game.countdown < 1:
            self.movement()
            if self.character == 2 and self.hook_x != None:
                self.hook_movement()
            if self.vel_up < -5:
                self.cumulative_vel_down -= self.vel_up / 13
            else:
                self.cumulative_vel_down = 0
        return
    def get_cam(self):
        cam = -self.display.camera
        max_x_deviation = 40
        if (cam + self.display.game.width / 2) < self.x - max_x_deviation:
            return self.x - max_x_deviation - self.display.game.width /2
        if (cam + self.display.game.width / 2) > self.x + max_x_deviation:
            return self.x + max_x_deviation - self.display.game.width /2
        return cam
    def events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_a, pygame.K_LEFT):
                self.left = True
            if event.key in (pygame.K_d, pygame.K_RIGHT):
                self.right = True
            if event.key in (pygame.K_s, pygame.K_DOWN):
                self.down = True
                if self.hugs_right() and not self.grounded:
                    self.wall_jump('r')
                elif self.hugs_left() and not self.grounded:
                    self.wall_jump('l')
            if event.key in (pygame.K_w, pygame.K_UP):
                self.up = True
            if event.key == pygame.K_LSHIFT and self.display.game.countdown < 1:
                self.shoot_hook(pygame.mouse.get_pos(), 2)
            if event.key in (pygame.K_SPACE,pygame.K_UP):
                if self.display.game.countdown < 1:
                    if self.jumps_left > 0:
                        self.jump = True
                        self.jumps_left -= 1
                        self.vel_up = self.jump_length
                        if self.grounded:
                            self.y -= 1
                            if self.character == 0:
                                self.jumps_left += 1
                        if self.right and not self.left:
                            self.vel_left -= self.jump_speed_boost
                        elif self.left and not self.right:
                            self.vel_left += self.jump_speed_boost
                    elif self.hugs_right() and not self.grounded:
                        self.wall_jump('r')
                    elif self.hugs_left() and not self.grounded:
                        self.wall_jump('l')
                    self.grounded = False

        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_a, pygame.K_LEFT):
                self.left = False
            if event.key in (pygame.K_d, pygame.K_RIGHT):
                self.right = False
            if event.key in (pygame.K_s, pygame.K_DOWN):
                self.down = False
            if event.key in (pygame.K_w, pygame.K_UP):
                self.up = False
            if event.key == pygame.K_SPACE:
                if self.jump:
                    self.vel_up /= 2
                    self.jump = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.magnet_polarity = 1
            elif event.button == 3:
                self.magnet_polarity = -1
            if event.button == 1 and self.display.game.countdown < 1:
                self.shoot_hook(pygame.mouse.get_pos())


        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.magnet_polarity == 1:
                self.magnet_polarity = 0
            elif event.button == 3 and self.magnet_polarity == -1:
                self.magnet_polarity = 0
            if event.button == 1 and self.display.game.countdown < 1:
                self.shoot_hook(pygame.mouse.get_pos(), -1)
                self.hook_buffer = False


    def is_founded(self, source=None):
        bounce = False
        for row in range(int(self.y // self.display.tile_size - 1), int(self.y // self.display.tile_size + 3)):
            for column in range(int(self.x // self.display.tile_size - 1), int(self.x // self.display.tile_size + 3)):
                try:
                    blockType = self.display.current_map[row][column]
                    if not blockType in (0, 5, 6, 7, 8, 9):
                        block = (column * self.display.tile_size, row * self.display.tile_size, self.display.tile_size,
                                 self.display.tile_size)
                        # if block[1] == self.y + self.height and block[0]
                        if self.collision((self.x + 1, self.y + self.height, self.width - 2, 1), block):
                            self.max_speed = self.regular_max_speed
                            self.acceleration = self.ground_acceleration
                            self.jump_length = self.regular_jump

                            if self.display.current_map[row][column] == 2:
                                self.max_speed = self.boosted_max_speed
                                self.acceleration = self.ground_acceleration * 2
                            if self.display.current_map[row][column] == 3:
                                self.jump_length = self.boosted_jump
                            if blockType != 4 or self.bouncy_mode:
                                return True
                            else:
                                bounce = True
                except:
                    pass
        if bounce:
            if source == 'render':
                return False
            else:
                return True
        self.acceleration = self.air_acceleration
        if self.max_speed == self.boosted_max_speed:
            self.acceleration = self.ground_acceleration
        return False
    def is_capped(self):
        for row in range(int(self.y // self.display.tile_size - 1), int(self.y // self.display.tile_size + 2)):
            for column in range(int(self.x // self.display.tile_size - 1), int(self.x // self.display.tile_size + 3)):
                try:
                    if not self.display.current_map[row][column] in (0, 5, 6, 7, 8, 9):
                        block = (column * self.display.tile_size, row * self.display.tile_size, self.display.tile_size,
                                 self.display.tile_size)
                        if self.collision((self.x + 1, self.y, self.width - 2, 1), block):
                            return True
                except:
                    pass
        return False
    def hugs_left(self):
        for row in range(int(self.y // self.display.tile_size - 1), int(self.y // self.display.tile_size + 3)):
            for column in range(int(self.x // self.display.tile_size - 1), int(self.x // self.display.tile_size + 3)):
                try:
                    if not self.display.current_map[row][column] in (0, 5, 6, 7, 8, 9):
                        block = (column * self.display.tile_size, row * self.display.tile_size, self.display.tile_size,
                                 self.display.tile_size)
                        if self.collision((self.x - 1, self.y - 1, 1, self.height - 2), block):
                            return True
                except:
                    pass
        return False
    def hugs_right(self):
        for row in range(int(self.y // self.display.tile_size - 1), int(self.y // self.display.tile_size + 3)):
            for column in range(int(self.x // self.display.tile_size - 1), int(self.x // self.display.tile_size + 3)):
                try:
                    if not self.display.current_map[row][column] in (0, 5, 6, 7, 8, 9):
                        block = (column * self.display.tile_size, row * self.display.tile_size, self.display.tile_size,
                                 self.display.tile_size)
                        if self.collision((self.x + self.width, self.y - 1, 1, self.height - 2), block):
                            return True
                except:
                    pass
        return False
    def update_block_statuses(self):
        self.grounded = self.is_founded()
        self.hug_left = self.hugs_left()
        self.hug_right = self.hugs_right()
        self.touching_up = self.is_capped()

    def hook_movement(self):
        line_color = (100, 200, 100)

        if self.hook_reeling:
            a, b = self.get_hook_vels(self.hook_x - self.x - self.width / 2, self.hook_y - self.y - self.width / 2,
                                      self.hook_speed)
            self.hook_vel_left = -a
            self.hook_vel_up = -b
            line_color = (200, 100, 100)

        if not self.hooked:
            divisor = int(max(abs(self.hook_vel_left), abs(self.vel_up))) + 1
            for i in range(divisor):
                self.collision_finder(True, 'h')
                if not self.hook_reeling:
                    d = ((self.x + self.width / 2 - self.hook_x) ** 2 + (self.y + self.height / 2 - self.hook_y) ** 2) ** 0.5
                    if d > self.hook_length:
                        self.hook_reeling = True
                if not self.hooked:
                    self.hook_x += self.hook_vel_left * self.delta * self.offset / divisor
                    self.hook_y += self.hook_vel_up * self.delta * self.offset / divisor
        if self.hook_reeling or self.hooked:
            hitbox = 0
            if self.hooked:
                hitbox = 5
            if self.collision((self.hook_x, self.hook_y, self.hook_size, self.hook_size), (self.x - hitbox, self.y - hitbox, self.width + 2 * hitbox, self.height + 2 * hitbox)):
                self.hook_x, self.hook_y = None, None
                self.hook_reeling = False
                self.hook_vel_up = 0
                self.hook_vel_left = 0
                self.hooked = False
                if self.hook_buffer:
                    self.shoot_hook(mouse.get_pos())
                return

        pygame.draw.line(self.display.screen, line_color, (self.x + self.cam + self.width / 2, self.y + self.width / 2), (self.hook_x + self.cam, self.hook_y), 4)
        pygame.draw.circle(self.display.screen, self.colors[2], (self.hook_x + self.cam, self.hook_y), self.hook_size / 2)
    def shoot_hook(self, mousepos, mode=1): #mode -1 - reel back; mode 1 - shoot hook; mode 2 - toggle
        if mode == 2:
            if self.hook_x == None:
                mode = 1
            else:
                mode = -1
        if mode == -1:
            if self.hook_x == None:
                return
            self.hooked = False
            self.hook_reeling = True
            return
        if self.hook_x != None:
            print("there already exists a hook")
            self.hook_buffer = True
            return
        self.hook_buffer = False
        self.hook_x, self.hook_y = self.x + self.width / 2, self.y + self.height / 2
        x_offset, y_offset = self.x + self.width / 2 + self.cam - mousepos[0], self.y + self.width / 2 - mousepos[1]
        a, b = self.get_hook_vels(x_offset, y_offset, self.hook_speed)
        self.hook_vel_left, self.hook_vel_up = -a, -b
    def get_hook_vels(self, x_offset, y_offset, speed):
        d = (x_offset ** 2 + y_offset ** 2) ** 0.5
        vx = speed * x_offset / d
        vy = speed * y_offset / d
        return vx, vy

    def magnetize(self, mousepos, distance, ox, oy):
        if self.magnet_polarity == 1:
            power =  1/distance * self.magnet_strength + 0.6
        elif self.magnet_polarity == -1:
            power =  3/distance * self.magnet_strength + 0.6
        x_share = abs(ox) / (abs(ox) + abs(oy))
        y_share = 1 - x_share
        dir_x, dir_y = 1,1 #1 is up and right
        if ox < 0:
            dir_x *= -1
        if oy < 0:
            dir_y *= -1
        dir_x *= self.magnet_polarity
        dir_y *= self.magnet_polarity
        x_share *= dir_x
        y_share *= dir_y
        self.vel_up += y_share * power
        self.vel_left += x_share * power

    def wall_jump(self, wall):
        xVel = 9
        if self.vel_up <= -5:
            self.vel_up = 7
        else:
            self.vel_up = min(13, self.vel_up + 12)
        self.jump = True
        if wall == 'l':
            if self.left:
                xVel -= 2
            else:
                self.sprite = self.sprites[1]
            self.vel_left -= xVel
        elif wall == 'r':
            if self.right:
                xVel -= 2
            else:
                self.sprite = self.sprites[0]
            self.vel_left += xVel

    def movement(self):
        self.update_block_statuses()
        if self.hooked:
            x_offset, y_offset = self.x + self.width / 2 - self.hook_x, self.y + self.width / 2 - self.hook_y
            a, b = self.get_hook_vels(x_offset, y_offset, self.hook_power)
            self.vel_up += b * self.delta * self.offset
            self.vel_left += a * self.delta * self.offset

        if self.right:
            if self.character != 2:
                if self.grounded:
                    self.vel_left -= self.ground_acceleration * self.delta * self.offset
                else:
                    self.vel_left -= self.air_acceleration * self.delta * self.offset
            elif self.hooked:
                self.vel_left -= self.air_acceleration * self.delta * self.offset
            self.sprite = self.sprites[1]
        if self.left:
            if self.character != 2:
                if self.grounded:
                    self.vel_left += self.ground_acceleration * self.delta * self.offset
                else:
                    self.vel_left += self.air_acceleration * self.delta * self.offset

            elif self.hooked:
                self.vel_left += self.air_acceleration * self.delta * self.offset
            self.sprite = self.sprites[0]


        for i in range(self.speed_correction):
            if self.vel_left < -self.max_speed:
                self.vel_left += self.delta * self.offset
            if self.vel_left > self.max_speed:
                self.vel_left -= self.delta * self.offset

        if self.grounded:
            if not self.right and not self.left:
                if self.vel_left < 0:
                    self.vel_left += self.ground_friction * self.delta * self.offset
                elif self.vel_left > 0:
                    self.vel_left -= self.ground_friction * self.delta * self.offset
                if -self.ground_friction < self.vel_left < self.ground_friction:
                    self.vel_left = 0
        else:
            if not self.right and not self.left:
                if self.vel_left < 0:
                    self.vel_left += self.air_friction * self.delta * self.offset
                elif self.vel_left > 0:
                    self.vel_left -= self.air_friction * self.delta * self.offset
                if -self.air_friction < self.vel_left < self.air_friction:
                    self.vel_left = 0

        if not self.gravity:
            if self.vel_up < 0:
                self.vel_up += self.air_friction * self.delta * self.offset
            elif self.vel_up > 0:
                self.vel_up -= self.air_friction * self.delta * self.offset

        if self.gravity:
            if self.jump:
                if self.vel_up <= 0:
                    self.jump = False
            if not self.grounded:
                self.vel_up -= self.g * self.delta * self.offset

            if self.vel_up < self.max_fall_speed:
                self.vel_up = self.max_fall_speed
            if self.vel_up > self.max_speed and not self.jump:
                if self.hooked:
                    self.vel_up = self.max_speed
                pass
        else:
            if self.up:
                self.vel_up += self.air_acceleration * self.delta * self.offset
            if self.down:
                self.vel_up -= self.air_acceleration * self.delta * self.offset

            if self.vel_up < -self.max_speed:
                self.vel_up = -self.max_speed
            if self.vel_up > self.max_speed:
                self.vel_up = self.max_speed

        self.pixel_move()
    def pixel_move(self):
        divisor = int(max(abs(self.vel_left), abs(self.vel_up))) + 1
        for i in range(divisor):
            if not self.collision_finder(False, 'p'):
                if self.max_speed == self.boosted_max_speed:
                    self.create_particle(self.width - 10, self.display.speed_color, self.x + self.width / 2,
                                         self.y + self.height / 2 + 4, 0, 0, 0, 10, 4.5)
                else:
                    self.create_particle(self.width - 10, self.current_trail_color, self.x + self.width / 2,
                                         self.y + self.height / 2, 0, 0, 0, 10, 4.5)
                self.archive_cords = [self.x, self.y]
            self.x -= self.vel_left * self.delta * self.offset / divisor
            self.y -= self.vel_up * self.delta * self.offset / divisor
            self.update_block_statuses()
            self.collision_finder(True, 'p')
            if self.won:
                self.delete()
                break
        self.sprite_rect.x, self.sprite_rect.y = self.x, self.y

        try:
            if self.grounded and not self.bouncy_mode:
                self.jumps_left = self.jump_amount
        except:
            pass
    def delete(self):
        self.display.game.timer_text.hidden = True
        if self.won:
            self.display.game.current_display = self.display.game.displays['win_screen']
            self.display.game.current_display.finish_time = self.display.game.getTimer()
            self.display.game.current_display.actual_time_text.update_text(str(self.display.game.getTimer()))
        self.display.objects.remove(self)
        self.display.particles = []
        del self




import time as czas
import pygame
from App import particle

class Player:
    def __init__(self, display):
        self.display = display
        self.display.objects.append(self)
        self.offset = 60
        self.cam = self.display.camera

        self.current_stretch = 0 #positive means it's wider and shorter; negative means it's taller and thinner
        self.target_stretch = 0
        self.max_stretch = 14
        self.min_stretch = -self.max_stretch
        self.stretch_delta = 2
        self.current_sprite_direction = 1

        self.g = 0.6
        self.regular_max_speed = 8
        self.boosted_max_speed = 16
        self.max_speed = self.regular_max_speed #current max speed
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



        self.width = self.display.tile_size + 10
        self.height = self.width
        self.id = self.display.game.character # 0 is runner, 1 is bouncer, 2 is hooker, 3 is magneter, 4 is rocketeer, 9 is debugger
        self.sprites = None
        # rocketeer_color = [200, 150, 50]
        # rocketeer_trail_color = [110, 70, 20]
        # rocketeer will have a rocket to perform rocketboosts away from the mouse

    def init_phase_2(self):
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
        # keep track of whether the player is on the ground or in the air
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
    #collision finder might need to be separated for hooker but for now its inherited
    def collision_finder(self, act_or_not: bool, entity):
        if entity == 'p':
            y = self.y
            x = self.x
            w = self.width
            h = self.height
        else: #entity = hook
            y = self.hook_y
            x = self.hook_x
            w = 1
            h = 1
            if self.hook_reeling:
                return

        for row in range(int(y // self.display.tile_size - 1), int(y // self.display.tile_size + 3)):
            if self.won: return False
            for column in range(int(x // self.display.tile_size - 1), int(x // self.display.tile_size + 3)):
                print(row, column)
                try:
                    block_type = self.display.current_map[row][column]
                    if block_type == 5:
                        block = (column * self.display.tile_size, row * self.display.tile_size, self.display.tile_size,
                                 self.display.tile_size)
                        if self.collision((x, y, w, h), block) and entity == 'p':
                            print('Your time: ', self.display.game.getTimer())
                            self.reset(False)
                            self.won = True
                            break
                    if block_type not in (1, 2, 3, 4): continue

                    block = (column * self.display.tile_size, row * self.display.tile_size, self.display.tile_size,
                             self.display.tile_size)
                    if not self.collision((x, y, w, h), block): continue
                    if not act_or_not: return True

                    if entity == 'p':
                        if self.nudge(self.detection(block), block, self.display.current_map[row][column]) == True and self.character == 0:
                            self.vel_up = self.min_bounce * 3
                            self.jumps_left = 1
                        # pygame.draw.rect(self.display.screen, (200, 0, 0), (block[0] + self.cam,block[1],block[2],block[3]))
                    elif entity == 'h':
                        self.hooked = True
                        self.hook_vel_left, self.hook_vel_up = 0, 0
                        pygame.draw.rect(self.display.screen, (200, 100, 200), (block[0] + self.cam, block[1], block[2], block[3]))

                except:
                    pass
        return False

    def tick(self):
        self.delta = self.display.game.delta_time
        if self.just_started:
            self.just_started = False
            self.reset(True)
            self.display.game.timer_text.hidden = True
        self.cam = self.display.camera
        current_color = []
        self.current_trail_color = []
        for i in range(3):
            if self.player_color[i] == max(self.player_color):
                current_color.append(int(self.player_color[i] - 70 * (1 - self.jumps_left)))
                self.current_trail_color.append(int(self.trail_color[i] - 30 * (1 - self.jumps_left)))
            else:
                current_color.append(int(self.player_color[i] + 40 * (1 - self.jumps_left)))
                self.current_trail_color.append(int(self.trail_color[i] + 20 * (1 - self.jumps_left)))

        self.sprite_rect.y = self.y + self.current_stretch
        self.sprite_rect.x = self.display.camera + self.x - self.current_stretch/2

        self.display.screen.blit(self.sprite, self.sprite_rect)

        if self.display.game.countdown < 1:
            self.movement()
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
            if event.key in (pygame.K_w, pygame.K_UP):
                self.up = True

        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_a, pygame.K_LEFT):
                self.left = False
            if event.key in (pygame.K_d, pygame.K_RIGHT):
                self.right = False
            if event.key in (pygame.K_s, pygame.K_DOWN):
                self.down = False
            if event.key in (pygame.K_w, pygame.K_UP):
                self.up = False

    def is_founded(self, source=None):
        bounce = False
        for row in range(int(self.y // self.display.tile_size - 1), int(self.y // self.display.tile_size + 3)):
            for column in range(int(self.x // self.display.tile_size - 1), int(self.x // self.display.tile_size + 3)):
                try:
                    blockType = self.display.current_map[row][column]
                    if not blockType in (1, 2, 3, 4): continue
                    block = (column * self.display.tile_size, row * self.display.tile_size, self.display.tile_size,
                             self.display.tile_size)
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
            if source == 'tick':
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
                    if not self.display.current_map[row][column] in (1,2,3,4): continue
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
                    if not self.display.current_map[row][column] in (1,2,3,4): continue
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
                    if not self.display.current_map[row][column] in (1,2,3,4): continue
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

    def movement(self):
        self.update_block_statuses()
        self.turn_sprite()
        if self.grounded:
            friction = self.ground_friction
            acceleration = self.ground_acceleration
        else:
            friction = self.air_friction
            acceleration = self.air_acceleration
        if self.right:
            self.vel_left -= acceleration * self.delta * self.offset
        if self.left:
            self.vel_left += acceleration * self.delta * self.offset
        for i in range(self.speed_correction):
            if self.vel_left < -self.max_speed:
                self.vel_left += self.delta * self.offset
            if self.vel_left > self.max_speed:
                self.vel_left -= self.delta * self.offset

        if not self.right and not self.left:
            if self.vel_left < 0:
                self.vel_left += friction * self.delta * self.offset
            elif self.vel_left > 0:
                self.vel_left -= friction * self.delta * self.offset
            if -friction < self.vel_left < friction:
                self.vel_left = 0

        if self.gravity:
            if self.jump:
                if self.vel_up <= 0:
                    self.jump = False
            if not self.grounded:
                self.vel_up -= self.g * self.delta * self.offset

            if self.vel_up < self.max_fall_speed:
                self.vel_up = self.max_fall_speed
        else:
            if self.up:
                self.vel_up += self.air_acceleration * self.delta * self.offset
            if self.down:
                self.vel_up -= self.air_acceleration * self.delta * self.offset

            if self.vel_up < -self.max_speed:
                self.vel_up = -self.max_speed
            if self.vel_up > self.max_speed:
                self.vel_up = self.max_speed

        self.apply_squash_stretch()
        self.pixel_move()
    def pixel_move(self):
        divisor = int(max(abs(self.vel_left), abs(self.vel_up))) + 1
        for i in range(divisor):
            if not self.collision_finder(False, 'p'):
                if self.max_speed == self.boosted_max_speed:
                    particle.Particle(self.display, (self.width - 10) / 2, self.display.speed_color,self.x + self.width / 2,
                                      self.y + self.height / 2 + 4, 0, 0, 0, 10, 4.5)
                else:
                    particle.Particle(self.display, (self.width - 10) / 2, self.current_trail_color, self.x + self.width / 2,
                                      self.y + self.height / 2 + 4, 0, 0, 0, 10, 4.5)
                self.archive_cords = [self.x, self.y]
            self.x -= self.vel_left * self.delta * self.offset / divisor
            self.y -= self.vel_up * self.delta * self.offset / divisor
            self.update_block_statuses()
            self.collision_finder(True, 'p')
            if self.won:
                self.delete()
                break
        self.sprite_rect.x, self.sprite_rect.y = self.x, self.y

    def turn_sprite(self):
        if self.right:
            self.sprite = self.sprites[1]
            self.current_sprite_direction = 1
        if self.left:
            self.sprite = self.sprites[0]
            self.current_sprite_direction = 0
    def apply_squash_stretch(self):
        if self.current_stretch == self.min_stretch and self.vel_up < 10:
            self.target_stretch = self.min_stretch/2
        if self.target_stretch < 0:
            if 2 > self.vel_up > -2:
                self.target_stretch = 0
        if self.target_stretch < self.current_stretch:
            self.current_stretch -= self.stretch_delta
        if self.target_stretch > self.current_stretch:
            self.current_stretch += self.stretch_delta
        self.sprite = pygame.transform.scale(self.sprites[self.current_sprite_direction], (self.width + self.current_stretch, self.height - self.current_stretch))
    def delete(self):
        pygame.mouse.set_cursor(self.display.game.cursors['standard'])
        self.display.game.timer_text.hidden = True
        musicTime = pygame.mixer.music.get_pos() * 3 / 2000
        pygame.mixer.music.load("Assets/Music/Menu music.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_pos(musicTime)
        if self.won:
            self.display.game.current_display = self.display.game.displays['win_screen']
            self.display.game.current_display.finish_time = self.display.game.getTimer()
            self.display.game.current_display.actual_time_text.update_text(str(self.display.game.getTimer()))
        self.display.objects.remove(self)
        self.display.particles = []
        del self
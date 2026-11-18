import Characters.player as player
import pygame

# hooker has a grappling hook

class Hooker(player.Player):
    def __init__(self, display):
        player.Player.__init__(self, display)

        self.name = "Hooker"
        self.id = 2
        self.player_color, self.trail_color = [200, 200, 30], [90, 90, 20]

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

        self.bouncy_mode = True
        self.g = 0.9
        self.max_fall_speed, self.max_speed, self.regular_max_speed = -15, 15, 15
        self.speed_correction = 10
        self.jump_speed_boost = 0
        self.jump_amount = 0
        self.sprites = [pygame.image.load("Assets/Sprites/yellow_left.png"), pygame.image.load("Assets/Sprites/yellow_right.png")]

        self.init_phase_2()

    def reset(self, restart):
        player.Player.reset(self, restart)
        self.hook_vel_up = 0
        self.hook_vel_left = 0
        self.hook_reeling = False
        self.hook_x = None
        self.hook_y = None
        self.hooked = False

    def nudge(self, direction: str, block: list, blockType):
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

        player.Player.nudge(self, direction, block, blockType)

    def tick(self):
        self.set_correct_cursor()

        player.Player.tick(self)
        if self.display.game.countdown < 1:
            if self.hook_x != None:
                self.hook_movement()
        current_color, self.current_trail_color = self.player_color, self.trail_color

    def events(self, event):
        player.Player.events(self, event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LSHIFT and self.display.game.countdown < 1:
                self.shoot_hook(pygame.mouse.get_pos(), 2)
        if event.type == pygame.MOUSEBUTTONDOWN and self.display.game.countdown < 1:
            if event.button == 1:
                self.shoot_hook(pygame.mouse.get_pos())
        if event.type == pygame.MOUSEBUTTONUP and self.display.game.countdown < 1:
            if event.button == 1:
                self.shoot_hook(pygame.mouse.get_pos(), -1)
                self.hook_buffer = False

    def set_correct_cursor(self):
        if not self.display.game.custom_cursors: return
        pygame.mouse.set_cursor(self.display.game.cursors['grappling'])

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
                    self.shoot_hook(pygame.mouse.get_pos())
                return

        pygame.draw.line(self.display.screen, line_color, (self.x + self.cam + self.width / 2, self.y + self.width / 2), (self.hook_x + self.cam, self.hook_y), 4)
        pygame.draw.circle(self.display.screen, self.player_color, (self.hook_x + self.cam, self.hook_y), self.hook_size / 2)
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

    def movement(self):
        self.update_block_statuses()
        self.turn_sprite()

        if self.hooked:
            x_offset, y_offset = self.x + self.width / 2 - self.hook_x, self.y + self.width / 2 - self.hook_y
            a, b = self.get_hook_vels(x_offset, y_offset, self.hook_power)
            self.vel_up += b * self.delta * self.offset
            self.vel_left += a * self.delta * self.offset
        for i in range(self.speed_correction):
            if self.vel_left < -self.max_speed:
                self.vel_left += self.delta * self.offset
            if self.vel_left > self.max_speed:
                self.vel_left -= self.delta * self.offset

        if self.grounded: friction = self.ground_friction
        else: friction = self.air_friction

        if not self.right and not self.left:
            if self.vel_left < 0:
                self.vel_left += friction * self.delta * self.offset
            elif self.vel_left > 0:
                self.vel_left -= friction * self.delta * self.offset
            if -friction < self.vel_left < friction:
                self.vel_left = 0
        if self.gravity and not self.grounded:
            self.vel_up -= self.g * self.delta * self.offset
        if self.vel_up < self.max_fall_speed:
            self.vel_up = self.max_fall_speed
        if self.vel_up > self.max_speed:
            self.vel_up = self.max_speed
        self.apply_squash_stretch()
        self.pixel_move()

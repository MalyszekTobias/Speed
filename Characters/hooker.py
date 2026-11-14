import App.player as player
import pygame

# hooker has a grappling hook

class Hooker(player.Player):
    def __init__(self, display):
        player.Player.__init__(self, display)

        self.name = "Hooker"
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

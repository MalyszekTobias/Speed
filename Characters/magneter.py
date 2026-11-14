import App.player as player
import pygame

# magneter can be attracted or repelled from the cursor

class Magneter(player.Player):
    def __init__(self, display):
        player.Player.__init__(self, display)

        self.name = "Magneter"
        self.player_color, self.trail_color = [60, 60, 200], [30, 30, 90]

        self.magnet_strength = 30
        self.magnet_polarity = 0
        self.numb_magnet_radius = 100

        self.bouncy_mode = False
        self.gravity = False
        self.sprites = [pygame.image.load("Assets/Sprites/teal_left.png"), pygame.image.load("Assets/Sprites/teal_right.png")]

        self.init_phase_2()

    def nudge(self, direction: str, block: list, blockType):
        if direction == 'down':
            self.target_stretch = self.max_stretch
            self.current_stretch = self.max_stretch / 2
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

        player.Player.nudge(self, direction, block, blockType)
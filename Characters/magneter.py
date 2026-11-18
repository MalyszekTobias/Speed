import Characters.player as player
import pygame

# magneter can be attracted or repelled from the cursor

class Magneter(player.Player):
    def __init__(self, display):
        player.Player.__init__(self, display)

        self.name = "Magneter"
        self.id = 3
        self.player_color, self.trail_color = [60, 60, 200], [30, 30, 90]

        self.magnet_strength = 30
        self.magnet_polarity = 0
        self.numb_magnet_radius = 100

        self.bouncy_mode = False
        self.gravity = True
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

    def tick(self):
        self.set_correct_cursor()

        pygame.draw.circle(self.display.screen, (255, 255, 255),
                           (self.display.camera + self.x + self.width / 2, self.y + self.height / 2),
                           self.numb_magnet_radius, 3)
        mousepos = pygame.mouse.get_pos()
        x_offset, y_offset = self.x + self.width / 2 + self.cam - mousepos[0], self.y + self.width / 2 - mousepos[1]
        distance = (x_offset ** 2 + y_offset ** 2) ** 0.5
        if distance > self.numb_magnet_radius and self.magnet_polarity != 0:
            self.magnetize(mousepos, distance, x_offset, y_offset)

        player.Player.tick(self)

    def events(self, event):
        player.Player.events(self, event)
        if event.type == pygame.MOUSEBUTTONDOWN and self.display.game.countdown < 1:
            if event.button == 1:
                self.magnet_polarity = -1
            elif event.button == 3:
                self.magnet_polarity = 1
        if event.type == pygame.MOUSEBUTTONUP and self.display.game.countdown < 1:
            if event.button == 1 and self.magnet_polarity == -1:
                self.magnet_polarity = 0
            elif event.button == 3 and self.magnet_polarity == 1:
                self.magnet_polarity = 0

    def set_correct_cursor(self):
        if not self.display.game.custom_cursors: return

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

    def pixel_move(self):
        player.Player.pixel_move(self)
        try:
            if self.grounded:
                self.jumps_left = self.jump_amount
        except:
            pass
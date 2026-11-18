import Characters.player as player
import pygame

# runner can run along the floor and jump twice, pretty normal stuff

class Runner(player.Player):
    def __init__(self, display):
        player.Player.__init__(self, display)

        self.name = "Runner"
        self.id = 0
        self.player_color, self.trail_color = [30, 200, 30], [20, 90, 20]

        self.bouncy_mode = False
        self.max_speed, self.regular_max_speed = 9, 9
        self.sprites = [pygame.image.load("Assets/Sprites/green_left.png"), pygame.image.load("Assets/Sprites/green_right.png")]

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

    def events(self, event):
        player.Player.events(self, event)
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_s, pygame.K_DOWN):
                self.down = True
                if self.hugs_right() and not self.grounded:
                    self.wall_jump('r')
                elif self.hugs_left() and not self.grounded:
                    self.wall_jump('l')
            if event.key in (pygame.K_SPACE, pygame.K_UP) and self.display.game.countdown < 1:
                    if self.jumps_left > 0:
                        self.jump = True
                        self.jumps_left -= 1
                        self.vel_up = self.jump_length
                        self.target_stretch = self.min_stretch
                        if self.grounded:
                            self.y -= 1
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
            if event.key == pygame.K_SPACE:
                if self.jump:
                    self.vel_up /= 2
                    self.jump = False
                    self.target_stretch = 0

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
                self.current_sprite_direction = 1
            self.vel_left -= xVel
        elif wall == 'r':
            if self.right:
                xVel -= 2
            else:
                self.sprite = self.sprites[0]
                self.current_sprite_direction = 0
            self.vel_left += xVel

    def pixel_move(self):
        player.Player.pixel_move(self)
        try:
            if self.grounded:
                self.jumps_left = self.jump_amount
        except:
            pass
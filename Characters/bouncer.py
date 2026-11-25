import Characters.player as player
import pygame

# bouncer bounces from every block, has 1 jump in the air after bouncing from a white / non-red floor

class Bouncer(player.Player):
    def __init__(self, display):
        player.Player.__init__(self, display)

        self.name = 'Bouncer'
        self.id = 1
        self.player_color, self.trail_color = [200, 30, 30], [90, 20, 20]

        self.jump_recovery_from_all_direction_bounces = True
        self.bouncy_mode = True
        self.gravity = True
        self.min_bounce = 5
        self.wall_and_ceiling_bounce = 5
        self.floor_bounce = 5
        self.sprites = [pygame.image.load("Assets/Sprites/red_left.png"), pygame.image.load("Assets/Sprites/red_right.png")]

        self.init_phase_2()

    def nudge(self, direction: str, block: list, blockType):
        bounceMulti = 1
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
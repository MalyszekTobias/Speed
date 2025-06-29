import time as czas
from random import random
import Assets
import pygame
from pygame import *
from app import particle
from mapMaker import tileSize, height, screen
import random as ran

class Player:
    def __init__(self, display):
        self.display = display
        self.display.objects.append(self)
        self.offset = 60

        self.g = 0.6
        self.regularMaxSpeed = 8
        self.boostedMaxSpeed = 16
        self.maxSpeed = self.regularMaxSpeed
        self.maxFallSpeed = -20
        self.regularJump = 16
        self.boostedJump = 23
        self.jumpLength = self.regularJump
        self.airAcceleration = 0.4
        self.groundAcceleration = 1
        self.acceleration = self.airAcceleration
        self.airFriction = 0.1
        self.groundFriction = 0.5
        self.gravity = True
        self.wallAndCeilingBounce = 6
        self.floorBounce = 5
        self.minBounce = 5
        self.bounceBlockPower = 2
        self.energyConservation = 0.7
        self.bouncyMode = True
        self.jumpRecoveryFromAllDirectionBounces = False
        self.jumpRecoveryFromReds = 0
        self.jumpAmount = 1
        self.jumpSpeedBoost = 4
        self.speedCorrection = 1

        self.hookX = None
        self.hookY = None
        self.hookSize = 20
        self.hooked = False
        self.hookSpeed = 40
        self.hookPower = 3
        self.hookLength = 520
        self.hookVelUp = 0
        self.hookVelLeft = 0
        self.hookReeling = False


        self.width = self.display.tileSize + 10
        self.height = self.width

        self.character = 1 # 0 is debugger, 1 is bouncer, 2 is runner, 3 is hooker, 4 is magneter

        self.colors = [[200, 200, 200], [200, 30, 30], [30, 200, 30], [200, 200, 30], [60, 60, 200]]
        self.trailColors = [[90, 90, 90], [90, 20, 20], [20, 90, 20], [90, 90, 20], [30, 30, 90]]

        if self.character == 0:
            self.bouncyMode = False
            self.gravity = False
            self.airAcceleration = 2
            self.groundAcceleration = 2
            self.maxSpeed = self.boostedMaxSpeed
            self.sprites = [pygame.image.load("Assets/Sprites/teal_left.png"), pygame.image.load("Assets/Sprites/teal_right.png")]
        if self.character == 1:
            # bouncer bounces from every block, has 1 jump in the air after bouncing from a white floor
            self.bouncyMode = True
            self.gravity = True
            self.g = 0.6
            self.minBounce = 5
            self.wallAndCeilingBounce = 5
            self.floorBounce = 5
            self.sprites = [pygame.image.load("Assets/Sprites/red_left.png"), pygame.image.load("Assets/Sprites/red_right.png")]
        if self.character == 2:
            # runner can run along the floor and jump twice, pretty normal stuff
            self.bouncyMode = False
            self.sprites = [pygame.image.load("Assets/Sprites/green_left.png"), pygame.image.load("Assets/Sprites/green_right.png")]
        if self.character == 3:
            # hooker has 1 small jump and a hook
            self.bouncyMode = True
            self.g = 0.9
            self.maxFallSpeed, self.maxSpeed, self.regularMaxSpeed = -15, 15, 15
            self.speedCorrection = 10
            self.jumpSpeedBoost = 0
            self.jumpAmount = 0
            self.sprites = [pygame.image.load("Assets/Sprites/yellow_left.png"), pygame.image.load("Assets/Sprites/yellow_right.png")]

        # magneter will get attracted to the mouse, no jump, no gravity
        self.playerColor, self.trailColor = self.colors[self.character], self.trailColors[self.character]

        for s in range(len(self.sprites)):
            self.sprites[s] = pygame.transform.scale(self.sprites[s], (self.width, self.height))
            self.sprite_rect = self.sprites[s].get_rect()
            self.sprite_rect.x,self.sprite_rect.y = 0, 0
        self.sprite = self.sprites[1]
        print(self.sprite)
        self.x = self.display.spawnCords[0]
        self.y = self.display.spawnCords[1]
        self.sprite_rect.x, self.sprite_rect.y = self.x, self.y
        self.velUp = 0
        self.velLeft = 0
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.jump = False
        self.grounded = False
        self.hugLeft = False
        self.hugRight = False
        self.touchingUp = False
        self.archiveCords = [self.x, self.y]
        self.jumpsLeft = self.jumpAmount
        self.justStarted = True
        self.won = False

    def restart(self, start):
        if start:
            self.display.game.countdown = 59
            self.display.game.pauseSum = 0
            self.display.game.startTime = czas.time_ns() // 1000000
            self.display.game.countdownText.hidden = False
        self.display.particles = []
        self.x = self.display.spawnCords[0]
        self.y = self.display.spawnCords[1]
        self.velUp = 0
        self.velLeft = 0
        self.jump = False
        self.grounded = False
        self.hugLeft = False
        self.hugRight = False
        self.touchingUp = False
        self.archiveCords = [self.x, self.y]
        self.jumpsLeft = self.jumpAmount
        self.hookVelUp = 0
        self.hookVelLeft = 0
        self.hookReeling = False
        self.hookX = None
        self.hookY = None
        self.hooked = False

        self.won = False

    def collision(self, list, block: list) -> bool:
        if self.verticalCollision(list[1], list[3], block[1], block[3]) and self.horizontalCollision(list[0], list[2], block[0], block[2]):
            return True
        return False
    # Checks if two objects share a horizontal line:
    def verticalCollision(self, y1, h1, y2, h2):

        if y2 + h2 < y1:
            return False
        if y1 + h1 < y2:
            return False
        return True  # checks
    # Checks if two objects share a vertical line:
    def horizontalCollision(self, x1, w1, x2, w2):
        if x2 + w2 < x1:
            return False
        if x1 + w1 < x2:
            return False
        return True
    def nudge(self, direction: str, block: list, blockType):
        if self.bouncyMode:
            bounceMulti = 1
            if self.character == 3:
                bounceMulti = 0

            if blockType == 4:
                r, c = block[1] // self.display.tileSize, block[0] // self.display.tileSize
                bouncable = False
                if self.x < block[0]:
                    if self.display.currentMap[r][c - 1] == 4:
                        bouncable = True
                elif self.x + self.width > block[0] + block[2]:
                    if self.display.currentMap[r][c + 1] == 4:
                        bouncable = True
                else:
                    bouncable = True
                if bouncable:
                    bounceMulti = 1.5

                elif self.character == 3:
                    bounceMulti = 0
                    print(None)
            if self.jumpRecoveryFromAllDirectionBounces:
                self.jumpsLeft = self.jumpAmount

            if direction == 'down':
                self.y = block[1] - self.height
                if self.velUp < -self.minBounce * bounceMulti:
                    self.velUp *= -self.energyConservation * bounceMulti
                elif 0 > self.velUp:
                    self.velUp = self.minBounce * bounceMulti

                if bounceMulti == 1:
                    self.jumpsLeft = self.jumpAmount
                return

            elif direction == 'up':
                self.y = self.archiveCords[1]

                if self.velUp > self.minBounce * bounceMulti:
                    self.velUp *= -self.energyConservation * bounceMulti
                elif 0 < self.velUp:
                    self.velUp = -self.minBounce * bounceMulti

                self.touchingUp = True
                return

            elif direction == 'left':
                self.x = self.archiveCords[0]

                if self.velLeft > self.minBounce * bounceMulti:
                    self.velLeft *= -self.energyConservation * bounceMulti
                elif 0 < self.velLeft:
                    self.velLeft = -self.minBounce * bounceMulti
                if self.velUp < 10:
                    self.velUp += 4.5
                self.hugLeft = True
                return
            elif direction == 'right':
                self.x = self.archiveCords[0]

                if self.velLeft < -self.minBounce * bounceMulti:
                    self.velLeft *= self.energyConservation * bounceMulti
                elif 0 > self.velLeft:
                    self.velLeft = self.minBounce * bounceMulti
                if self.velUp < 10:
                    self.velUp += 4.5
                self.hugRight = True
                return
        else:
            if direction == 'down':
                self.y = block[1] - self.height - 1
                self.velUp = 0
                r,c = block[1] // self.display.tileSize, block[0] // self.display.tileSize
                bouncable = False
                if self.x < block[0]:
                    if self.display.currentMap[r][c - 1] == 4:
                        bouncable = True
                elif self.x + self.width > block[0] + block[2]:
                    if self.display.currentMap[r][c + 1] == 4:
                        bouncable = True
                else:
                    bouncable = True

                if blockType != 4:
                    return False
                elif bouncable:
                    return True

            elif direction == 'up':
                self.y = block[1] + block[3] + 1
                self.velUp = 0
                return
            elif direction == 'left':
                self.x = block[0] + block[2] + 1
                self.velLeft = 0
                return
            elif direction == 'right':
                self.x = block[0] - self.width - 1
                self.velLeft = 0
                return
    def corner(self, block: list):
        mapx, mapy = block[0] // self.display.tileSize, block[1] // self.display.tileSize


        right, down = False, False
        c = self.x + self.width - block[0]
        d = self.y + self.height - block[1]
        if block[0] + block[2] - self.x < c:
            c = block[0] + block[2] - self.x
            right = True
            if self.hugLeft:
                return 'left'
        elif self.hugRight:
            return 'right'
        if block[1] + block[3] - self.y < d:
            d = block[1] + block[3] - self.y
            down = True
            if self.isCapped():
                return 'up'
        elif self.isFounded():
            return 'down'
        a, b = abs(self.x - self.archiveCords[0]), abs(self.y - self.archiveCords[1])
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
        if self.horizontalCollision(self.archiveCords[0], self.width, block[0], block[2]):
            if self.archiveCords[1] + self.height < block[1]:
                return 'down'  # going down
            else:
                return 'up'
        elif self.verticalCollision(self.archiveCords[1], self.height, block[1], block[3]):
            if self.archiveCords[0] + self.width < block[0]:
                return 'right'  # going right
            else:
                return 'left'
        else:
            return self.corner(block)
    def collisionFinder(self, actOrNot: bool, entity):
        if entity == 'p':
            y = self.y
            x = self.x
            w = self.width
            h = self.height
        elif entity == 'h':
            y = self.hookY
            x = self.hookX
            w = 1
            h = 1
            if self.hookReeling:
                return

        for row in range(int(y // self.display.tileSize - 1), int(y // self.display.tileSize + 3)):
            if not self.won:
                for column in range(int(x // self.display.tileSize - 1), int(x // self.display.tileSize + 3)):
                    try:
                        if not self.display.currentMap[row][column] in (0, 5, 6, 7, 8, 9):
                            block = (column * self.display.tileSize, row * self.display.tileSize, self.display.tileSize,
                                     self.display.tileSize)
                            if self.collision((x, y, w, h), block):
                                if actOrNot:
                                    if entity == 'p':
                                        if self.nudge(self.detection(block), block, self.display.currentMap[row][column]) == True and self.character == 2:
                                            self.velUp = self.minBounce * 2
                                            self.jumpsLeft = 1
                                        # pygame.draw.rect(self.display.screen, (200, 0, 0), (block[0] + self.cam,block[1],block[2],block[3]))
                                    elif entity == 'h':
                                        self.hooked = True
                                        self.hookVelLeft, self.hookVelUp = 0, 0
                                        pygame.draw.rect(self.display.screen, (200, 100, 200), (block[0] + self.cam, block[1], block[2], block[3]))
                                else:
                                    return True
                        elif self.display.currentMap[row][column] == 5:
                            block = (column * self.display.tileSize, row * self.display.tileSize, self.display.tileSize,
                                     self.display.tileSize)
                            if self.collision((x, y, w, h), block) and entity == 'p':
                                print('Your time: ', self.display.game.getTimer(), self.x)
                                self.restart(False)
                                self.won = True
                                break

                    except:
                        pass
        return False

    def createParticle(self, size, color, x, y, velRight, velUp, g, lifetime, shrink):
        self.particle = particle.Particle(self.display, size / 2, color, x, y, velRight, velUp, g, lifetime, shrink)
        self.display.particles.append(self.particle)
    def render(self):
        self.delta = self.display.game.delta_time
        if self.justStarted:
            self.justStarted = False
            self.restart(True)
            self.display.game.timerText.hidden = True
        self.cam = self.display.camera
        currentColor = []
        self.currentTrailColor = []
        for i in range(3):
            if self.playerColor[i] == max(self.playerColor):
                currentColor.append(int(self.playerColor[i] - 70 *(1 - self.jumpsLeft)))
                self.currentTrailColor.append(int(self.trailColor[i] - 30 *(1 - self.jumpsLeft)))
            else:
                currentColor.append(int(self.playerColor[i] + 40 * (1-self.jumpsLeft)))
                self.currentTrailColor.append(int(self.trailColor[i] + 20 * (1-self.jumpsLeft)))

        if self.character == 3:
            currentColor, currentTrailColor = self.playerColor, self.trailColor
        if self.x + self.width / 2 > self.display.game.width / 2:
            self.sprite_rect.x, self.sprite_rect.y = (self.display.game.width - self.width) / 2, self.y

            # pygame.draw.rect(self.display.screen, currentColor,((self.display.game.width - self.width) / 2 - 1, self.y - 1, self.width + 2, self.height + 2))    # camera work
        else:
            self.sprite_rect.x, self.sprite_rect.y = self.x, self.y

            # pygame.draw.rect(self.display.screen, currentColor, (self.x - 1, self.y - 1, self.width + 2, self.height + 2))
        self.display.screen.blit(self.sprite, self.sprite_rect)


        if self.display.game.countdown < 1:
            self.movement()
            if self.character == 3 and self.hookX != None:
                self.hook_movement()


        return self.x + self.width / 2 - self.display.game.width / 2
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
            if event.key == pygame.K_LSHIFT and self.display.game.countdown < 1:
                self.shootHook(pygame.mouse.get_pos())
            if event.key == pygame.K_SPACE or event.key == K_UP:
                if self.display.game.countdown < 1:
                    if self.hugsRight() and not self.grounded:
                        self.wall_jump('r')
                    elif self.hugsLeft() and not self.grounded:
                        self.wall_jump('l')
                    elif self.jumpsLeft > 0:
                        self.jump = True
                        self.jumpsLeft -= 1
                        self.velUp = self.jumpLength
                        if self.grounded:
                            self.y -= 1
                            if self.character == 2:
                                self.jumpsLeft += 1
                        if self.right and not self.left:
                            self.velLeft -= self.jumpSpeedBoost
                        elif self.left and not self.right:
                            self.velLeft += self.jumpSpeedBoost



            if event.key == pygame.K_r:
                self.restart(True)

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
                    self.velUp /= 2
                    self.jump = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.display.game.countdown < 1:
                self.shootHook(pygame.mouse.get_pos())

    def isFounded(self):
        for row in range(int(self.y // self.display.tileSize - 1), int(self.y // self.display.tileSize + 3)):
            for column in range(int(self.x // self.display.tileSize - 1), int(self.x // self.display.tileSize + 3)):
                try:
                    if not self.display.currentMap[row][column] in (0, 5, 6, 7, 8, 9):
                        block = (column * self.display.tileSize, row * self.display.tileSize, self.display.tileSize,
                                 self.display.tileSize)
                        # if block[1] == self.y + self.height and block[0]
                        if self.collision((self.x + 1, self.y + self.height, self.width - 2, 1), block):
                            self.maxSpeed = self.regularMaxSpeed
                            self.acceleration = self.groundAcceleration
                            self.jumpLength = self.regularJump

                            if self.display.currentMap[row][column] == 2:
                                self.maxSpeed = self.boostedMaxSpeed
                                self.acceleration = self.groundAcceleration * 2
                            if self.display.currentMap[row][column] == 3:
                                self.jumpLength = self.boostedJump
                            return True
                except:
                    pass
        self.acceleration = self.airAcceleration
        if self.maxSpeed == self.boostedMaxSpeed:
            self.acceleration = self.groundAcceleration
        return False
    def isCapped(self):
        for row in range(int(self.y // self.display.tileSize - 1), int(self.y // self.display.tileSize + 2)):
            for column in range(int(self.x // self.display.tileSize - 1), int(self.x // self.display.tileSize + 3)):
                try:
                    if not self.display.currentMap[row][column] in (0, 5, 6, 7, 8, 9):
                        block = (column * self.display.tileSize, row * self.display.tileSize, self.display.tileSize,
                                 self.display.tileSize)
                        if self.collision((self.x + 1, self.y, self.width - 2, 1), block):
                            return True
                except:
                    pass
        return False
    def hugsLeft(self):
        for row in range(int(self.y // self.display.tileSize - 1), int(self.y // self.display.tileSize + 3)):
            for column in range(int(self.x // self.display.tileSize - 1), int(self.x // self.display.tileSize + 3)):
                try:
                    if not self.display.currentMap[row][column] in (0, 5, 6, 7, 8, 9):
                        block = (column * self.display.tileSize, row * self.display.tileSize, self.display.tileSize,
                                 self.display.tileSize)
                        if self.collision((self.x - 1, self.y - 1, 1, self.height - 2), block):
                            return True
                except:
                    pass
        return False
    def hugsRight(self):
        for row in range(int(self.y // self.display.tileSize - 1), int(self.y // self.display.tileSize + 3)):
            for column in range(int(self.x // self.display.tileSize - 1), int(self.x // self.display.tileSize + 3)):
                try:
                    if not self.display.currentMap[row][column] in (0, 5, 6, 7, 8, 9):
                        block = (column * self.display.tileSize, row * self.display.tileSize, self.display.tileSize,
                                 self.display.tileSize)
                        if self.collision((self.x + self.width, self.y - 1, 1, self.height - 2), block):
                            return True
                except:
                    pass
        return False
    def updateBlockStatuses(self):
        self.grounded = self.isFounded()
        self.hugLeft = self.hugsLeft()
        self.hugRight = self.hugsRight()
        self.touchingUp = self.isCapped()

    def hook_movement(self):
        lineColor = (100, 200, 100)

        if self.hookReeling:
            a, b = self.getHookVels(self.hookX - self.x - self.width / 2, self.hookY - self.y - self.width / 2, self.hookSpeed)
            self.hookVelLeft = -a
            self.hookVelUp = -b
            lineColor = (200, 100, 100)

        if not self.hooked:
            divisor = int(max(abs(self.hookVelLeft), abs(self.velUp))) + 1
            for i in range(divisor):
                self.collisionFinder(True, 'h')
                if not self.hookReeling:
                    d = ((self.x + self.width/2 - self.hookX) ** 2 + (self.y + self.height/2 - self.hookY) ** 2) ** 0.5
                    if d > self.hookLength:
                        self.hookReeling = True
                if not self.hooked:
                    self.hookX += self.hookVelLeft * self.delta * self.offset / divisor
                    self.hookY += self.hookVelUp * self.delta * self.offset / divisor
        if self.hookReeling or self.hooked:
            hitbox = 0
            if self.hooked:
                hitbox = 5
            if self.collision((self.hookX, self.hookY, self.hookSize, self.hookSize), (self.x - hitbox, self.y - hitbox, self.width + 2*hitbox, self.height + 2*hitbox)):
                self.hookX, self.hookY = None, None
                self.hookReeling = False
                self.hookVelUp = 0
                self.hookVelLeft = 0
                self.hooked = False
                return

        pygame.draw.line(self.display.screen, lineColor, (self.x + self.cam + self.width / 2, self.y + self.width / 2), (self.hookX + self.cam, self.hookY), 4)
        pygame.draw.circle(self.display.screen, self.playerColor, (self.hookX + self.cam, self.hookY), self.hookSize / 2)
    def shootHook(self, mousepos):
        if self.hookX == None:
            self.hookX, self.hookY = self.x + self.width / 2, self.y + self.height / 2
            x_offset, y_offset = self.x + self.width / 2 + self.cam - mousepos[0], self.y + self.width / 2 - mousepos[1]
            a, b = self.getHookVels(x_offset, y_offset, self.hookSpeed)
            self.hookVelLeft, self.hookVelUp = -a, -b
        else:
            self.hooked = False
            self.hookReeling = True
    def getHookVels(self, x_offset, y_offset, speed):
        d = (x_offset ** 2 + y_offset ** 2) ** 0.5
        vx = speed * x_offset / d
        vy = speed * y_offset / d
        return vx, vy

    def wall_jump(self, wall):
        xVel = 10
        self.velUp = max(5, self.velUp + 15)
        self.jump = True
        if wall == 'l':
            self.velLeft -= xVel
        elif wall == 'r':
            self.velLeft += xVel

    def movement(self):
        self.updateBlockStatuses()
        if self.hooked:
            x_offset, y_offset = self.x + self.width / 2 - self.hookX, self.y + self.width / 2 - self.hookY
            a, b = self.getHookVels(x_offset, y_offset, self.hookPower)
            self.velUp += b * self.delta * self.offset
            self.velLeft += a * self.delta * self.offset

        if self.right:
            if self.character != 3:
                if self.grounded:
                    self.velLeft -= self.groundAcceleration * self.delta * self.offset
                else:
                    self.velLeft -= self.airAcceleration * self.delta * self.offset
            elif self.hooked:
                self.velLeft -= self.airAcceleration * self.delta * self.offset
            self.sprite = self.sprites[1]
        if self.left:
            if self.character != 3:
                if self.grounded:
                    self.velLeft += self.groundAcceleration * self.delta * self.offset
                else:
                    self.velLeft += self.airAcceleration * self.delta * self.offset

            elif self.hooked:
                self.velLeft += self.airAcceleration * self.delta * self.offset
            self.sprite = self.sprites[0]


        for i in range(self.speedCorrection):
            if self.velLeft < -self.maxSpeed:
                self.velLeft +=  self.delta * self.offset
            if self.velLeft > self.maxSpeed:
                self.velLeft -= self.delta * self.offset

        if self.grounded:
            if not self.right and not self.left:
                if self.velLeft < 0:
                    self.velLeft += self.groundFriction * self.delta * self.offset
                elif self.velLeft > 0:
                    self.velLeft -= self.groundFriction * self.delta * self.offset
                if -self.groundFriction < self.velLeft < self.groundFriction:
                    self.velLeft = 0
        else:
            if not self.right and not self.left:
                if self.velLeft < 0:
                    self.velLeft += self.airFriction * self.delta * self.offset
                elif self.velLeft > 0:
                    self.velLeft -= self.airFriction * self.delta * self.offset
                if -self.airFriction < self.velLeft < self.airFriction:
                    self.velLeft = 0

        if not self.gravity:
            if self.velUp < 0:
                self.velUp += self.airFriction * self.delta * self.offset
            elif self.velUp > 0:
                self.velUp -= self.airFriction * self.delta * self.offset

        if self.gravity:
            if self.jump:
                if self.velUp <= 0:
                    self.jump = False
            if not self.grounded:
                self.velUp -= self.g * self.delta * self.offset

            if self.velUp < self.maxFallSpeed:
                self.velUp = self.maxFallSpeed
            if self.velUp > self.maxSpeed and not self.jump:
                if self.hooked:
                    self.velUp = self.maxSpeed
                pass
        else:
            if self.up:
                self.velUp += self.airAcceleration * self.delta * self.offset
            if self.down:
                self.velUp -= self.airAcceleration * self.delta * self.offset

            if self.velUp < -self.maxSpeed:
                self.velUp = -self.maxSpeed
            if self.velUp > self.maxSpeed:
                self.velUp = self.maxSpeed


        self.pixelMove()
    def pixelMove(self):
        divisor = int(max(abs(self.velLeft), abs(self.velUp))) + 1
        for i in range(divisor):
            if not self.collisionFinder(False, 'p'):
                if self.maxSpeed == self.boostedMaxSpeed:
                    self.createParticle(self.width - 10, self.display.speedColor, self.x + self.width / 2, self.y + self.height / 2 + 4, 0, 0, 0, 10, 4.5)
                else:
                    self.createParticle(self.width - 10, self.currentTrailColor, self.x + self.width / 2, self.y + self.height / 2, 0, 0, 0, 10, 4.5)
                self.archiveCords = [self.x, self.y]
            self.x -= self.velLeft * self.delta * self.offset / divisor
            self.y -= self.velUp * self.delta * self.offset / divisor
            self.updateBlockStatuses()
            self.collisionFinder(True, 'p')
            if self.won:
                self.delete()
                break
        self.sprite_rect.x, self.sprite_rect.y = self.x, self.y

        try:
            if self.grounded and not self.bouncyMode:
                self.jumpsLeft = self.jumpAmount
        except:
            pass
    def delete(self):
        self.display.game.timerText.hidden = True
        if self.won:
            self.display.game.current_display = self.display.game.displays['win_screen']
        self.display.objects.remove(self)
        self.display.particles = []
        del self

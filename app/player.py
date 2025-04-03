import time as czas
from random import random

import pygame
from pygame import *
from app import particle
from mapMaker import tileSize, height
import random as ran


class Player:
    def __init__(self, display):
        self.display = display
        self.display.objects.append(self)


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
        self.wallAndCeilingBounce = 5
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
        self.hookSpeed = 25
        self.hookPower = 3
        self.hookVelUp = 0
        self.hookVelLeft = 0
        self.hookReeling = False


        self.width = self.display.tileSize
        self.height = self.width
        self.playerColor = (200, 30, 30)
        self.trailColor = (90, 20, 20)
        self.character = 2 # 0 is debugger, 1 is bouncer, 2 is runner, 3 is hooker, 4 is magneter

        if self.character == 0:
            self.bouncyMode = False
            self.gravity = False
            self.airAcceleration = 2
            self.groundAcceleration = 2
            self.maxSpeed = self.boostedMaxSpeed
            self.playerColor = (200, 200, 200)
            self.trailColor = (90, 90, 90)
        if self.character == 1:
            # bouncer bounces from every block, has 1 jump in the air after bouncing from a white floor
            self.bouncyMode = True
            self.gravity = True
            self.g = 0.6
            self.trailColor = (90, 20, 20)
            self.minBounce = 5
            self.wallAndCeilingBounce = 5
            self.floorBounce = 5
        if self.character == 2:
            # runner can run along the floor and jump twice, pretty normal stuff
            self.bouncyMode = False
            self.playerColor = (30, 200, 30)
            self.trailColor = (20, 90, 20)


        # hooker will have 1 small jump and a hook

        # magneter will get attracted to the mouse, no jump, no gravity

        self.x = self.display.spawnCords[0]
        self.y = self.display.spawnCords[1]
        self.velUp = 0
        self.velRight = 0
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
        self.velRight = 0
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

                if self.velRight < -self.minBounce * bounceMulti:
                    self.velRight *= -self.energyConservation * bounceMulti
                elif 0 > self.velRight:
                    self.velRight = self.minBounce * bounceMulti
                self.hugLeft = True
                return
            elif direction == 'right':
                self.x = self.archiveCords[0]

                if self.velRight > self.minBounce * bounceMulti:
                    self.velRight *= -self.energyConservation * bounceMulti
                elif 0 < self.velRight:
                    self.velRight = -self.minBounce * bounceMulti
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
                self.velRight = 0
                return
            elif direction == 'right':
                self.x = block[0] - self.width - 1
                self.velRight = 0
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
        self.particle = particle.Particle(self.display, size, color, x, y, velRight, velUp, g, lifetime, shrink)
        self.display.particles.append(self.particle)
    def render(self):
        if self.justStarted:
            self.justStarted = False
            self.restart(True)
            self.display.game.timerText.hidden = False
        self.cam = self.display.camera
        if self.x + self.width / 2 > self.display.game.width / 2:
            pygame.draw.rect(self.display.screen, self.playerColor,((self.display.game.width - self.width) / 2 - 1, self.y - 1, self.width + 2, self.height + 2))    # camera work
        else:
            pygame.draw.rect(self.display.screen, self.playerColor, (self.x - 1, self.y - 1, self.width + 2, self.height + 2))


        if self.display.game.countdown < 1:
            self.movement()

            self.hook_movement()


        if self.hookX != None:
            col = (100, 200, 100)
            if self.hooked:
                pass
            else:
                self.hookX += self.hookVelLeft
                self.hookY += self.hookVelUp
                col = self.playerColor
            if self.hookReeling:
                col = (200, 100, 100)
            pygame.draw.line(self.display.screen, col, (self.x + self.cam + self.width / 2, self.y + self.width / 2), (self.hookX + self.cam, self.hookY), 4)
            pygame.draw.circle(self.display.screen, self.playerColor, (self.hookX + self.cam, self.hookY), self.hookSize / 2)
            if not self.hookReeling:
                self.collisionFinder(True, 'h')

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
            if event.key == pygame.K_SPACE or event.key == K_UP:
                if self.display.game.countdown < 1:
                    if self.jumpsLeft > 0:
                        self.jump = True
                        self.jumpsLeft -= 1
                        self.velUp = self.jumpLength
                        if self.grounded:
                            self.y -= 1
                            if self.character == 2:
                                self.jumpsLeft += 1
                        if self.right and not self.left:
                            self.velRight += self.jumpSpeedBoost
                        elif self.left and not self.right:
                            self.velRight -= self.jumpSpeedBoost
                    else:
                        pass

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
                        if self.collision((self.x, self.y - 1, 1, self.height - 2), block):
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
                        if self.collision((self.x + self.width - 1, self.y - 1, 1, self.height - 2), block):
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
        if self.hookReeling:
            a, b = self.getHookVels(self.hookX - self.x - self.width / 2, self.hookY - self.y - self.width / 2, self.hookSpeed)
            self.hookVelLeft = -a
            self.hookVelUp = -b
            if self.collision((self.hookX, self.hookY, self.hookSize, self.hookSize), (self.x, self.y, self.width, self.height)):
                self.hookX, self.hookY = None, None
                self.hookReeling = False
                self.hookVelUp = 0
                self.hookVelLeft = 0
    def shootHook(self, mousepos):
        if self.hookX == None:
            self.hookX, self.hookY = self.x + self.width / 2, self.y + self.height / 2
            x_offset, y_offset = self.x + self.width / 2 + self.cam - mousepos[0], self.y + self.width / 2 - mousepos[1]
            a, b = self.getHookVels(x_offset, y_offset, self.hookSpeed)
            self.hookVelLeft, self.hookVelUp = -a, -b
        elif not self.hookReeling:
            self.hooked = False
            self.hookReeling = True
    def getHookVels(self, x_offset, y_offset, speed):
        d = (x_offset ** 2 + y_offset ** 2) ** 0.5
        vx = speed * x_offset / d
        vy = speed * y_offset / d
        return vx, vy



    def movement(self):
        self.updateBlockStatuses()
        if self.gravity:
            if self.jump:
                if self.velUp <= 0:
                    self.jump = False
            if not self.grounded:
                self.velUp -= self.g

            if self.velUp < self.maxFallSpeed:
                self.velUp = self.maxFallSpeed
            if self.velUp > self.maxSpeed and not self.jump:
                self.velUp = self.maxSpeed

        else:
            if self.up:
                self.velUp += self.airAcceleration
            if self.down:
                self.velUp -= self.airAcceleration

            if self.velUp < -self.maxSpeed:
                self.velUp = -self.maxSpeed
            if self.velUp > self.maxSpeed:
                self.velUp = self.maxSpeed

        if self.right:
            if self.grounded:
                self.velRight += self.groundAcceleration
            else:
                self.velRight += self.airAcceleration
        if self.left:
            if self.grounded:
                self.velRight -= self.groundAcceleration
            else:
                self.velRight -= self.airAcceleration

        if self.velRight < -self.maxSpeed:
            self.velRight += self.speedCorrection
        if self.velRight > self.maxSpeed:
            self.velRight -= self.speedCorrection

        if self.grounded:
            if not self.right and not self.left:
                if self.velRight < 0:
                    self.velRight += self.groundFriction
                elif self.velRight > 0:
                    self.velRight -= self.groundFriction
                if -self.groundFriction < self.velRight < self.groundFriction:
                    self.velRight = 0
        else:
            if not self.right and not self.left:
                if self.velRight < 0:
                    self.velRight += self.airFriction
                elif self.velRight > 0:
                    self.velRight -= self.airFriction
                if -self.airFriction < self.velRight < self.airFriction:
                    self.velRight = 0

        if not self.gravity:
            if self.velUp < 0:
                self.velUp += self.airFriction
            elif self.velUp > 0:
                self.velUp -= self.airFriction

        if self.hooked:
            x_offset, y_offset = self.x + self.width / 2 - self.hookX, self.y + self.width / 2 - self.hookY
            a, b = self.getHookVels(x_offset, y_offset, self.hookPower)
            self.velUp += b
            self.velRight -= a
        self.pixelMove()
    def pixelMove(self):
        divisor = abs(int(max(self.velRight, self.velUp))) + 1
        for i in range(divisor):
            if not self.collisionFinder(False, 'p'):
                if self.maxSpeed == self.boostedMaxSpeed:
                    self.createParticle(self.width, self.display.speedColor, self.x, self.y, 0, 0, 0, 10, 4.5)
                else:
                    self.createParticle(self.width, self.trailColor, self.x, self.y, 0, 0, 0, 10, 4.5)
                self.archiveCords = [self.x, self.y]
            self.x += self.velRight / divisor
            self.y -= self.velUp / divisor
            self.updateBlockStatuses()
            self.collisionFinder(True, 'p')
            if self.won:
                self.delete()
                break

        try:
            if self.grounded and not self.bouncyMode:
                self.jumpsLeft = self.jumpAmount
        except:
            pass
    def delete(self):
        self.display.game.timerText.hidden = True
        self.display.game.current_display = self.display.game.displays['win_screen']
        self.display.objects.remove(self)
        self.display.particles = []
        del self

import pygame
from pygame import *
from app import game


class Player:
    def __init__(self, display):
        self.display = display
        self.display.objects.append(self)
        self.x = 100
        self.y = 600
        self.velUp = 0
        self.velRight = 0
        self.width = 50
        self.height = 50
        self.playerColor = (200, 30, 30)
        self.g = 0.5
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.jump = False
        self.grounded = False
        self.maxSpeed = 8
        self.maxFallSpeed = -7
        self.jumpLength = 15
        self.airAcceleration = 0.4
        self.groundAcceleration = 1
        self.airFriction = 0.1
        self.groundFriction = 0.5
        self.archiveCords = [self.x, self.y]
        self.gravity = True
        self.founded = False


    def collision(self, list, block: list) -> bool:
        x, y, w, h = list[0],list[1],list[2],list[3]
        if x <= block[0] <= x + w or block[0] <= x <= block[0] + block[2]:
            if y <= block[1] <= y + h or block[1] <= y <= block[1] + block[3]:
                return True
        return False


    def nudge(self, direction: str, block: list):
        if direction == 'down':
            self.y = block[1] - self.height
            self.velUp = 0
            self.grounded = True
            return

        elif direction == 'up':
            self.y = block[1] + block[3]
            self.velUp = 0
            return
        elif direction == 'left':
            self.x = block[0] + block[2]
            self.velRight = 0
            return
        elif direction == 'right':
            self.x = block[0] - self.width
            self.velRight = 0
            return


    def corner(self, block: list):
        right, down = False, False
        a, b = abs(self.x - self.archiveCords[0]), abs(self.y - self.archiveCords[1])
        c = self.x + self.width - block[0]
        if block[0] + block[2] - self.x < c:
            c = block[0] + block[2] - self.x
            right = True
        d = self.y + self.height - block[1]
        if block[1] + block[3] - self.y < d:
            d = block[1] + block[3] - self.y
            down = True

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




    def correction(self, block: list):
        direction = None
        if self.archiveCords[0] <= block[0] <= self.archiveCords[0] + self.width or block[0] <= self.archiveCords[0] <= block[0] + block[2]:
            if self.y - self.archiveCords[1] < 0:
                direction = 'up'
            elif not self.grounded:
                direction = 'down'
        elif self.archiveCords[1] < block[1] < self.archiveCords[1] + self.width or block[1] < self.archiveCords[1] < block[1] + block[3]:
            if self.x - self.archiveCords[0] < 0:
                direction = 'left'
            else:
                direction = 'right'
        else:
            direction = 'else'
            self.nudge(self.corner(block), block)

        if not direction == 'else':
            self.nudge(direction, block)



    def collisions(self):
        for row in range(len(self.display.currentMap)):
            for column in range(len(self.display.currentMap[row])):
                if self.display.currentMap[row][column] == 1:
                    block = (column * self.display.tileSize, row * self.display.tileSize, self.display.tileSize, self.display.tileSize)
                    if self.collision((self.archiveCords[0], self.archiveCords[1], self.width, self.height),block):
                        print('collide')
                    if self.collision((self.x, self.y, self.width, self.height),block):
                        self.correction(block)
                        pygame.draw.rect(self.display.screen, (200, 0, 0), (block[0] + self.display.camera,block[1],block[2],block[3]))




    def render(self):
        if self.x + self.width / 2 > self.display.game.width / 2:
            pygame.draw.rect(self.display.screen, self.playerColor, ((self.display.game.width - self.width )/ 2, self.y, self.width, self.height))
        else:
            pygame.draw.rect(self.display.screen, self.playerColor, (self.x, self.y, self.width, self.height))

        t = True
        for row in range(len(self.display.currentMap)):
            for column in range(len(self.display.currentMap[row])):
                if self.display.currentMap[row][column] == 1:
                    block = (column * self.display.tileSize, row * self.display.tileSize, self.display.tileSize, self.display.tileSize)
                    if self.collision((self.x, self.y, self.width, self.height),block):
                        t = False

        if t:
            self.archiveCords = [self.x, self.y]
        self.movement()
        self.collisions()

        return self.x + self.width / 2 - self.display.game.width / 2


    def events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self.left = True
            if event.key == pygame.K_d:
                self.right = True
            if event.key == pygame.K_s:
                self.down = True
            if event.key == pygame.K_w:
                self.up = True
            if event.key == pygame.K_SPACE:
                if self.velUp < 0:
                    self.velUp = 0
                self.jump = self.jumpLength
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                self.left = False
            if event.key == pygame.K_d:
                self.right = False
            if event.key == pygame.K_s:
                self.down = False
            if event.key == pygame.K_w:
                self.up = False
            if event.key == pygame.K_SPACE:
                self.jump = 0
    def isFounded(self):
        for row in range(len(self.display.currentMap)):
            for column in range(len(self.display.currentMap[row])):
                if self.display.currentMap[row][column] == 1:
                    block = (column * self.display.tileSize, row * self.display.tileSize, self.display.tileSize, self.display.tileSize)
                    if self.collision((self.x + 1, self.y + self.height - 1, self.width - 2, 1),block):
                        return True
        print(1)
        return False

    def movement(self):
        self.grounded = self.isFounded()
        if self.gravity:
            if self.jump > 0:
                self.velUp += 3 * self.jump / (self.jumpLength) - 1.2
                self.jump -= 1
            elif not self.grounded:
                self.velUp -= self.g

            if self.velUp < self.maxFallSpeed:
                self.velUp = self.maxFallSpeed

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
            self.velRight = -self.maxSpeed
        if self.velRight > self.maxSpeed:
            self.velRight = self.maxSpeed

        if self.grounded:
            if self.velRight < 0:
                self.velRight += self.groundFriction
            elif self.velRight > 0:
                self.velRight -= self.groundFriction
            if -self.groundFriction < self.velRight < self.groundFriction:
                self.velRight = 0
        else:
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


        self.x += self.velRight
        self.y -= self.velUp
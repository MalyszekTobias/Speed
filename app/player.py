import pygame
from pygame import *
from app import game


class Player:
    def __init__(self, display):
        self.display = display
        self.display.objects.append(self)
        self.x = 100
        self.y = 10
        self.velUp = 0
        self.velRight = 0
        self.width = 50
        self.height = 50
        self.playerColor = (200, 30, 30)
        self.g = 0.5
        self.left = False
        self.right = False
        self.jump = False
        self.grounded = False
        self.maxSpeed = 8
        self.maxFallSpeed = -7
        self.jumpLength = 15
        self.airAcceleration = 0.4
        self.groundAcceleration = 1
        self.airFriction = 0.1
        self.groundFriction = 0.5



    def render(self):
        if self.x + self.width / 2 > self.display.game.width / 2:
            print()
            pygame.draw.rect(self.display.screen, self.playerColor, ((self.display.game.width - self.width )/ 2, self.y, self.width, self.height))
        else:
            pygame.draw.rect(self.display.screen, self.playerColor, (self.x, self.y, self.width, self.height))

        self.movement()
        return self.x + self.width / 2 - self.display.game.width / 2


    def events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self.left = True
            if event.key == pygame.K_d:
                self.right = True
            if event.key == pygame.K_SPACE:
                if self.velUp < 0:
                    self.velUp = 0
                self.jump = self.jumpLength
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                self.left = False
            if event.key == pygame.K_d:
                self.right = False
            if event.key == pygame.K_SPACE:
                self.jump = 0

    def movement(self):
        if self.jump > 0:
            self.velUp += 3 * self.jump / (self.jumpLength) - 1.2
            self.jump -= 1
        else:
            self.velUp -= self.g
        if self.velUp < self.maxFallSpeed:
            self.velUp = self.maxFallSpeed

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
        else:
            if self.velRight < 0:
                self.velRight += self.airFriction
            elif self.velRight > 0:
                self.velRight -= self.airFriction


        self.x += self.velRight
        self.y -= self.velUp
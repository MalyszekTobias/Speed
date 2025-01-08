import pygame.draw


class Particle:
    def __init__(self, display, size, color, x, y, velRight, velUp, g, lifetime):
        self.display = display
        self.size = size
        self.color = color
        self.x = x
        self.y = y
        self.velRight = velRight
        self.velUp = velUp
        self.g = g
        self.lifetime = lifetime


    def render(self):
        self.move()
        pygame.draw.rect(self.display.screen, self.color, (self.x + self.display.camera, self.y, self.size, self.size))
        self.lifetime -= 1
        if self.lifetime < 1:
            self.display.particles.remove(self)
            del self


    def move(self):
        self.velUp -= self.g
        self.x += self.velRight
        self.y -= self.velUp
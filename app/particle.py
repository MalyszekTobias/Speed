import pygame.draw


class Particle:
    def __init__(self, display, size, color, x, y, velRight, velUp, g, lifetime, shrink):
        self.display = display
        self.size = size
        self.color = color
        self.x = x
        self.y = y
        self.velRight = velRight
        self.velUp = velUp
        self.g = g
        self.lifetime = lifetime
        self.shrink = shrink


    def render(self):
        self.move()
        if self.size > 5:
            pygame.draw.circle(self.display.screen, self.color, (self.x + self.display.camera, self.y), self.size)
        self.lifetime -= 1
        self.size -= self.shrink / 2
        self.x += self.shrink / 2
        self.y += self.shrink / 2
        if self.lifetime < 1:
            self.display.particles.remove(self)
            del self


    def move(self):
        self.velUp -= self.g
        self.x += self.velRight
        self.y -= self.velUp
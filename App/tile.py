import pygame


class Tile:
    def __init__(self, display):
        self.display = display
        self.display.objects.append(self)
        self.x = 100
        self.y = 10
        self.width = 50
        self.height = 50
        self.tileColor = (200, 200, 200)

    def tick(self):
        pygame.draw.rect(self.display.screen, self.tileColor, (self.x, self.y, self.width, self.height))

    def events(self, event):
        pass
import pygame
import app
class Slider:
    def __init__(self, display, x, y, width, height, icon=None, value=50):
        self.display, self.x, self.y, self.width, self.height, self.icon , self.value = display, x, y, width, height, icon, value
        display.objects.append(self)
        self.icon = pygame.transform.scale(icon, (height, height))
        self.icon_rect = pygame.Rect(x - height - 30, y, height, height)
        self.notch_radius = 20

    def render(self):
        self.display.screen.blit(self.icon, self.icon_rect)
        pygame.draw.line(self.display.screen, 'white', (self.x, self.y+self.height//2), (self.x + self.width, self.y+self.height//2), 8)
        pygame.draw.circle(self.display.screen, 'white', (self.x + (self.value/100 * self.width), self.y+self.height//2), self.notch_radius)

    def events(self, event):
        if event == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.cursor_collide():
                    print('cursor')

    def cursor_collide(self):
        return True
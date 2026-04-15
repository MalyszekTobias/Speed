import pygame
import app
class Slider:
    def __init__(self, display, x, y, width, height, icon=None, value=50):
        self.display, self.x, self.y, self.width, self.height, self.icon , self.value = display, x, y, width, height, icon, value
        display.objects.append(self)
        self.icon = pygame.transform.scale(icon, (height, height))
        self.icon_rect = pygame.Rect(x - height - 30, y, height, height)
        self.notch_x = (value*width) // 100
        print(self.notch_x)
        self.notch_size = 50
        self.grabbed = None
    def render(self):
        if self.grabbed != None:
            self.notch_x = pygame.mouse.get_pos()[0] - self.x + self.grabbed + self.notch_size
        if self.notch_x <0:
            self.notch_x = 0
        if self.notch_x > self.width:
            self.notch_x = self.width
        self.display.screen.blit(self.icon, self.icon_rect)
        pygame.draw.line(self.display.screen, 'white', (self.x, self.y+self.height//2), (self.x + self.width, self.y+self.height//2), 8)
        pygame.draw.rect(self.display.screen, 'red', (self.x + self.notch_x - self.notch_size//2, self.y+self.height//2 - self.notch_size//2, self.notch_size, self.notch_size))

    def events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.grabbed = self.cursor_collide()
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.grabbed = None

    def cursor_collide(self):
        x,y = self.x + self.notch_x - self.notch_size//2, self.y+self.height//2 - self.notch_size//2
        w = self.notch_size
        a,b = pygame.mouse.get_pos()
        print(x, a, x+w)
        print(y, b, y+w)
        if x < a < x+w:
            if y < b < y+w:
                print('grab')
                return x - (a + self.notch_size//2)
        return None

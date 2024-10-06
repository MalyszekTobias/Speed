import pygame
from Speed import maps
from app import custom_text, custom_images, button, player

class basic_display():
    def __init__(self, game):
        self.game = game
        self.screen = self.game.screen

        self.objects = []

    def render(self):
        for obj in self.objects:
            obj.render()

    def events(self, event):
        for obj in self.objects:
            obj.events(event)

class game_display(basic_display):
    def __init__(self, game):
        basic_display.__init__(self, game)
        self.currentMap = maps.tuto
        self.tileSize = int(self.game.height / len(self.currentMap))
        print(self.game.width)
        print(self.tileSize)


        print(self.objects)
        self.player = player.Player(self)

    def mainloop(self):
        pass

    def render(self):
        for obj in self.objects:
            obj.render()

    def events(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.game.current_display = self.game.displays['pause_display']
        else:
            for obj in self.objects:
                obj.events(event)

class pause_display(basic_display):
    def __init__(self, game):
        basic_display.__init__(self, game)


        custom_text.Custom_text(self, self.game.width / 2, self.game.height / 3, None, 100, 'Paused', text_color='White')
        button.Button(self, 'game_display', self.game.width / 2 - 150, self.game.height * 0.45 + 100, 300, 75, (0, 0, 0), outline_color='white', text='Resume', text_color='white')

    def events(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.game.current_display = self.game.displays['game_display']
        else:
            for obj in self.objects:
                obj.events(event)

class start_screen(basic_display):
    def __init__(self, game):
        basic_display.__init__(self, game)
        custom_text.Custom_text(self, self.game.width/2, self.game.height/3, None, 100, 'PyGame Game', text_color='Green')
        button.Button(self, 'settings', self.game.width/2 - 100, self.game.height * 0.75, 200, 75, (0, 0, 0), outline_color='white', text='Settings', text_color='white')
        button.Button(self, 'game_display', self.game.width / 2 - 100, self.game.height * 0.75 - 100, 200, 75, (0, 0, 0), outline_color='white', text='Start', text_color='white')
class settings_screen(basic_display):
    def __init__(self, game):
        basic_display.__init__(self, game)
        button.Button(self, 'start_screen', 25, self.game.height - 100, 200, 75, (0, 0, 0), outline_color='white', text=' Save & exit', text_color='white')



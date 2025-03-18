import time
import pygame
import maps
from app import custom_text, custom_images, button, player
from mapMaker import camera, tileSize


class basic_display():
    def __init__(self, game):
        self.game = game
        self.screen = self.game.screen

        self.objects = []
        self.particles = []

    def render(self):
        for obj in self.particles:
            obj.render()
        for obj in self.objects:
            obj.render()

    def events(self, event):
        for obj in self.objects:
            obj.events(event)


class game_display(basic_display):
    def __init__(self, game):
        basic_display.__init__(self, game)
        self.camera = 0
        self.bgColor = (0, 0, 0)
        self.tileColor = (200, 200, 200)
        self.speedColor = (50, 230, 50)
        self.jumpColor = (50, 50, 250)
        self.bounceColor = (250, 50, 50)
        self.winColor = (182, 196, 77)
        self.colors = (self.bgColor, self.tileColor, self.speedColor, self.jumpColor, self.bounceColor, self.winColor)
        self.currentMap = maps.trampoline
        self.tileSize = int(self.game.height / len(self.currentMap))
        for i in range(len(self.currentMap)):
            for j in range(len(self.currentMap[i])):
                if self.currentMap[i][j] == 6:
                    self.spawnCords = [j * tileSize, i * tileSize]

        pygame.draw.rect(self.screen, self.bgColor, (0, 0, self.game.width, self.game.height))


    def mainloop(self):
        pass

    def render(self):
        m, n = len(self.currentMap), len(self.currentMap[0])
        for i in range(m):
            for j in range(n):
                num = self.currentMap[i][j]
                if not num in (0, 6, 7, 8, 9):
                    pygame.draw.rect(self.screen, self.colors[num],
                                     (j * self.tileSize + self.camera, i * self.tileSize, self.tileSize, self.tileSize))

        for obj in self.particles:
            obj.render()
        for obj in self.objects:
            c = obj.render()
            if c > 0:
                self.camera = -c
            else:
                self.camera = 0

    def events(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.game.current_display = self.game.displays['pause_display']
            self.game.pausedStart = time.time_ns() // 1000000
            self.game.countdownText.hidden = True
        else:
            for obj in self.objects:
                obj.events(event)


class pause_display(basic_display):
    def __init__(self, game):
        basic_display.__init__(self, game)

        custom_text.Custom_text(self, self.game.width / 2, self.game.height / 3, None, 100, 'Paused',
                                text_color='White')
        button.Button(self, 'game_display', self.game.width / 2 - 150, self.game.height * 0.45 + 100, 300, 75,
                      (0, 0, 0), outline_color='white', text='Resume', text_color='white')

    def events(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.game.current_display = self.game.displays['game_display']
            self.game.pauseSum += self.game.currPauseTime
            self.game.currPauseTime = 0
            self.game.pausedStart = None
            if self.game.countdown > 0:
                self.game.pauseSum = 0
                self.game.countdownText.hidden = False

        else:
            for obj in self.objects:
                obj.events(event)


class start_screen(basic_display):
    def __init__(self, game):
        basic_display.__init__(self, game)
        custom_text.Custom_text(self, self.game.width / 2, self.game.height / 3, None, 100, 'Speed', text_color='Green')
        button.Button(self, 'settings', self.game.width / 2 - 100, self.game.height * 0.75, 200, 75, (0, 0, 0),
                      outline_color='white', text='Settings', text_color='white')
        button.Button(self, 'game_display', self.game.width / 2 - 100, self.game.height * 0.75 - 100, 200, 75,
                      (0, 0, 0), outline_color='white', text='Start', text_color='white')


class settings_screen(basic_display):
    def __init__(self, game):
        basic_display.__init__(self, game)
        button.Button(self, 'start_screen', 25, self.game.height - 100, 200, 75, (0, 0, 0), outline_color='white',
                      text=' Save & exit', text_color='white')


class win_screen(basic_display):
    def __init__(self, game):
        basic_display.__init__(self, game)
        button.Button(self, 'restart', 25, self.game.height - 100, 200, 75, (0, 0, 0), outline_color='white',
                      text=' restart', text_color='white')
        button.Button(self, 'start_screen_after_win', self.game.width - 175, self.game.height - 100, 200, 75, (0, 0, 0),
                      outline_color='white', text='main menu', text_color='white')

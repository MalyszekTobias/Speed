import time

import pygame
import maps
from app import custom_text, custom_images, button, player
from mapMaker import camera, tileSize, screen


class basic_display():
    def __init__(self, game):
        self.game = game
        self.offset = 60
        self.screen = self.game.screen

        self.objects = []
        self.particles = []
        self.width, self.height = game.width, game.height
        self.character = 3

    def render(self):
        self.delta = self.game.delta_time
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
        self.currentMap = None

        pygame.draw.rect(self.screen, self.bgColor, (0, 0, self.game.width, self.game.height))


    def mainloop(self):
        pass

    def get_map(self):
        self.currentMap = maps.maps[self.game.currentMap]
        self.tileSize = int(self.game.height / len(self.currentMap))
        for i in range(len(self.currentMap)):
            for j in range(len(self.currentMap[i])):
                if self.currentMap[i][j] == 6:
                    self.spawnCords = [j * tileSize, i * tileSize]
    def render(self):
        self.delta = self.game.delta_time
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

        custom_text.Custom_text(self, self.game.width / 2, self.game.height / 3, None, self.game.header_text_size, 'Paused',
                                text_color='White')
        button.Button(self, 'game_display', self.game.width / 2 - 150, self.game.height * 0.45 + 100, 130, 70,
                      (0, 0, 0), outline_color='white', text='Resume', text_color='white')
        button.Button(self, 'level_select_screen', self.game.width / 2 + 150, self.game.height * 0.45 + 100, 130, 70,
                      (0, 0, 0), outline_color='white', text='Quit', text_color='white')
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
        custom_text.Custom_text(self, self.game.width / 2, self.game.height / 3, None, self.game.header_text_size, 'Speed', text_color='Green')
        button.Button(self, 'settings', self.game.width / 2 - 100, self.game.height * 0.75, 200, 75, (0, 0, 0),
                      outline_color='white', text='Settings', text_color='white')
        button.Button(self, 'level_select_screen', self.game.width / 2 - 100, self.game.height * 0.75 - 100, 200, 75,
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
        button.Button(self, 'start_screen_after_win', self.game.width - 200, self.game.height - 100, 200, 75, (0, 0, 0),
                      outline_color='white', text='main menu', text_color='white')

class level_select_screen(basic_display):
    def __init__(self, game):
        basic_display.__init__(self, game)
        button.Button(self, 'game_display', self.game.width / 2 + 50, self.game.height / 2 + 100, 300, 100, (0, 0, 0), outline_color='white',
                      text='Play', text_color='white')
        self.mapNames, self.maps = self.getMaps()
        self.game.currentMap = 0
        self.character_cell_height = 200
        self.character_select_border = 5
        self.character_colors = [[5, 219, 5], [250,50,50], [249, 249, 20], [65, 242, 255]]
        self.character_sprites = [pygame.image.load("Assets/Sprites/green_right.png"), pygame.image.load("Assets/Sprites/red_right.png"), pygame.image.load("Assets/Sprites/yellow_right.png"), pygame.image.load("Assets/Sprites/teal_right.png")]
        self.sprite_rects = []
        img_size = self.character_cell_height - 2 * self.character_select_border
        for s in range(len(self.character_sprites)):
            self.character_sprites[s] = pygame.transform.scale(self.character_sprites[s], (img_size, img_size))
            sprite_rect = self.character_sprites[s].get_rect()
            sprite_rect.x,sprite_rect.y = self.character_select_border, self.character_select_border + s*self.character_cell_height
            self.sprite_rects.append(sprite_rect)
        # self.objects = []
        self.name_text = custom_text.Custom_text(self, self.game.width / 2, self.game.height / 2, self.game.font, self.game.debug_text_size, self.mapNames[self.game.currentMap], text_color='white')

    def change_map(self, amount: int):
        if 0 <= self.game.currentMap + amount < len(self.mapNames):
            self.game.currentMap += amount
            self.name_text.update_text(self.mapNames[self.game.currentMap])
        else:
            print('no more maps')

    def change_character(self, amount):
        if 0 <= self.game.character + amount <= 3:
            self.game.character += amount
            print(self.game.character)
            # self.game.player.character = self.character
        else:
            print('no more characters')

    def events(self, event):
        for obj in self.objects:
            obj.events(event)
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_a, pygame.K_LEFT):
                self.change_map(-1)
            elif event.key in (pygame.K_d, pygame.K_RIGHT):
                self.change_map(1)
            elif event.key in (pygame.K_w, pygame.K_UP):
                self.change_character(-1)
            elif event.key in (pygame.K_s, pygame.K_DOWN):
                self.change_character(1)

    def getMaps(self):
        n, m = [], []
        for i in range(len(maps.names)):
            n.append(maps.names[i])
            m.append(maps.maps[i])
        return n, m

    def render(self):
        self.delta = self.game.delta_time
        for obj in self.particles:
            obj.render()
        for obj in self.objects:
            obj.render()
        a = self.game.character
        x = 0
        y = a * self.character_cell_height
        pygame.draw.rect(self.screen, self.character_colors[a],
                         (x, y, self.character_cell_height, self.character_cell_height))
        for i in range(4):
            screen.blit(self.character_sprites[i], self.sprite_rects[i])
import time

import pygame
import maps
from app import custom_text, custom_images, button, player, particle
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
        self.pauseButton = button.Button(self, 'pause', 15, 25, 75, 75, (0, 0, 0), outline_color='white',
                      text='II', text_color='white')
        self.restartButton = button.Button(self, 'restart', 105, 25, 75, 75, (0, 0, 0), outline_color='white',
                      text='r', text_color='white')
        self.pauseIcon = pygame.image.load('Assets/Icons/pause_icon.png')
        self.pauseIcon_rect = self.pauseIcon.get_rect()
        self.pauseIcon_rect.x, self.pauseIcon_rect.y = 15, 25
        self.restartIcon = pygame.image.load('Assets/Icons/restart_icon.png')
        self.restartIcon_rect = self.restartIcon.get_rect()
        self.restartIcon_rect.x, self.restartIcon_rect.y = 105, 25
        self.pauseFade = pygame.image.load('Assets/Icons/pause_fade.png')
        self.pauseFade_rect = self.pauseFade.get_rect()
        self.pauseFade_rect.x, self.pauseFade_rect.y = 15, 25
        self.restartFade = pygame.image.load('Assets/Icons/restart_fade.png')
        self.restartFade_rect = self.restartFade.get_rect()
        self.restartFade_rect.x, self.restartFade_rect.y = 105, 25

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
            obj.render()
        c = self.game.player.get_cam()
        if c > 0:
            self.camera = -c
        else:
            self.camera = 0
        self.screen.blit(self.pauseIcon, self.pauseIcon_rect)
        self.screen.blit(self.restartIcon, self.restartIcon_rect)
        if self.pauseButton.rect.collidepoint(pygame.mouse.get_pos()):
            self.screen.blit(self.pauseFade, self.pauseFade_rect)
        if self.restartButton.rect.collidepoint(pygame.mouse.get_pos()):
            self.screen.blit(self.restartFade, self.restartFade_rect)


    def events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.pauseButton.click()
            if event.key == pygame.K_r:
                self.restartButton.click()

        for obj in self.objects:
            obj.events(event)


class pause_display(basic_display):
    def __init__(self, game):
        basic_display.__init__(self, game)

        custom_text.Custom_text(self, self.game.width / 2, self.game.height / 3, None, self.game.header_text_size, 'Paused',
                                text_color='White')
        self.resumeButton = button.Button(self, 'resume', self.game.width / 2 - 150, self.game.height * 0.45 + 100, 130, 70,
                      (0, 0, 0), outline_color='white', text='Resume', text_color='white')
        self.quitButton = button.Button(self, 'level_select_screen', self.game.width / 2 + 150, self.game.height * 0.45 + 100, 130, 70,
                      (0, 0, 0), outline_color='white', text='Quit', text_color='white')
    def events(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.resumeButton.click()


        else:
            for obj in self.objects:
                obj.events(event)


class start_screen(basic_display):
    def __init__(self, game):
        basic_display.__init__(self, game)
        custom_text.Custom_text(self, self.game.width / 2, self.game.height / 3, None, self.game.header_text_size, 'Speed', text_color='Green')
        self.settingsButton = button.Button(self, 'settings', self.game.width / 2 - 100, self.game.height * 0.75, 200, 75, (0, 0, 0),
                      outline_color='white', text='Settings', text_color='white')
        self.lvl_select_Button = button.Button(self, 'level_select_screen', self.game.width / 2 - 100, self.game.height * 0.75 - 100, 200, 75,
                      (0, 0, 0), outline_color='white', text='Start', text_color='white')
        self.quitButton = button.Button(self, 'quit_game', self.game.width / 2 - 100, self.game.height * 0.75 +100, 200, 75,
                      (0, 0, 0), outline_color='white', text='Quit', text_color='white')
        self.map_editor_from_start_Button = button.Button(self, 'map_editor', self.game.width - 400, self.game.height * 0.75 +100, 200, 75,
                      (0, 0, 0), outline_color='white', text='Map editor', text_color='white')
    def events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.quitButton.click()
            elif event.key in (pygame.K_SPACE, 13):
                self.lvl_select_Button.click()
        for obj in self.objects:
            obj.events(event)


class settings_screen(basic_display):
    def __init__(self, game):
        basic_display.__init__(self, game)
        self.quitButton = button.Button(self, 'start_screen', 25, self.game.height - 100, 200, 75, (0, 0, 0), outline_color='white',
                      text=' Save & exit', text_color='white')
    def events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.quitButton.click()
        for obj in self.objects:
            obj.events(event)


class win_screen(basic_display):
    def __init__(self, game):
        basic_display.__init__(self, game)
        self.restartButton = button.Button(self, 'play', 25, self.game.height - 100, 200, 75, (0, 0, 0), outline_color='white',
                      text='restart', text_color='white')
        self.menuButton = button.Button(self, 'start_screen_after_win', self.game.width - 200, self.game.height - 100, 200, 75, (0, 0, 0),
                      outline_color='white', text='main menu', text_color='white')

    def events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.restartButton.click()

        for obj in self.objects:
            obj.events(event)

class level_select_screen(basic_display):
    def __init__(self, game):
        basic_display.__init__(self, game)
        self.character_cell_height = 200
        self.character_select_border = 5
        self.buttonWidth = 250
        img_size = self.character_cell_height - 2 * self.character_select_border
        self.playButton = button.Button(self, 'play', (self.game.width - self.character_cell_height) / 2 + 300 - self.buttonWidth/2 + self.character_cell_height, self.game.height / 2 + 100, self.buttonWidth, 90, (0, 0, 0), outline_color='white',
                      text='Play', text_color='white')
        self.menuButton = button.Button(self, 'start_screen', (self.game.width - self.character_cell_height) / 2 - 300 - self.buttonWidth/2 + self.character_cell_height, self.game.height / 2 + 100, self.buttonWidth, 90, (0, 0, 0), outline_color='white',
                      text='Exit', text_color='white')
        self.ch0Button = button.Button(self, 'change_character', 0, 0, 10 + img_size, 10 + img_size, (32,10,10), text='0', text_color='white', outline_width=0)
        self.ch1Button = button.Button(self, 'change_character', 0, self.character_cell_height, 10 + img_size, 10 + img_size, (32,10,10), text='1', text_color='white', outline_width=0)
        self.ch2Button = button.Button(self, 'change_character', 0, self.character_cell_height*2, 10 + img_size, 10 + img_size, (32,10,10), text='2', text_color='white', outline_width=0)
        self.ch3Button = button.Button(self, 'change_character', 0, self.character_cell_height*3, 10 + img_size, 10 + img_size, (32,10,10), text='3', text_color='white', outline_width=0)
        self.mapNames, self.maps = self.getMaps()
        self.game.currentMap = 0

        self.character_colors = [[5, 219, 5], [250,50,50], [249, 249, 20], [65, 242, 255]]
        self.character_sprites = [pygame.image.load("Assets/Sprites/green_right.png"), pygame.image.load("Assets/Sprites/red_right.png"), pygame.image.load("Assets/Sprites/yellow_right.png"), pygame.image.load("Assets/Sprites/teal_right.png")]
        self.sprite_rects = []

        for s in range(len(self.character_sprites)):
            self.character_sprites[s] = pygame.transform.scale(self.character_sprites[s], (img_size, img_size))
            sprite_rect = self.character_sprites[s].get_rect()
            sprite_rect.x,sprite_rect.y = self.character_select_border, self.character_select_border + s*self.character_cell_height
            self.sprite_rects.append(sprite_rect)
        # self.objects = []
        self.name_text = custom_text.Custom_text(self, (self.game.width - self.character_cell_height) / 2 + self.character_cell_height, self.game.height / 2, self.game.font, self.game.debug_text_size, self.mapNames[self.game.currentMap], text_color='white')

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
            elif event.key in (pygame.K_SPACE, 13):
                self.playButton.click()
            elif event.key == pygame.K_ESCAPE:
                self.menuButton.click()

    def getMaps(self):
        n, m = [], []
        for i in range(len(maps.names)):
            n.append(maps.names[i])
            m.append(maps.maps[i])
        return n, m

    def render(self):
        self.delta = self.game.delta_time
        screen.fill((0, 40, 0))
        pygame.draw.rect(self.screen, (32, 10, 10), (0, 0, self.character_cell_height, self.height))
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

class map_editor_list(basic_display):
    def __init__(self, game):
        basic_display.__init__(self, game)
        self.game = game
        self.menuButton = button.Button(self, 'start_screen', 25,25, 75,75, (0, 0, 0), outline_color='white', text='Exit', text_color='white')
        self.map_height = 150
        self.map_width = 1000
        self.mapLog_x = self.width/2 - self.map_width/2
        self.visible_maps = 5
        self.visible_space = self.visible_maps*(self.map_height+15)
        self.mapLog_start_y = (self.height - self.visible_space) / 2
        self.current_top_map = 0
        self.current_selected_map = None
        self.scroll_dist = 0
        self.scroll_due = 0
        self.scroll_speed = 20
        self.scroll_curtain_y = self.mapLog_start_y + self.visible_space
        self.mapNames, self.maps = self.getMaps()
        self.map_buttons = []
        self.refresh_buttons()
    def getMaps(self):
        n, m = [], []
        for i in range(len(maps.names)):
            n.append(maps.names[i])
            m.append(maps.maps[i])
        return n, m

    def render(self):
        for obj in self.objects:
            obj.render()
        if self.scroll_due < 0:
            if self.scroll_due < -self.scroll_speed:
                self.scroll_due += self.scroll_speed
                self.scroll_dist -= self.scroll_speed
            else:
                self.scroll_dist += self.scroll_due
                self.scroll_due = 0
            if self.scroll_dist < -len(self.maps)*(self.map_height + 15) + self.visible_space:
                self.scroll_dist = -len(self.maps)*(self.map_height + 15) + self.visible_space
                self.scroll_due = 0
            self.refresh_buttons()
        elif self.scroll_due > 0:
            if self.scroll_due > self.scroll_speed:
                self.scroll_due -= self.scroll_speed
                self.scroll_dist += self.scroll_speed
            else:
                self.scroll_dist += self.scroll_due
                self.scroll_due = 0
            if self.scroll_dist > 0:
                self.scroll_dist = 0
                self.scroll_due = 0
            self.refresh_buttons()
        pygame.draw.rect(self.screen, 'black', (0, self.scroll_curtain_y, self.width, 1000))
        pygame.draw.rect(self.screen, 'black', (0, 0, self.width, self.mapLog_start_y))

    def refresh_buttons(self):
        if self.map_buttons != []:
            for b in self.map_buttons:
                b.delete()
        self.map_buttons = []
        for i in range(len(self.maps)):
            oc = 'white'
            if i == self.current_selected_map:
                oc = 'yellow'
            mb = button.Button(self, 'select_map', self.mapLog_x, self.scroll_dist + self.mapLog_start_y + i*(self.map_height+15), self.map_width,self.map_height, (0, 0, 0), outline_color=oc, text=self.mapNames[i], text_color='white')
            self.map_buttons.append(mb)

    def scroll(self, dir):
        if self.current_top_map <= 0 and dir == 1:
            return
        if self.current_top_map >= len(self.maps) - self.visible_maps and dir == -1:
            return
        self.scroll_due += dir*(self.map_height+15)
        self.current_top_map -= dir
        self.refresh_buttons()
    def events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_s, pygame.K_DOWN):
                self.scroll(-1)
            if event.key in (pygame.K_w, pygame.K_UP):
                self.scroll(1)
        if event.type == pygame.MOUSEWHEEL:
            self.scroll(event.y)
        for obj in self.objects:
            obj.events(event)

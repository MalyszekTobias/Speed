import os.path
import time
from itertools import count

import pygame

import maps
from app import custom_text, custom_images, button, player, particle, slider


class basic_display():
    def __init__(self, game):
        self.game = game
        self.offset = 60
        self.screen = self.game.screen

        self.objects = []
        self.particles = []
        self.width, self.height = game.width, game.height
        self.character = 3
        self.midx, self.midy = self.width/2, self.height*2/3


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
        self.spawnCords = [50,50]
        self.colors = (self.bgColor, self.tileColor, self.speedColor, self.jumpColor, self.bounceColor, self.winColor)
        self.currentMap = None
        self.pauseButton = button.Button(self, 'pause', 15, 25, 75, 75, (0, 0, 0), outline_color='white',
                      icon=[pygame.image.load('Assets/Icons/pause_icon.png'),pygame.image.load('Assets/Icons/pause_hover.png')])
        self.restartButton = button.Button(self, 'restart', 105, 25, 75, 75, (0, 0, 0), outline_color='white',
                      icon=[pygame.image.load('Assets/Icons/restart_icon.png'), pygame.image.load('Assets/Icons/restart_hover.png')])


    def mainloop(self):
        pass

    def get_map(self):
        self.currentMap = maps.maps[self.game.currentMap]
        self.tileSize = int(self.height / len(self.currentMap))
        for i in range(len(self.currentMap)):
            for j in range(len(self.currentMap[i])):
                if self.currentMap[i][j] == 6:
                    self.spawnCords = [j * self.tileSize, i * self.tileSize]
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


    def events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.pauseButton.click()
            if event.key == pygame.K_r:
                self.restartButton.click()
                print('______________________________________')

        for obj in self.objects:
            obj.events(event)


class pause_display(basic_display):
    def __init__(self, game):
        basic_display.__init__(self, game)

        custom_text.Custom_text(self, self.width / 2, self.height / 3, None, self.game.header_text_size, 'Paused',
                                text_color='White')
        self.resumeButton = button.Button(self, 'resume', self.midx - 170, self.midy , 120, 120,
                      (0, 0, 0), icon=[pygame.image.load('Assets/Icons/play.png'),pygame.image.load('Assets/Icons/play_hover.png')])
        self.quitButton = button.Button(self, 'level_select_screen', self.midx + 50, self.midy, 120, 120,
                       text='Quit', icon=[pygame.image.load('Assets/Icons/home.png'), pygame.image.load('Assets/Icons/home_hover.png')])
    def events(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.resumeButton.click()


        else:
            for obj in self.objects:
                obj.events(event)


class start_screen(basic_display):
    def __init__(self, game):
        self.count = 0
        basic_display.__init__(self, game)
        self.title = custom_text.Custom_text(self, -50, self.midy - 300, None, self.game.header_text_size, 'Speed', text_color='Green')
        self.settingsButton = button.Button(self, 'settings', self.midx -170, self.midy + 20, 150, 150, icon=[pygame.image.load('Assets/Icons/settings.png'), pygame.image.load('Assets/Icons/settings_hover.png')])
        self.lvl_select_Button = button.Button(self, 'level_select_screen', self.midx - 170, self.midy - 170, 150, 150, icon=[pygame.image.load('Assets/Icons/play.png'), pygame.image.load('Assets/Icons/play_hover.png')])
        self.quitButton = button.Button(self, 'quit_game',self.midx +20, self.midy + 20, 150, 150, icon=[pygame.image.load('Assets/Icons/Exit.png'), pygame.image.load('Assets/Icons/Exit_hover.png')])
        self.map_editor_from_start_Button = button.Button(self, 'map_editor_list', self.midx + 20, self.midy - 170, 150, 150, icon=[pygame.image.load('Assets/Icons/edit.png'), pygame.image.load('Assets/Icons/edit_hover.png')])
    def events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.quitButton.click()
            elif event.key in (pygame.K_SPACE, 13):
                self.lvl_select_Button.click()
        for obj in self.objects:
            obj.events(event)

    def render(self):
        self.count += 0.0057
        if self.title.x >= self.midx:
            acc = 0
        elif self.title.x >= self.midx - 20:
            acc = 1
        else:
            acc = 1/self.count
        self.title.x += acc
        self.title.update_pos()

        for obj in self.objects:
            obj.render()


class settings_screen(basic_display):
    def __init__(self, game):
        basic_display.__init__(self, game)
        self.quitButton = button.Button(self, 'start_screen', self.midx - 75, self.height - 200, 150, 150, icon=[pygame.image.load('Assets/Icons/home.png'),pygame.image.load('Assets/Icons/home_hover.png')])
        self.margin = 500
        self.soundbar_height = 100
        self.sounds_bar_pos = [self.margin, 300]
        self.music_bar_pos = [self.margin, 300 + self.soundbar_height]
        self.sounds_bar = slider.Slider(self, self.sounds_bar_pos[0], self.sounds_bar_pos[1], self.width-2*self.margin - self.soundbar_height, self.soundbar_height, pygame.image.load('Assets/Icons/sound.png'))

    def events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.quitButton.click()
        for obj in self.objects:
            obj.events(event)


class win_screen(basic_display):
    def __init__(self, game):
        basic_display.__init__(self, game)
        self.restartButton = button.Button(self, 'play', self.width/2 - 130, self.height - 200, 110, 110,
                      icon=[pygame.image.load('Assets/Icons/restart_icon.png'), pygame.image.load('Assets/Icons/restart_hover.png')])
        self.menuButton = button.Button(self, 'start_screen_after_win', self.width/2 + 20, self.height - 200, 110, 110,
                      icon=[pygame.image.load('Assets/Icons/home.png'),pygame.image.load('Assets/Icons/home_hover.png')])
        self.finish_time = '0'
        self.congrats_text = custom_text.Custom_text(self, self.midx, self.midy - 400, None, 80, 'Congratulations', center=True, text_color='white')
        self.yourTime_text = custom_text.Custom_text(self, self.midx - 140, self.midy - 150, None, 80, 'Your time:', center=True, text_color='white')
        self.actual_time_text = custom_text.Custom_text(self, self.midx + 50, self.midy - 190, "Assets/digital-7.ttf", 80, self.finish_time, center=False, text_color='white')
        self.objects.append(self.congrats_text)
        self.objects.append(self.yourTime_text)
        self.objects.append(self.actual_time_text)
    def events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.restartButton.click()

        for obj in self.objects:
            obj.events(event)

    def render(self):
        for obj in self.objects:
            obj.render()

class level_select_screen(basic_display):
    def __init__(self, game):
        basic_display.__init__(self, game)
        self.character_cell_height = 200
        self.character_select_border = 5
        self.buttonWidth = 150
        img_size = self.character_cell_height - 2 * self.character_select_border
        self.playButton = button.Button(self, 'play', (self.width - self.character_cell_height) / 2 + 300 - self.buttonWidth/2 + self.character_cell_height, self.height / 2 + 100, self.buttonWidth, 150, icon=[pygame.image.load('Assets/Icons/play.png'), pygame.image.load('Assets/Icons/play_hover.png')])
        self.menuButton = button.Button(self, 'start_screen', (self.width - self.character_cell_height) / 2 - 300 - self.buttonWidth/2 + self.character_cell_height, self.height / 2 + 100, self.buttonWidth, 150, icon=[pygame.image.load('Assets/Icons/home.png'), pygame.image.load('Assets/Icons/home_hover.png')])
        self.ch0Button = button.Button(self, 'change_character', 0, 0, 10 + img_size, 10 + img_size, (32,10,10), text='0', text_color='white', outline_width=0)
        self.ch1Button = button.Button(self, 'change_character', 0, self.character_cell_height, 10 + img_size, 10 + img_size, (32,10,10), text='1', text_color='white', outline_width=0)
        self.ch2Button = button.Button(self, 'change_character', 0, self.character_cell_height*2, 10 + img_size, 10 + img_size, (32,10,10), text='2', text_color='white', outline_width=0)
        self.ch3Button = button.Button(self, 'change_character', 0, self.character_cell_height*3, 10 + img_size, 10 + img_size, (32,10,10), text='3', text_color='white', outline_width=0)
        self.map_buttons = []
        self.mapNames, self.maps, self.allowed_chars = self.getMaps()
        self.game.currentMap = 0
        self.char_choice_storage = self.game.character

        self.character_colors = [[5, 219, 5], [250,50,50], [249, 249, 20], [65, 242, 255]]
        self.character_sprites = [pygame.image.load("Assets/Sprites/green_right.png"), pygame.image.load("Assets/Sprites/red_right.png"), pygame.image.load("Assets/Sprites/yellow_right.png"), pygame.image.load("Assets/Sprites/teal_right.png")]
        self.gray_sprites = [pygame.transform.scale(sprite.copy(), (img_size, img_size)) for sprite in self.character_sprites]
        for s in self.gray_sprites:
            s.fill((78, 78, 78), special_flags=pygame.BLEND_RGB_MULT)
        self.sprite_rects = []

        for s in range(len(self.character_sprites)):
            self.character_sprites[s] = pygame.transform.scale(self.character_sprites[s], (img_size, img_size))
            sprite_rect = self.character_sprites[s].get_rect()
            sprite_rect.x,sprite_rect.y = self.character_select_border, self.character_select_border + s*self.character_cell_height
            self.sprite_rects.append(sprite_rect)

        self.bgColor = (0, 0, 0)
        self.tileColor = (200, 200, 200)
        self.speedColor = (50, 230, 50)
        self.jumpColor = (50, 50, 250)
        self.bounceColor = (250, 50, 50)
        self.winColor = (182, 196, 77)
        self.spawnColor = (200, 100, 0)
        self.colors = (self.bgColor, self.tileColor, self.speedColor, self.jumpColor, self.bounceColor, self.winColor, self.spawnColor)

        self.map_width = 400
        self.map_height =200
        self.map_gap = 100
        self.slide_due = 0
        self.slide_speed = 90
        self.slide_dist = 0
        self.preview_block_size = self.map_height // len(self.maps[0])
        self.preview_width_blocks = self.map_width // self.preview_block_size

        self.name_texts = []
        self.make_previews_names_and_buttons()

    def change_map(self, amount: int):
        if 0 <= self.game.currentMap + amount < len(self.mapNames) and self.slide_due == 0:
            self.game.currentMap += amount
            self.slide_due = -amount * (self.map_gap + self.map_width)
            self.manage_map_buttons(-1)
            if self.allowed_chars[self.game.currentMap].__contains__(self.char_choice_storage):
                self.game.character = self.char_choice_storage
        else:
            print('no more maps')

    def change_character(self, amount):
        if 0 <= self.game.character + amount <= 3:
            self.game.character += amount
            self.char_choice_storage = self.game.character
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
        elif event.type == pygame.MOUSEWHEEL:
            self.change_map(-event.y)

    def getMaps(self):
        n, m, a = [], [], []
        for i in range(len(maps.names)):
            n.append(maps.names[i])
            m.append(maps.maps[i])
            a.append(maps.allowed_chars[i])
        try:
            if self.game.currentMap > len(n) - 1:
                self.game.currentMap -= 1
                self.slide_dist += self.map_gap + self.map_width

        except:
            pass
        return n, m, a

    def slide_maps(self):
        copy = self.slide_due
        if self.slide_due < 0:
            if self.slide_due < -self.slide_speed:
                self.slide_due += self.slide_speed
                self.slide_dist -= self.slide_speed
            else:
                self.slide_dist += self.slide_due
                self.slide_due = 0
        elif self.slide_due > 0:
            if self.slide_due > self.slide_speed:
                self.slide_due -= self.slide_speed
                self.slide_dist += self.slide_speed
            else:
                self.slide_dist += self.slide_due
                self.slide_due = 0
            if self.slide_dist > 0:
                self.slide_dist = 0
                self.slide_due = 0
        if self.slide_due == 0 and copy != 0:  #spawns buttons if the maps stopped moving
            self.manage_map_buttons(1, offset=copy)

    def render(self):
        if self.mapNames[self.game.currentMap] == 'Tutorial 1' and self.game.character > 1:
            self.game.character = 1
        if self.mapNames[self.game.currentMap] == 'Tutorial 2' and self.game.character < 2:
            self.game.character = 2
        self.delta = self.game.delta_time
        self.screen.fill((0, 40, 0))
        for obj in self.particles:
            obj.render()
        for obj in self.objects:
            obj.render()
        self.slide_maps()
        for i in range(len(self.name_texts)):
            x = (self.width - self.character_cell_height) / 2 + self.character_cell_height + i*(self.map_width + self.map_gap) + self.slide_dist
            self.name_texts[i].x = x
            self.name_texts[i].update_pos()
        for i in range(len(self.previews)):
            self.render_map(i)

        pygame.draw.rect(self.screen, (32, 10, 10), (0, 0, self.character_cell_height, self.height))
        a = self.game.character
        x = 0
        y = a * self.character_cell_height
        pygame.draw.rect(self.screen, self.character_colors[a],
                         (x, y, self.character_cell_height, self.character_cell_height))


        for i in range(4):
            if self.allowed_chars[self.game.currentMap].__contains__(i):
                self.screen.blit(self.character_sprites[i], self.sprite_rects[i])
            else:
                self.screen.blit(self.gray_sprites[i], self.sprite_rects[i])

    def make_previews_names_and_buttons(self):
        if self.name_texts != []:
            for name in self.name_texts:
                name.delete()

        self.name_texts = []
        for i in range(len(self.maps)):
            x = (self.width - self.character_cell_height) / 2 + self.character_cell_height + i*(self.map_width + self.map_gap)
            text = custom_text.Custom_text(self, x, self.midy - 450, self.game.font, self.game.debug_text_size, self.mapNames[i], text_color='white')
            self.name_texts.append(text)

        self.previews = []
        for m in self.maps:
            map = []
            for row in range(len(m)):
                map.append([])
                for block in range(len(m[row])):
                    if block < self.preview_width_blocks:
                        map[row].append(m[row][block])
            self.previews.append(map)
        self.manage_map_buttons(1)


    def render_map(self, i):
        map = self.previews[i]
        pbs = self.preview_block_size

        actual_width = pbs*len(map[0])
        current_map_width = min(actual_width, self.map_width)
        x0, y0 = self.name_texts[i].x - current_map_width//2, self.name_texts[i].y + 60


        if i == self.game.currentMap:
            pygame.draw.rect(self.screen, 'yellow', (x0 - 10, y0 - 10, current_map_width+20, self.map_height+20))
        for row in range(len(map)):
            for column in range(len(map[row])):
                x = x0 + column*pbs
                y = y0 + row*pbs
                pygame.draw.rect(self.screen, self.colors[map[row][column]], (x, y, pbs, pbs))

    def manage_map_buttons(self, mode, offset=0):
        if mode == 1:
            for i in range(len(self.maps)):
                map = self.previews[i]
                pbs = self.preview_block_size

                actual_width = pbs * len(map[0])
                current_map_width = min(actual_width, self.map_width)
                x, y = self.name_texts[i].x - current_map_width//2 + offset, self.name_texts[i].y + 60
                b = button.Button(self, 'select_map',x, y, current_map_width, self.map_height, text='do not render')
                self.map_buttons.append(b)
        if mode == -1:
            if self.map_buttons == []:
                return
            else:
                for b in self.map_buttons:
                    b.delete()
            self.map_buttons = []

class map_editor_list(basic_display):
    def __init__(self, game):
        basic_display.__init__(self, game)
        self.game = game
        self.new_map_button = button.Button(self, 'map_editor', 105,25, 75,75, text='+', icon=[pygame.image.load('Assets/Icons/plus.png'), pygame.image.load('Assets/Icons/plus_hover.png')])
        self.menuButton = button.Button(self, 'start_screen', 25,25, 75,75, icon=[pygame.image.load('Assets/Icons/home.png'), pygame.image.load('Assets/Icons/home_hover.png')])
        self.map_height = 150
        self.map_width = 1000
        self.little_button_size = self.map_height - 30
        self.mapLog_x = self.width/2 - self.map_width/2
        self.current_top_map = 0
        self.current_selected_map = None
        self.small_buttons = []
        self.scroll_dist = 0
        self.scroll_due = 0
        self.scroll_speed = 20
        self.map_buttons = []
        self.getMaps()
    def getMaps(self):
        n, m = [], []
        for i in range(len(maps.names)):
            n.append(maps.names[i])
            m.append(maps.maps[i])
        self.mapNames, self.maps = n, m
        self.visible_maps = min(len(self.mapNames), 5)
        self.visible_space = self.visible_maps * (self.map_height + 15)
        self.mapLog_start_y = (self.height - self.visible_space) / 2
        self.scroll_curtain_y = self.mapLog_start_y + self.visible_space
        if self.map_buttons != []:
            for b in self.map_buttons:
                if self.small_buttons.__contains__(b):
                    self.small_buttons.remove(b)
                b.delete()
        self.map_buttons = []
        self.refresh_buttons()

    def render(self):
        for obj in self.objects:
            obj.render()

        for b in self.map_buttons:
            if b.text == None:
                b.render()
        pygame.draw.rect(self.screen, 'black', (self.mapLog_x, self.scroll_curtain_y, self.width, 1000))
        pygame.draw.rect(self.screen, 'black', (self.mapLog_x, 0, self.width, self.mapLog_start_y))
        for obj in self.objects:
            if isinstance(obj, button.Button):
                if not self.map_buttons.__contains__(obj):
                    obj.render()
        if self.scroll_due < 0:
            if self.scroll_due < -self.scroll_speed:
                self.scroll_due += self.scroll_speed
                self.scroll_dist -= self.scroll_speed
            else:
                self.scroll_dist += self.scroll_due
                self.scroll_due = 0
            if self.scroll_dist < -(len(self.maps)+1)*(self.map_height + 15) + self.visible_space:
                self.scroll_dist = -(len(self.maps)+1)*(self.map_height + 15) + self.visible_space
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

    def refresh_buttons(self, trash=None, y=None):

        if self.map_buttons != []:
            for b in self.map_buttons:
                if self.small_buttons.__contains__(b):
                    self.small_buttons.remove(b)
                b.delete()
        self.map_buttons = []
        for i in range(len(self.maps) + 1):
            # print(self.mapNames[i])
            if i == trash:
                continue
            oc = 'white'
            y = self.scroll_dist + self.mapLog_start_y + i*(self.map_height+15)
            if i == self.current_selected_map:
                oc = 'yellow'
                self.make_small_buttons(y)
            if i == len(self.maps):
                print('plus')
                mb = button.Button(self, 'map_editor', self.mapLog_x, y, self.map_width,self.map_height, (0, 0, 0), outline_color=oc, text='+', text_color='white', font_size=int(self.map_height*0.7))
            else:
                mb = button.Button(self, 'select_map', self.mapLog_x, y, self.map_width,self.map_height, (0, 0, 0), outline_color=oc, text=self.mapNames[i], text_color='white')
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
            if event.key == pygame.K_ESCAPE:
                self.menuButton.click()
        if event.type == pygame.MOUSEWHEEL:
            self.scroll(event.y)
        for obj in self.small_buttons:
            obj.events(event)

            if self.game.current_display != self:
                print('stopped')
                return
        for obj in self.objects:
            obj.events(event)
            if self.game.current_display != self:
                return

    def make_small_buttons(self, y):
        lbs = self.little_button_size
        lil_distance = (self.map_height - lbs) // 2
        edit_button = button.Button(self, 'map_editor', self.mapLog_x +lil_distance, y + lil_distance, lbs,lbs, icon=[pygame.image.load('Assets/Icons/edit.png'), pygame.image.load('Assets/Icons/edit_hover.png')])
        trash_button = button.Button(self, 'trash_map', self.mapLog_x + self.map_width - lbs - lil_distance, y + lil_distance, lbs,lbs, icon=[pygame.image.load('Assets/Icons/trash.png'), pygame.image.load('Assets/Icons/trash_hover.png')])
        self.map_buttons.append(edit_button)
        self.map_buttons.append(trash_button)
        self.small_buttons.append(edit_button)
        self.small_buttons.append(trash_button)
    def trash(self):
        self.maps.pop(self.current_selected_map)
        self.mapNames.pop(self.current_selected_map)
        maps.delete(self.current_selected_map)
        self.refresh_buttons(self.current_selected_map)
        self.current_selected_map = None
    def check_if_visible(self):
        if len(self.maps)+1 <= self.visible_maps:
            return True
        sel = self.current_selected_map
        top = self.current_top_map
        if sel < top:
            return False
        if sel >= top + self.visible_maps:
            return False
        return True

class map_editor(basic_display):
    def __init__(self, game):
        basic_display.__init__(self, game)
        self.game = game
        self.bgColor = (0, 0, 0)
        self.tileColor = (200, 200, 200)
        self.speedColor = (50, 230, 50)
        self.jumpColor = (50, 50, 250)
        self.bounceColor = (250, 50, 50)
        self.winColor = (182, 196, 77)
        self.spawnColor = (200, 100, 0)
        self.cam_speed = 15
        self.colors = (self.bgColor, self.tileColor, self.speedColor, self.jumpColor, self.bounceColor, self.winColor, self.spawnColor)
        self.blocks = [0, 1, 2, 3, 4, 5, 6] # 0 is air, 1 is normal, 2 is speed, 3 is jump, 4 is bounce, 5 is win, 6 is spawn
        self.current_block = 1
        self.camera = 0
        self.movement = 0
        self.clicked = 0
        self.original = None
        self.map = [[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] ,
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] ,
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] ,
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] ,
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] ,
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] ,
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] ,
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] ,
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] ,
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] ,
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] ,
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] ,
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] ,
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] ,
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] ,
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] ,
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] ,
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] ,
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] ,
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
        self.mapName = self.get_map_name()
        self.tileSize = int(self.height / len(self.map))
        self.width_in_tiles, self.height_in_tiles = self.width // self.tileSize, int(self.height // self.tileSize)
        self.quitButton = button.Button(self, 'map_editor_list', 25,25, 75,75, text='Exit', icon=[pygame.image.load('Assets/Icons/trash.png'), pygame.image.load('Assets/Icons/trash_hover.png')])
        self.saveButton = button.Button(self, 'map_editor_list', self.width - 100,25, 75,75, text='Save', icon=[pygame.image.load('Assets/Icons/tick.png'), pygame.image.load('Assets/Icons/tick_hover.png')])

    def introduce_map(self, map, name):
        self.map = map
        self.mapName = name
        self.original = name
        self.movement = 0
        self.camera = 0
        self.tileSize = int(self.height / len(self.map))

    def get_map_name(self):
        for i in range(1, 100):
            path = 'maps/New map ' + str(i) + '.txt'
            if not os.path.isfile(path):
                return 'New map ' + str(i)
        print('too many maps')

    def render(self):
        self.camera += self.movement
        if self.camera < 0:
            self.camera = 0
        if self.camera // self.tileSize > len(self.map[0]) - self.width_in_tiles -1:
            for i in range(len(self.map)):
                if i < self.height_in_tiles - 1:
                    self.map[i].append(0)
                else:
                    self.map[i].append(1)
        for row in range(self.height_in_tiles):
            for column in range(self.camera // self.tileSize, len(self.map[0])):
                color = self.colors[self.map[row][column]]
                pygame.draw.rect(self.screen, color, (column * self.tileSize - self.camera, row * self.tileSize, self.tileSize - 1, self.tileSize - 1))

        for obj in self.objects:
            obj.render()

    def events(self, event):

        for obj in self.objects:
            obj.events(event)
        if self.game.current_display != self:
            return
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.clicked = event.button
        elif event.type == pygame.MOUSEBUTTONUP:
                self.clicked = 0
        if self.clicked != 0:
            a = self.current_block
            if self.clicked == 3:
                self.current_block = 0
            pos = pygame.mouse.get_pos()
            try:
                self.map[pos[1] // self.tileSize][(pos[0] + self.camera) // self.tileSize] = self.current_block
            except:
                print('map editor slight error')
            self.current_block = a
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                self.movement = self.cam_speed
            if event.key == pygame.K_a:
                self.movement = -self.cam_speed

            if event.key == pygame.K_0:
                self.current_block = 0
            if event.key == pygame.K_1:
                self.current_block = 1
            if event.key == pygame.K_2:
                self.current_block = 2
            if event.key == pygame.K_3:
                self.current_block = 3
            if event.key == pygame.K_4:
                self.current_block = 4
            if event.key == pygame.K_5:
                self.current_block = 5
            if event.key == pygame.K_6:
                self.current_block = 6

        elif event.type == pygame.KEYUP:
            if event.key in [pygame.K_d, pygame.K_a]:
                self.movement = 0

    def reset(self):
        self.current_block = 1
        self.camera = 0
        self.movement = 0
        self.clicked = 0
        self.map = [
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
             1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
        self.mapName = self.get_map_name()
        self.original = None

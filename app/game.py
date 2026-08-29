import time


import ctypes
from logging import exception

user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
import pygame

import app.player
import maps
from app import config, display, custom_text
import maps


class Game:
    def __init__(self):
        pygame.init()
        config.set_config()

        self.cfg = config.read_config()

        self.version = self.cfg['version']
        self.width = float(self.cfg['width'])
        self.height = float(self.cfg['height'])
        # self.fps = float(self.cfg['fps'])
        self.fps = 60
        self.title = self.cfg['title']
        self.enable_debug = int(self.cfg['enable_debug'])
        self.music_volume = int(self.cfg["music_volume"])
        self.sound_volume = int(self.cfg["sound_volume"])

        self.clock = pygame.time.Clock()
        self.font = None
        self.countdown = -1
        self.currentMap = None

        self.player = None
        self.character = 0

        self.start_time = None
        self.paused_start = None
        self.pause_sum = 0
        self.curr_pause_time = 0
        self.time_now = None
        self.delta_time = 0

        self.header_text_size = 150
        self.timer_text_size = 130
        self.normal_text_size = 50
        self.debug_text_size = 50

        self.run = True

        self.objects = []
        if self.cfg['fullscreen'] == '1':
            self.width, self.height = screensize
        maps.startup_map_load()

        self.screen = pygame.display.set_mode((self.width, self.height))

        if self.cfg['fullscreen'] == '1':
            pygame.display.toggle_fullscreen()

        pygame.display.set_caption(f"{self.title} (v {self.version})")

        self.displays = {'template_display': display.basic_display(self), 'level_select_screen': display.level_select_screen(self), 'game_display': display.game_display(self), 'pause_display': display.pause_display(self), 'start_screen': display.start_screen(self), 'settings_screen': display.settings_screen(self), 'win_screen': display.win_screen(self), 'map_editor_list': display.map_editor_list(self), 'map_editor': display.map_editor(self)}
        self.current_display = self.displays['start_screen']

        self.pointing_at = []

        self.debug = False
        self.debug_items = [custom_text.Custom_text(self, 12, 15, self.font, self.debug_text_size, f'Current version: {self.version}', text_color='white', center=False),
                            custom_text.Custom_text(self, 12, 45, self.font, self.debug_text_size, f'Resolution: {self.width}x{self.height}', text_color='white', center=False),
                            custom_text.Custom_text(self, 12, 75, self.font, self.debug_text_size, f'FPS cap: {self.fps}', text_color='white', center=False),
                            custom_text.Custom_text(self, 12, 105, self.font, self.debug_text_size, f'FPS: {self.clock.get_fps()}', text_color='white', center=False),
                            custom_text.Custom_text(self, 12, 135, self.font, self.debug_text_size, f'Objects in memory: {len(self.current_display.objects)}', text_color='white', center=False),
                            custom_text.Custom_text(self, 12, 165, self.font, self.debug_text_size, f'Current display: {type(self.current_display)}', text_color='white', center=False),
                            custom_text.Custom_text(self, 12, 195, self.font, self.debug_text_size, f'Pointing at: {self.pointing_at}', text_color='white', center=False)]

        self.timer_text = custom_text.Custom_text(self, self.width - self.timer_text_size * 3.1, self.height - 130, "Assets/digital-7.ttf", self.timer_text_size, self.getTimer(), text_color='white', background_color='black', center=False)
        self.countdown_text = custom_text.Custom_text(self, self.width / 2, self.height / 3, "Assets/digital-7.ttf", 80, str(self.countdown // 6), text_color='white', background_color='black', center=False)



        for debug_item in self.debug_items:
            debug_item.hidden = True

        pygame.mixer.music.load("Assets/Music/Menu music.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(self.music_volume/100)
        self.click_sound = pygame.mixer.Sound("Assets/Sounds/Click.mp3")
        self.click_sound.set_volume(self.sound_volume/100)

        self.mainloop()

    def getTimer(self, update=False):
        try:
            seconds = (self.time_now - self.start_time - self.pause_sum - self.curr_pause_time) / 1000
            minutes = seconds // 60
            seconds %= 60

            s = int(seconds)
            ms = seconds % 1
            ms *= 100
            ms = int(ms)
            ms.__round__(0)

            if s <10:
                s = '0' + str(int(s))
            if ms <10:
                ms = '0' + str(int(ms))
            if minutes <10:
                minutes = '0' + str(int(minutes))
            minutes, s, ms = str(minutes), str(s), str(ms)
            r = ''
            r+= minutes
            r+=':'
            r+= s
            r+=':'
            r += ms
            if update:
                self.timer_text.update_text(r)
            return r
        except:
            if update:
                self.timer_text.update_text('0:00')
            return '0:00'

    def mainloop(self):
        self.timer_text.hidden = True
        while self.run:
            self.screen.fill('black')
            self.events()
            self.current_display.tick()
            for object in self.objects:
                object.tick()
            self.update()

            self.clock.tick(self.fps)
            self.time_now = time.time_ns() // 1000000
            if not self.paused_start == None:
                self.curr_pause_time = self.time_now - self.paused_start
            if self.curr_pause_time == 0:
                if self.countdown > 0:
                    self.start_time = time.time_ns() // 1000000
                    self.countdown -= 1
                elif self.countdown == 0:
                    self.countdown -= 1
                    self.timer_text.hidden = False
                else:
                    self.countdown_text.hidden = True


    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSLASH and self.enable_debug:
                    self.debug = not self.debug
                    for di in self.debug_items:
                        di.hidden = not di.hidden
                elif event.key == pygame.K_t and self.current_display in (self.displays['game_display'], self.displays['pause_display']):
                    if self.timer_text.hidden:
                        self.timer_text.hidden = False
                    else:
                        self.timer_text.hidden = True
            self.current_display.events(event)

    def update(self):
        if self.debug:
            self.show_debug()

        if self.clock.get_time() / 1000.0 > 0.1:
            self.delta_time = 0.1
        else:
            self.delta_time = self.clock.get_time() / 1000.0

        self.getTimer(update=True)
        self.countdown_text.update_text(str(self.countdown // 6))

        pygame.display.update()
        pygame.display.flip()

    def show_debug(self):

        for obj in self.current_display.objects:
            try:
                if not obj.rect.collidepoint(pygame.mouse.get_pos()):
                    continue
                if obj in self.pointing_at:
                    continue
                self.pointing_at.append(obj)
            except:
                pass

        i = []
        for obj in self.pointing_at:
            if obj.rect.collidepoint(pygame.mouse.get_pos()) == False:
                i.append(obj)
        for obj in i:
            self.pointing_at.remove(obj)
        i = []

        self.debug_items[3].update_text(f'FPS: {self.clock.get_fps()}')
        self.debug_items[4].update_text(f'Objects in memory: {len(self.current_display.objects)}')
        self.debug_items[5].update_text(f'Current display: {type(self.current_display)}')
        self.debug_items[6].update_text(f'Pointing at: {self.pointing_at}')

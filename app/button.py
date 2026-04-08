import time

import pygame
import maps
from app import custom_text, player

class Button:
    def __init__(self, display, action, x, y, width, height, color=(0,0,0), text=None, text_color='black', outline_color=None, outline_width=5, font_size=None, icon=None):  # Getting all the parameters of the button

        self.action = action
        self.text = text
        self.display = display
        self.cooldown = 2
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.game = self.display.game

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.iconAmount = 0
        if icon != None:
            if type(icon) == list:
                self.img, self.img_hover = icon[0], icon[1]
                self.img, self.img_hover = pygame.transform.scale(self.img, (self.width, self.height)), pygame.transform.scale(self.img_hover, (self.width, self.height))
                self.iconAmount = 2
            else:
                self.img = icon
                self.img = pygame.transform.scale(self.img, (self.width, self.height))
                self.iconAmount = 1
        self.display.objects.append(self)
        if font_size == None:
            f = int(self.height // 1.7)
        else:
            f = font_size
        if text == 'do not render':
            self.text = text
            self.cooldown = 0
        elif text != None and self.iconAmount == 0:
            center = self.y + self.height/2
            self.text_entity = custom_text.Custom_text(self.display, self.x + self.width / 2, center, None,
                                    f, text, text_color=text_color)
            self.text = text

        self.outline_color = outline_color
        self.outline_width = outline_width

    def render(self):  # Rendering a button on screen
        if self.text == 'do not render':
            return
        self.cooldown -= 1
        if self.iconAmount == 0:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(self.display.screen, self.get_hover_color(), self.rect, border_radius=10)
            else:
                pygame.draw.rect(self.display.screen, self.color, self.rect, border_radius=10)

        elif self.iconAmount == 1:
            self.game.screen.blit(self.img, self.rect)
        else:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.game.screen.blit(self.img_hover, self.rect)
            else:
                self.game.screen.blit(self.img, self.rect)

        if self.outline_color != None:
            pygame.draw.rect(self.display.screen, self.outline_color, self.rect, self.outline_width, border_radius=10)

    def events(self, event):  # Checks events
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.cooldown <= 0 and self.rect.collidepoint(event.pos):  # Checks if the button has been pressed
            self.click()


    def delete(self):
        try:
            self.text_entity.delete()
        except:
            pass
        # if self.action == 'map_editor':
        #     print('deleted')
        self.display.objects.remove(self)
        del self.text
        del self


    def click(self):
        if self.action == 'map_editor':
            if self.text == '+': #new map
                self.game.current_display = self.game.displays['map_editor']
                self.game.current_display.reset()
            else: #edit map
                if self.game.current_display.check_if_visible():

                    i = self.game.current_display.current_selected_map
                    self.game.current_display.current_selected_map = None
                    self.game.current_display.refresh_buttons()
                    m = maps.maps[i]
                    n = maps.names[i]
                    self.game.current_display = self.game.displays['map_editor']
                    self.game.current_display.introduce_map(m,n)
                else:
                    print('invisible', self.text)
        elif self.action == 'map_editor_list':
            if self.text == 'Save':
                maps.add(self.game.current_display.mapName, self.game.current_display.map, original=self.game.current_display.original)
                lsc = self.game.displays['level_select_screen']
                self.game.currentMap = 0
                lsc.slide_dist = 0
                lsc.mapNames, lsc.maps, lsc.allowed_chars = lsc.getMaps()
                lsc.manage_map_buttons(-1)
                lsc.make_previews_names_and_buttons()
                self.game.displays['map_editor_list'].current_selected_map = None
                self.game.displays['map_editor_list'].getMaps()
            self.game.current_display = self.game.displays['map_editor_list']
        elif self.action == 'trash_map':
            if self.game.current_display.check_if_visible():
                self.game.current_display.trash()
                lsc = self.game.displays['level_select_screen']
                self.game.currentMap = 0
                lsc.slide_dist = 0
                lsc.mapNames, lsc.maps, lsc.allowed_chars = lsc.getMaps()
                lsc.manage_map_buttons(-1)
                lsc.make_previews_names_and_buttons()
        elif self.action == 'change_character':
            self.game.character = int(self.text)
        elif self.action == 'settings':
            self.game.current_display = self.game.displays['settings_screen']
        elif self.action == 'start_screen':
            self.game.current_display = self.game.displays['start_screen']
            self.game.current_display.count = 0
            self.game.current_display.title.x = -50
        elif self.action == 'play':
            self.playClicked()
        elif self.action == 'resume':
            self.resumeClicked()
        elif self.action == 'restart':
            self.restartClicked()
        elif self.action == 'pause':
            self.pauseClicked()
        elif self.action == 'start_screen_after_win':
            self.game.current_display = self.game.displays['start_screen']
            self.game.current_display.count = 0
            self.game.current_display.title.x = -50
            self.game.startTime = time.time_ns() // 1000000
        elif self.action == 'level_select_screen':
            if self.text == 'Quit':
                musicTime = pygame.mixer.music.get_pos() * 3 / 2000
                pygame.mixer.music.load("Assets/Music/Menu music.mp3")
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_pos(musicTime)
                self.game.player.delete()
            self.game.current_display = self.game.displays['level_select_screen']
            self.game.timerText.hidden = True
        elif self.action == 'quit_game':
            pygame.display.quit()
        elif self.action == 'select_map':
            if self.text == 'do not render': #that means it's in the level select screen
                id = self.game.current_display.map_buttons.index(self)
                if self.game.currentMap == id:
                    self.playClicked()
                amount = id - self.game.currentMap
                if amount != 0:
                    self.game.current_display.change_map(amount)
            else:
                id = self.game.current_display.mapNames.index(self.text)
                if self.game.current_display.current_selected_map == id:
                    self.game.current_display.current_selected_map = None
                    self.text_entity.text_color = 'white'
                    self.game.current_display.refresh_buttons()

                else:
                    self.game.current_display.current_selected_map = id
                    self.text_entity.text_color = 'yellow'
                    self.game.current_display.refresh_buttons()


        else:
            print(self.text, self.action, 'not implemented')

    def get_hover_color(self):
        biggest = max(self.color)
        if biggest <= 225:
            return tuple(color + 30 for color in self.color)
        else:
            return tuple(color - 30 if color >= 30 else 0 for color in self.color)

    def playClicked(self):
        self.game.current_display = self.game.displays['game_display']
        self.game.current_display.get_map()
        self.game.startTime = time.time_ns() // 1000000
        self.game.pauseSum = 0
        self.game.currPauseTime = 0
        self.game.timeNow = self.game.startTime
        self.game.countdown = 59
        self.game.pausedStart = None
        self.game.current_display.player = player.Player(self.game.current_display)
        self.game.player = self.game.current_display.player
        self.game.getTimer(update=True)
        self.game.countdownText.hidden = True
        self.game.countdownText.update_text(str(self.game.countdown // 6))
        musicTime = pygame.mixer.music.get_pos() * 2/3000
        pygame.mixer.music.load("Assets/Music/Fast music.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_pos(musicTime)

    def restartClicked(self):
        self.game.current_display = self.game.displays['game_display']
        self.game.current_display.player.reset(True)

    def pauseClicked(self):
        self.game.current_display = self.game.displays['pause_display']
        self.game.pausedStart = time.time_ns() // 1000000
        self.game.countdownText.hidden = True

    def resumeClicked(self):
        self.game.current_display = self.game.displays['game_display']
        if self.game.countdown < 0:
            self.game.pauseSum += self.game.currPauseTime
        self.game.currPauseTime = 0
        self.game.pausedStart = None
        if self.game.countdown > 0:
            self.game.pauseSum = 0
            self.game.countdownText.hidden = False



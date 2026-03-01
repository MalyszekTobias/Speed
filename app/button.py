import time

import pygame
from app import custom_text, player

class Button:
    def __init__(self, display, action, x, y, width, height, color, text=None, text_color='black', outline_color=None, outline_width=5):  # Getting all the parameters of the button

        self.action = action
        self.text = text
        self.display = display

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.game = self.display.game

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)  # Creating a rect object

        self.display.objects.append(self)  # Adding self to objects of the screen

        if text != None:  # if there is text it's put on the button
            self.text_entity = custom_text.Custom_text(self.display, self.x + self.width / 2, self.y + self.height / 2, None,
                                    int(self.height // 1.7), text, text_color=text_color)
            self.text = text

        self.outline_color = outline_color
        self.outline_width = outline_width

    def render(self):  # Rendering a button on screen
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(self.display.screen, self.get_hover_color(), self.rect, border_radius=10)
        else:
            pygame.draw.rect(self.display.screen, self.color, self.rect, border_radius=10)


        if self.outline_color != None:
            pygame.draw.rect(self.display.screen, self.outline_color, self.rect, self.outline_width, border_radius=10)

    def events(self, event):  # Checks events
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos):  # Checks if the button has been pressed
            self.click()


    def delete(self):
        self.text_entity.delete()
        self.display.objects.remove(self)
        del self.text
        del self


    def click(self):
        if self.action == 'map_editor':
            self.game.current_display = self.game.displays['map_editor_list']
        elif self.action == 'change_character':
            self.game.character = int(self.text)
        elif self.action == 'settings':
            self.game.current_display = self.game.displays['settings_screen']
        elif self.action == 'start_screen':
            self.game.current_display = self.game.displays['start_screen']
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
            self.game.startTime = time.time_ns() // 1000000
        elif self.action == 'level_select_screen':
            if self.text == 'Quit':
                self.game.player.delete()
            self.game.current_display = self.game.displays['level_select_screen']
            self.game.timerText.hidden = True
        elif self.action == 'quit_game':
            pygame.display.quit()
        elif self.action == 'select_map':
            id = self.game.current_display.mapNames.index(self.text)
            if self.game.current_display.current_selected_map == id:
                self.game.current_display.current_selected_map = None
                self.text_entity.text_color = 'white'
            else:
                self.game.current_display.current_selected_map = id
                self.text_entity.text_color = 'yellow'
            self.game.current_display.refresh_buttons()

        else:
            print('clicked')

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
        a = self.game.getTimer()
        self.game.countdownText.hidden = True
        if a != '0:00' and int(a) >= 10 ** (self.game.timerDigits - 3):
            self.game.timerDigits += 1
            self.game.timerText.x = self.game.width - self.game.timerDigits * 45
        self.game.timerText.update_text(str(a))
        self.game.countdownText.update_text(str(self.game.countdown // 6))

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



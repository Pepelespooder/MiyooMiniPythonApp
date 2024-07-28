import pygame
from pygame.locals import *
import sys
import os
from datetime import datetime

class App:
    def draw_text(self, font, color, x, y, align='left', text=''):
        text_obj = font.render(text, True, color)
        text_rect = text_obj.get_rect()
        if align == 'center':
            text_rect.midtop = (x, y)
        elif align == 'right':
            text_rect.topright = (x, y)
        else:  # left
            text_rect.topleft = (x, y)
        self.screen.blit(text_obj, text_rect)
        
    def draw_button(self, x, y, text, active):
        width = 100
        height = 40
        if active:
            color = self.button_color
        else:
            color = self.button_color_active
        pygame.draw.rect(self.screen, color, (x, y, width, height))
        self.draw_text(self.font, self.white, x + width // 2, y + height // 2 - self.font.get_height() // 2, 'center', text)

    def draw_progressbar(self, x, y, width, height, percent):
        pygame.draw.rect(self.screen, self.progressbar_color, (x, y, width, height))
        pygame.draw.rect(self.screen, self.progressbar_bar_color, (x, y, int(width * (percent / 100.0)), height))
        
    def draw_scrollbox(self, x, y, width, percent):
        height = self.app_height - y - 30
        scrollbox_width = 4
        scrollbox_height = height // (self.memo_lines_max / self.memo_lines_ouput_max)
        scrollbox_y = y + (height - scrollbox_height) * (percent / 100.0)
        pygame.draw.rect(self.screen, self.scrollbox_background_color, (x, y, scrollbox_width, height), 0)
        if percent != -1:
            pygame.draw.rect(self.screen, self.white, (x, scrollbox_y, scrollbox_width, scrollbox_height), 0)

    def __init__(self):
        pygame.init()
        self.app_width = 640
        self.app_height = 480
        self.screen = pygame.display.set_mode((self.app_width, self.app_height))
        pygame.display.set_caption('App')
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.background.fill((7, 18, 22))
        self.black = pygame.Color(0, 0, 0)
        self.white = pygame.Color(255, 255, 255)
        self.gray = pygame.Color(128, 128, 128)
        self.menu_item_color = pygame.Color(58, 69, 73)
        self.memo_background_color = pygame.Color(28, 35, 40)
        self.scrollbox_background_color = pygame.Color(60, 70, 72)
        self.button_color = pygame.Color(41, 50, 59)
        self.button_color_active = pygame.Color(59, 71, 84)
        self.progressbar_color = pygame.Color(50, 54, 65)
        self.progressbar_bar_color = pygame.Color(160, 169, 176)
        self.font_size = 32
        self.font = pygame.font.Font(None, self.font_size)
        self.fps_controller = pygame.time.Clock()
        self.layout_index = 0
        self.main_list = ['Set RTC', 'Option 2', 'Option 3']
        self.main_list_output_max = 12
        self.list_selected_index = 0    
        self.list_selected_offset = 0  
        self.list_selected_item = ''
        
        self.input_active = False
        self.input_text = ''
        
        self.rtc_file = 'rtc.txt'
        self.load_rtc()

        self.main_loop()

    def load_rtc(self):
        if os.path.exists(self.rtc_file):
            with open(self.rtc_file, 'r') as file:
                self.rtc_time = file.read().strip()
        else:
            self.rtc_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.save_rtc()

    def save_rtc(self):
        with open(self.rtc_file, 'w') as file:
            file.write(self.rtc_time)

    def main_loop(self):
        while True:
            self.handle_events()
            self.update_screen()
            self.fps_controller.tick(30)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if self.layout_index == 0:
                    if event.key == K_ESCAPE or event.key == K_BACKSPACE or event.key == K_SPACE:
                        pygame.quit()
                        sys.exit()
                    elif event.key == K_UP:
                        if self.list_selected_index > 0:
                            self.list_selected_index -= 1
                        else:
                           self.list_selected_index = len(self.main_list) - 1 
                    elif event.key == K_DOWN:
                        if self.list_selected_index < len(self.main_list) - 1:
                            self.list_selected_index += 1
                        else:
                            self.list_selected_index = 0
                    elif event.key == K_RETURN or event.key == K_LCTRL:
                        self.list_selected_item = self.main_list[self.list_selected_index]
                        if self.list_selected_index == 0:
                            self.layout_index = 1
                            self.input_active = True
                            self.input_text = self.rtc_time
                    if self.list_selected_index > self.main_list_output_max - 1:
                        self.list_selected_offset = self.list_selected_index // self.main_list_output_max * self.main_list_output_max
                    else:
                        self.list_selected_offset = 0
                        
                elif self.layout_index == 1:
                    if event.key == K_ESCAPE or event.key == K_BACKSPACE or event.key == K_SPACE:
                        self.layout_index = 0
                        self.input_active = False
                    elif event.key == K_RETURN and self.input_active:
                        self.rtc_time = self.input_text
                        self.save_rtc()
                        self.layout_index = 0
                        self.input_active = False
                    elif event.key == K_BACKSPACE:
                        if self.input_active:
                            self.input_text = self.input_text[:-1]
                    else:
                        if self.input_active:
                            self.input_text += event.unicode
                    
    def update_screen(self):
        self.screen.fill(self.black)
        if self.layout_index == 0:
            self.draw_layout_list()
        elif self.layout_index == 1:
            self.draw_layout_set_rtc()
        
        pygame.display.flip()
        
    def draw_layout_list(self):
        self.draw_text(self.font, self.white, 8, 8, 'left', 'List')
        
        for i, line in enumerate(self.main_list):
            if i < self.list_selected_offset:
                continue
            if i - self.list_selected_offset >= self.main_list_output_max:
                continue
            if i == self.list_selected_index:
                item_background_color = self.white
                item_font_color = self.black
            else:
                item_background_color = self.menu_item_color
                item_font_color = self.white
            
            x = 8
            y = self.font_size * (i - self.list_selected_offset + 1) + 8
            width = self.app_width - 16
            height = self.font_size
            pygame.draw.rect(self.screen, item_background_color, (x, y, width, height - 1), 0)
            self.draw_text(self.font, item_font_color, x + 2, y + 4, 'left', self.cut_str(line, 70))
            
    def draw_layout_set_rtc(self):
        self.draw_text(self.font, self.white, 8, 8, 'left', 'Set RTC')
        self.draw_text(self.font, self.green, 10, 50, 'left', self.input_text)
        
    def cut_str(self, string, n):
        if len(string) > n:
            return string[:n-3] + '...'
        else:
            return string
            
    def add_line_breaks(self, text, n):
        result = ''
        count = 0

        for char in text:
            result += char
            count += 1

            if char == '\n':
                count = 0
                continue

            if count == n:
                count = 0
                text_len = len(result)
                added = False

                for i in range(1, n + 1):
                    if text_len - i < 0:
                        break
                    if result[text_len - i] == ' ':
                        result = result[:text_len - i] + '\n' + result[text_len - i + 1:]
                        added = True
                        break

                if not added:
                    result += '\n'
            
        return result

if __name__ == "__main__":
    app = App()

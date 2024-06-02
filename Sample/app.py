import pygame
from pygame.locals import *
import sys
import os

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
        if active == True:
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
        # background scrollbox
        pygame.draw.rect(self.screen, self.scrollbox_background_color, (x, y, scrollbox_width, height), 0)
        # active scroll
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
        #self.font = pygame.font.Font(os.path.join(os.path.dirname(__file__), 'arial.ttf'), 17)
        self.font_size = 32
        self.font = pygame.font.Font(None, self.font_size)
        self.fps_controller = pygame.time.Clock()
        self.layout_index = 0
        self.main_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20']
        self.main_list_output_max = 12
        self.list_selected_index = 0    
        self.list_selected_offset = 0  
        self.list_selected_item = ''
        
        self.memo = 'Python is a high-level programming language that has gained immense popularity due to its numerous advantages. Here are some key benefits that make Python attractive to developers and organizations worldwide:\n\n'
        self.memo += '1. Simplicity and Readability:\nPython is known for its simple and concise syntax, which makes it easy to read and understand, even for beginners. This reduces learning time and simplifies code maintenance.\n\n' 
        self.memo += '2. Extensive Libraries and Frameworks:\nPython has a vast standard library and numerous third-party libraries and frameworks, allowing it to address a wide range of tasks from web development (Django, Flask) to data analysis (Pandas, NumPy) and machine learning (TensorFlow, scikit-learn).\n\n' 
        self.memo += '3. Cross-Platform Compatibility: Python is cross-platform, meaning code written in Python can run on various operating systems like Windows, macOS, and Linux without modification.\n\n'
        self.memo += '4. Community and Support:\nPython boasts one of the largest and most active developer communities. This ensures ample resources, support, and regular updates to keep the language current with modern needs.\n\n'
        self.memo += '5. Versatility:\nPython is used in numerous fields, including web development, scientific research, artificial intelligence, and task automation. Its versatility allows developers to use the same language for various tasks, enhancing efficiency.\n\n'
        self.memo += '6. High Development Productivity:\nPython''s high-level syntax and rich library ecosystem accelerate development, reducing time-to-market and increasing development flexibility.\n\n'
        self.memo += '7. Integration with Other Languages:\nPython easily integrates with other languages like C, C++, and Java, serving as a bridge between different software components and maximizing performance.\n\n'
        self.memo += '8. Educational Use:\nDue to its simplicity, Python is often used for educational purposes, making it an excellent first language for learning programming basics.\n\n'
        self.memo += 'Overall, Python offers a powerful set of tools and capabilities, making it an ideal choice for solving diverse programming challenges.'
        
        #self.memo = '1234567890 1234567890 1234567890 1234567890 1234567890 1234567890 1234567890 1234567890 1234567890 1234567890 1234567890 1234567890 1234567890 1234567890 1234567890 1234567890 1234567890 '
        
        self.memo_line_offset = 0
        self.memo_lines_max = 0
        self.memo_lines_ouput_max = 13
        
        # Statuses
        self.progressbar_value = 75
        self.item1_turn_status = '< turn on>'
        self.btn1_active = False
        self.btn2_active = False

        self.main_loop()

    def main_loop(self):
        while True:
            self.handle_events()
            self.update_screen()
            self.fps_controller.tick(30) #fps limiter

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                # L1=K_e, L2=K_TAB, R1=K_t, R2=K_BACKSPACE, X=K_LSHIFT, Y=K_LALT, B=K_LCTRL, A=K_SPACE, SELECT=K_RCTRL, START=K_RETURN, DPADUP=K_UP, DPADDOWN=K_DOWN, DPAFLEFT=K_LEFT, DPADRIGHT=K_RIGHT
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
                    elif event.key == K_LEFT:
                        if self.progressbar_value > 0:
                            self.progressbar_value -= 1
                    elif event.key == K_RIGHT:
                        if self.progressbar_value < 100:
                            self.progressbar_value += 1
                    elif event.key == K_RETURN or event.key == K_LCTRL:
                        self.list_selected_item = self.main_list[self.list_selected_index]
                        if self.list_selected_index != 0:
                            self.layout_index = 1
                            self.memo_line_offset = 0
                        else:
                            if self.item1_turn_status == '< turn on>':
                                self.item1_turn_status = '< turn off>'
                            else:
                                self.item1_turn_status = '< turn on>'
                    elif event.key == K_e:
                        self.btn1_active = not self.btn1_active
                    elif event.key == K_t:
                        self.btn2_active = not self.btn2_active
                    if self.list_selected_index > self.main_list_output_max - 1:
                        self.list_selected_offset = self.list_selected_index // self.main_list_output_max * self.main_list_output_max
                    else:
                        self.list_selected_offset = 0
                        
                elif self.layout_index == 1:
                    if event.key == K_ESCAPE or event.key == K_BACKSPACE or event.key == K_SPACE:
                        self.layout_index = 0
                    elif event.key == K_UP:
                        if self.memo_line_offset > 0:
                            self.memo_line_offset -= 1
                    elif event.key == K_DOWN:
                        if self.memo_line_offset < self.memo_lines_max - self.memo_lines_ouput_max:
                            self.memo_line_offset += 1
                    
                    
    def update_screen(self):
        self.screen.fill((0, 0, 0))
        if self.layout_index == 0:
            self.draw_layout_list()
            self.draw_button(320, 430, 'Btn 1 (L)', self.btn1_active)
            self.draw_button(430, 430, 'Btn 2 (R)', self.btn2_active)
            self.draw_progressbar(8, 440, 300, 20, self.progressbar_value)
        elif self.layout_index == 1:
            self.draw_layout_memo()
        
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
            
            # Items
            x = 8
            y = self.font_size * (i - self.list_selected_offset + 1) + 8
            width = self.app_width - 16
            height = self.font_size
            pygame.draw.rect(self.screen, item_background_color, (x, y, width, height - 1), 0)
            self.draw_text(self.font, item_font_color, x + 2, y + 4, 'left', self.cut_str(line, 70))
            
            if i == 0:
                self.draw_text(self.font, item_font_color, self.app_width - 80, y + 4, 'center', self.item1_turn_status)
            
    def draw_layout_memo(self):
        self.draw_text(self.font, self.white, 8, 8, 'left', 'Display: ' + self.list_selected_item)
        lines = self.add_line_breaks(self.memo, 46).split('\n')
        self.memo_lines_max = len(lines)
        
        # Scroll
        if self.memo_lines_max > self.memo_lines_ouput_max:
            scroll_percent = self.memo_line_offset * 100 // (self.memo_lines_max - self.memo_lines_ouput_max)
        else:
            scroll_percent = -1
        self.draw_scrollbox(self.app_width - 8, 30, 6, scroll_percent)
        
        self.draw_text(self.font, self.gray, 620, 455, 'right', str(self.memo_line_offset * 100 // (self.memo_lines_max - self.memo_lines_ouput_max)) + '%')
        pygame.draw.rect(self.screen, self.memo_background_color, (9, 30, self.app_width - 24, self.app_height - 60), 0)
        
        # Output lines of text
        for i, line in enumerate(lines):
            if i < self.memo_line_offset:
                continue
            if i - self.memo_line_offset >= self.memo_lines_ouput_max:
                continue
            self.draw_text(self.font, self.white, 18, self.font_size * (i - self.memo_line_offset) + 40, 'left', line)
        
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
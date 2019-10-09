import pygame
from button import Button
from settings import Settings
import sys
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
moon_glow = (235,245,255)



class StartScreen:
    def __init__(self, ai_settings, screen):
        self.ai_settings = ai_settings
        self.screen = screen

        self.make_button()
        self.title_card()
        self.alien_score()
        self.start = True

        self.music = 'sounds/start.mp3'

    def play_music(self):
        pygame.mixer.music.load(self.music)
        pygame.mixer.music.play(-1, 0.0)

    @staticmethod
    def stop_music(self):
        pygame.mixer.music.stop()

    def make_button(self):
        self.play_button = Button(self.ai_settings, self.screen, "Play", self.ai_settings.screen_width/2 -200, self.ai_settings.screen_height - 50)
        self.high_score_button = Button(self.ai_settings, self.screen, "High Score", self.ai_settings.screen_width/2 + 200, self.ai_settings.screen_height - 50)

    def title_card(self):
        self.title_font = pygame.font.Font('fonts/Wingko.ttf', 70)
        self.space_message = self.title_font.render('Space', True, RED)
        self.space_message_rect = self.space_message.get_rect()
        self.space_message_rect.centerx = self.ai_settings.screen_width/2
        self.space_message_rect.centery = 50

        self.invader_message = self.title_font.render('Invaders', True, BLUE)
        self.invader_message_rect = self.invader_message.get_rect()
        self.invader_message_rect.centerx = self.ai_settings.screen_width/2
        self.invader_message_rect.centery = self.space_message_rect.centery + 100

    def alien_score(self):
        self.alien_score_font = pygame.font.SysFont('comicsansms', 50)
        self.alien_score_info = []
        self.alien_score_rect = []
        for x in range(4):
            num = (2**x) * 10
            message = "= {} points".format(num)
            if x == 3:
                message = '= ??? points'
            self.alien_score_info.append(self.alien_score_font.render(message, True, RED))
            self.alien_score_rect.append(self.alien_score_info[x].get_rect())
            self.alien_score_rect[x].centerx = self.ai_settings.screen_width/2 + 50
            self.alien_score_rect[x].centery = self.ai_settings.screen_height/2 -100 + (x * 100)

        self.alien_images = []
        self.alien_images_rect = []
        for x in range(4):
            self.alien_images.append(pygame.image.load('images/alien-{}.png'.format(x+1)))
            self.alien_images[x] = pygame.transform.scale(self.alien_images[x], (100, 100))
            self.alien_images_rect.append(self.alien_images[x].get_rect())
            self.alien_images_rect[x].centery = self.alien_score_rect[x].centery
            self.alien_images_rect[x].centerx = self.alien_score_rect[x].centerx - 150

    def draw(self):
        self.screen.fill((75, 50, 50))

        for i in range(4):
            self.screen.blit(self.alien_images[i], self.alien_images_rect[i])
            self.screen.blit(self.alien_score_info[i], self.alien_score_rect[i])

        self.screen.blit(self.space_message, self.space_message_rect)
        self.screen.blit(self.invader_message, self.invader_message_rect)

        self.play_button.draw_button()
        self.high_score_button.draw_button()

    def check_play_button(self, _mouse_x, _mouse_y):
        return self.play_button.rect.collidepoint(_mouse_x, _mouse_y)

    def check_high_score_button(self, _mouse_x, _mouse_y):
        return self.high_score_button.rect.collidepoint(_mouse_x, _mouse_y)


if __name__ == '__main__':
    pygame.init()
    settings = Settings()
    _screen = pygame.display.set_mode((settings.screen_width,
                                      settings.screen_height))
    start_screen = StartScreen(settings, _screen)
    clock = pygame.time.Clock()
    start, play, high_score = True, False, False
    while start or high_score:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if start_screen.check_play_button(mouse_x, mouse_y):
                    start, high_score = False, False
                    break
                if start_screen.check_high_score_button(mouse_x, mouse_y):
                    start, high_score = False, True

        if start:
            start_screen.draw()
        else:
            pass

        pygame.display.update()
        clock.tick(150)
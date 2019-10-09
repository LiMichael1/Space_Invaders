import pygame
from button import Button


class GameOver(pygame.sprite.Sprite):
    def __init__(self, ai_settings, screen):
        super().__init__()

        self.ai_settings = ai_settings
        self.screen = screen
        self.font = pygame.font.Font('fonts/Wingko.ttf', 70)
        self.play_button = Button(self.ai_settings, self.screen, 'Play Again',
                                  self.ai_settings.screen_width/2, self.ai_settings.screen_height/2)
        self.quit_button = Button(self.ai_settings, self.screen, 'Quit',
                                  self.ai_settings.screen_width/2, self.ai_settings.screen_height/2 + 100)

        self.game_over_message = self.font.render('Game Over', True, (255, 0, 0))
        self.game_over_message_rect = self.game_over_message.get_rect()
        self.game_over_message_rect.centerx = self.screen.get_rect().centerx
        self.game_over_message_rect.centery = self.screen.get_rect().centery/2

        self.image = pygame.Surface([800, 800])
        self.image.fill((0, 0, 255))
        self.image_rect = self.image.get_rect()
        self.image_rect.centerx = self.screen.get_rect().centerx
        self.image_rect.centery = self.screen.get_rect().centery

    def draw(self):

        self.screen.blit(self.image, self.image_rect)
        self.play_button.draw_button()
        self.quit_button.draw_button()
        self.screen.blit(self.game_over_message, self.game_over_message_rect)

    def check_play_button(self, _mouse_x, _mouse_y):
        return self.play_button.rect.collidepoint(_mouse_x, _mouse_y)

    def check_quit_button(self, _mouse_x, _mouse_y):
        return self.quit_button.rect.collidepoint(_mouse_x, _mouse_y)


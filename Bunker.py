import pygame
import PIL


class Bunker:
    image = pygame.image.load('images/bunker.png')
    image = pygame.transform.scale(image, ( 100, 100))

    def __init__(self, ai_settings, screen, centerx, centery):
        self.ai_settings = ai_settings
        self.screen = screen
        self.image_rect = self.image.get_rect()
        self.image_rect.centerx = centerx
        self.image_rect.centery = centery

    def draw(self):
        self.screen.blit(self.image, self.image_rect)

    def hit(self):
        pass


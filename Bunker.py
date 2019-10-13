import pygame
import PIL


class Bunker(pygame.sprite.Sprite):
    image = pygame.image.load('images/bunker.png')
    image = pygame.transform.scale(image, ( 100, 100))

    def __init__(self, ai_settings, screen, centerx, centery):
        super().__init__()
        self.ai_settings = ai_settings
        self.screen = screen
        self.rect = self.image.get_rect()
        self.rect.centerx = centerx
        self.rect.centery = centery

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def hit(self):
        pass


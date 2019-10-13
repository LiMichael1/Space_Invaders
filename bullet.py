import pygame
from pygame.sprite import Sprite



class Bullet(Sprite):
    """ A class to manaage bullets fired from the ship"""

    def __init__(self, ai_settings, screen, ship, enemy=False):
        super(Bullet, self).__init__()
        self.screen = screen

        self.image = pygame.image.load('images/laser.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (ai_settings.bullet_width+30, ai_settings.bullet_height+30))
        # Create a bullet rect at (0, 0) and then set correct position
        self.rect = self.image.get_rect()

        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # Store the bullet's position as a decimal value
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor
        self.enemy = enemy

    def update(self):
        """Move the bullet up the screen"""
        # Update the decimal position of the bullet
        if self.enemy:
            self.y += self.speed_factor
        else:
            self.y -= self.speed_factor
        # Update the rect position
        self.rect.y = self.y

    def draw_bullets(self):
        """Draw the bullet to screen"""
        self.screen.blit(self.image, self.rect)
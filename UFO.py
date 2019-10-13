from alien import Alien
import pygame
from timer import Timer
from SpriteSheet import SpriteSheet
import random


class UFO(Alien):
    sprite_sheet = SpriteSheet('images/UFO.png')
    image1 = sprite_sheet.image_at((0, 0, 64, 64))
    image2 = sprite_sheet.image_at((0, 64, 64, 64))
    frames = [image1, image2]

    def __init__(self, ai_settings, screen):
        super().__init__(ai_settings=ai_settings, screen=screen)
        self.reset()
        self.alive = True
        for x in UFO.frames:
            x = pygame.transform.scale(x, (48, 48)).convert_alpha()

    timer = Timer(frames=frames)

    def reset(self):
        self.rect.centery = 50
        self.rect.centerx = 0
        self.alive = True

    def dead(self):
        self.alive = False

    def imagerect(self):
        return self.timer.imagerect()

    def update(self):
        """Move the alien right or left"""
        self.x += ((self.ai_settings.alien_speed_factor + random.randint(0, 3)) *
                   self.ai_settings.UFO_direction)
        self.rect.x = self.x


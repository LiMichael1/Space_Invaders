from alien import Alien
import pygame
from SpriteSheet import SpriteSheet
from timer import Timer


class Alien3(Alien):
    sprite_sheet = SpriteSheet('images/shark.png')
    width = sprite_sheet.width()
    height = sprite_sheet.height()
    frames = []
    for i in range(2):
        frames.append(sprite_sheet.image_at((0, int(i * height / 2), width, int(height / 2))))

    for x in frames:
        x = pygame.transform.scale(x, (48, 48))

    timer = Timer(frames=frames)

    def __init__(self, ai_settings, screen):
        super().__init__(ai_settings=ai_settings, screen=screen)

    def imagerect(self):
        return Alien3.timer.imagerect()
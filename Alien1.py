from alien import Alien
import pygame
from timer import Timer
from SpriteSheet import SpriteSheet


class Alien1(Alien):
    sprite_sheet = SpriteSheet('images/Alien.png')
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
        return Alien1.timer.imagerect()







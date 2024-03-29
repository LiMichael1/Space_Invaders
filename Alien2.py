from alien import Alien
import pygame
from timer import Timer
from SpriteSheet import SpriteSheet
from settings import Settings
import sys


class Alien2(Alien):
    sprite_sheet = SpriteSheet('images/Alien_Squid.png')
    width = sprite_sheet.width()
    height = sprite_sheet.height()
    frames = []
    for i in range(2):
        frames.append(sprite_sheet.image_at((0, int(i * height / 2), width, int(height / 2))))
    for t in frames:
        t = pygame.transform.scale(t, (48, 48))

    timer = Timer(frames=frames)

    def __init__(self, ai_settings, screen):
        super().__init__(ai_settings=ai_settings, screen=screen)

    def imagerect(self):
        return Alien2.timer.imagerect()





if __name__ == '__main__':
    pygame.init()

    settings = Settings()
    screen = pygame.display.set_mode((settings.screen_width,
                                      settings.screen_height))

    clock = pygame.time.Clock()
    alien = Alien2(settings, screen)
    while True:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()


        alien.explode()

        pygame.display.update()
        clock.tick(50)
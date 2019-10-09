import pygame
from pygame.sprite import Sprite
from SpriteSheet import SpriteSheet
from timer import Timer


class Explosion(Sprite):
    explosion_sheet = SpriteSheet('images/Explosion.png')
    explosion_width = explosion_sheet.width()
    explosion_height = explosion_sheet.height()
    explosion_frames = []
    for i in range(2):
        for j in range(2):
            explosion_frames.append(explosion_sheet.image_at
                                    ((int(j * explosion_width / 2), int(i * explosion_height / 2),
                                      explosion_width / 2, explosion_height / 2)))
    for j in explosion_frames:
        j = pygame.transform.scale(j, (48, 48))

    def __init__(self, screen, alien):
        super().__init__()
        self.rect = self.j[0].get_rect(topleft=(alien.rect.x, alien.rect.y))
        self.screen = screen

    def explode(self):
        self.screen.blit(Explosion.explosion_timer.imagerect(), self.rect)
        self.kill()

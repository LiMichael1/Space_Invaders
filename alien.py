import pygame
from pygame.sprite import Sprite
from SpriteSheet import SpriteSheet
from timer import Timer

class Alien(Sprite):
    """A class to represent a single aline in the fleet"""
    frames = []
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

    explosion_timer = Timer(frames=explosion_frames, wait=200, looponce=True)

    def __init__(self, ai_settings, screen):
        """ Initialize the alien and set its starting position"""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # load the alien image and set its rect attribute
        # self.image = pygame.image.load('images/alien-1.png')
        self.image = self.imagerect()

        self.rect = pygame.Rect((0, 0), (48, 48))

        # Start each new aline near the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact position
        self.x = float(self.rect.x)

    def blitme(self):
        """Draw the alien at it's current location"""
        self.screen.blit(self.imagerect(), self.rect)

    def check_edges(self):
        """Return True if alien is at edge of screen"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def imagerect(self):
        raise NotImplementedError

    def update(self):
        """Move the alien right or left"""
        self.x += (self.ai_settings.alien_speed_factor *
                   self.ai_settings.fleet_direction)
        self.rect.x = self.x

    def explode(self):
        # self.image = Alien.explosion_timer.imagerect()
        self.screen.blit(Alien.explosion_timer.imagerect(), self.rect)
        pygame.display.flip()
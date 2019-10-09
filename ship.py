import pygame
from pygame.sprite import Sprite
from SpriteSheet import SpriteSheet
from timer import Timer
from settings import Settings
import sys


class Ship(Sprite):
    sprite_sheet = SpriteSheet('images/Jet.png')
    width = sprite_sheet.width()
    height = sprite_sheet.height()
    frames = []
    for i in range(3):
        for j in range(3):
            frames.append(sprite_sheet.image_at((int(j * width/3), int(i * height/3), width/3, height/3)))
    timer = Timer(frames=[frames[0], frames[1]])

    explosion = frames[2:7]
    explosion_timer = Timer(frames=explosion, looponce=True)

    def __init__(self, ai_settings, screen):
        """Initialize the ship and set its starting position"""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # load the ship image and get it's rect
        self.image = Ship.frames[0]
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # start each new ship at the bottom center of the screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # Store a decimal value for the ship's center
        self.center = float(self.rect.centerx)


        # Movement flag
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Update the ship's position based on the movment flag """
        # Update the ship's center value, not the rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.rect.centerx += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.rect.centerx -= self.ai_settings.ship_speed_factor
            # self.rect.centerx = self.center

    def blitme(self):
        """ Draw the ship at it's current location"""
        self.screen.blit(self.imagerect(), self.rect)


    def center_ship(self):
        """Center the ship on the screen"""
        self.center = self.screen_rect.centerx

    def imagerect(self):
        return Ship.timer.imagerect()

    def explode(self):
        self.screen.blit(self.explosion_timer.imagerect(), self.rect)
        pygame.display.flip()

if __name__ == '__main__':
    pygame.init()

    settings = Settings()
    screen = pygame.display.set_mode((settings.screen_width,
                                      settings.screen_height))

    clock = pygame.time.Clock()
    ship = Ship(settings, screen)
    explode = False
    while True:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.type == pygame.K_SPACE:
                    explode = True

        ship.explode()



        pygame.display.update()
        clock.tick(50)



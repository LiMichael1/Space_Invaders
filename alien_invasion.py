import sys
import pygame
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from alien import Alien
import game_functions as gf
from pygame.sprite import Group


def run_game():
    # Initialize game and create a screen object

    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width,
                                      ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # PLAY BUTTON
    play_button = Button(ai_settings, screen, "Play")

    # instance to store game statistics and create a scoreboard
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    # MAKE A SHIP
    ship = Ship(ai_settings, screen)

    # Make a group to store the bullets in
    bullets = Group()
    aliens = Group()

    # Make an alien
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # MAIN LOOP FOR THE GAME
    while True:

        gf.check_events(ai_settings, screen, stats, sb, play_button,ship,
                        aliens, bullets)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens,
                              bullets)
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens,
                             bullets)

        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens,
                         bullets, play_button)


run_game()
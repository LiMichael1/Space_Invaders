import pygame
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from Alien1 import Alien1
from Alien2 import Alien2
from Alien3 import Alien3
from UFO import UFO
from PlayScreen import PlayScreen


def run_game():
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width,
                                      ai_settings.screen_height))
    pygame.display.set_caption("Space Invaders")

    play_screen = PlayScreen(ai_settings=ai_settings, screen=screen)
    play_screen.play()

    pygame.mixer.music.stop()

run_game()
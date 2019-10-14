import sys
from time import sleep

import pygame
from bullet import Bullet
from Alien1 import Alien1
from Alien2 import Alien2
from Alien3 import Alien3
from pygame.sprite import Group
from high_score import High_Score
from game_stats import GameStats
from scoreboard import Scoreboard
from ship import Ship
from UFO import UFO
from startScreen import StartScreen
from Bunker import Bunker
from gameover import GameOver
import random

clock = pygame.time.Clock()


class PlayScreen:
    def __init__(self, ai_settings, screen):

        self.ai_settings = ai_settings
        self.screen = screen

        self.display_start = True
        self.display_high_score = False
        self.start_screen = StartScreen(ai_settings=ai_settings, screen=screen)
        self.stats = GameStats(ai_settings=self.ai_settings)
        self.sb = Scoreboard(ai_settings=self.ai_settings, screen=self.screen, stats=self.stats)
        self.ship = Ship(ai_settings=self.ai_settings, screen=self.screen)

        self.high_score = High_Score(self.ai_settings, self.screen)
        self.gameover = GameOver(self.ai_settings, self.screen)
        self.quit = False

        self.alien1 = Alien1(ai_settings=self.ai_settings, screen=self.screen)
        self.alien2 = Alien2(ai_settings=self.ai_settings, screen=self.screen)
        self.alien3 = Alien3(ai_settings=self.ai_settings, screen=self.screen)

        self.aliens = [self.alien1, self.alien2, self.alien3]

        self.UFO = UFO(ai_settings=self.ai_settings, screen=self.screen)

        self.faster = False

        self.bullets = Group()
        self.enemy_bullets = Group()
        self.alien_group = Group()

        self.play_music = 'sounds/play.mp3'
        self.play_music_faster = 'sounds/play-faster.mp3'
        self.missile_sound = pygame.mixer.Sound('sounds/missile.wav')

        self.bunker = Group()
        self.create_bunker()

    def create_bunker(self):
        for x in range(3):
            bunk = Bunker(ai_settings=self.ai_settings, screen=self.screen,
                          centerx= x * 400 + 200, centery=self.ai_settings.screen_height - 100)
            self.bunker.add(bunk)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self.check_keydown_events(event)

            elif event.type == pygame.KEYUP:
                self.check_keyup_events(event)

    def check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self.fire_bullet()
        elif event.key == pygame.K_q:
            sys.exit()

    def new_game(self):
        self.ai_settings.initialize_dynamic_settings()

        pygame.mouse.set_visible(False)

        self.stats.reset_stats()
        self.stats.game_active = True

        self.sb.prep_score()
        self.sb.prep_ships()

        self.alien_group.empty()
        self.bullets.empty()
        self.enemy_bullets.empty()

        # create fleet
        self.create_fleet()
        self.create_bunker()

        self.ship.center_ship()

    def fire_bullet(self):
        if len(self.bullets) < self.ai_settings.bullets_allowed:
            new_bullet = Bullet(ai_settings=self.ai_settings, screen=self.screen, ship=self.ship)
            self.bullets.add(new_bullet)
            self.missile_sound.play()

    def fire_enemy_bullet(self):
        if random.random() < self.ai_settings.probability_to_fire:
            if len(self.enemy_bullets) < self.ai_settings.enemy_bullets_allowed:
                alien = random.choice(list(self.alien_group.spritedict.keys()))
                new_bullet = Bullet(ai_settings=self.ai_settings, screen=self.screen, ship=alien, enemy=True)
                self.enemy_bullets.add(new_bullet)
                self.missile_sound.play()


    def get_number_aliens_x(self):
        alien_width = self.aliens[0].rect.width
        available_space_x = self.ai_settings.screen_width - (2 * alien_width)
        number_aliens_x = int(available_space_x / (2 * alien_width))
        return number_aliens_x

    def get_number_rows(self):
        alien_height = self.aliens[0].rect.height
        available_space_y = (self.ai_settings.screen_height -
                             (3 * alien_height) - self.ship.rect.height)
        number_rows = int(available_space_y / (2 * alien_height))
        return number_rows

    def create_alien(self, which_alien, row_number, alien_number):
        one_alien = None
        if which_alien == 0:
            one_alien = Alien1(ai_settings=self.ai_settings, screen=self.screen)
        elif which_alien == 1:
            one_alien = Alien2(ai_settings=self.ai_settings, screen=self.screen)
        elif which_alien == 2:
            one_alien = Alien3(ai_settings=self.ai_settings, screen=self.screen)
        alien_width = one_alien.rect.width
        one_alien.x = alien_width + 2 * alien_width * alien_number
        one_alien.rect.x = one_alien.x
        one_alien.rect.y = one_alien.rect.height + 2 * one_alien.rect.height * row_number
        self.alien_group.add(one_alien)

    def create_fleet(self):
        rows = self.get_number_rows()
        aliens_per_row = self.get_number_aliens_x()
        for row_number in range(rows):
            which_alien = int(row_number / 2)
            for alien_number in range(aliens_per_row):
                self.create_alien(which_alien=which_alien, row_number=row_number, alien_number=alien_number)

    def check_bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.alien_group, True, True)

        pygame.sprite.groupcollide(self.alien_group, self.bunker, False, True)

        if self.UFO.alive:
            if pygame.sprite.spritecollideany(self.UFO, self.bullets):
                self.UFO.explode()
                self.UFO.dead()
                self.stats.score += self.ai_settings.ufo_points
                self.sb.prep_score()

        if collisions:
            for aliens in collisions.values():
                for alien in aliens:
                    for x in range(len(self.aliens)):
                        if type(alien) == type(self.aliens[x]):
                            self.stats.score += self.ai_settings.alien_points[x]
                            self.sb.prep_score()
                    alien.explode()
                    sleep(0.05)
                    alien.explosion_timer.reset()
                # needs to update settings for alien points

        if len(self.alien_group) < 11 and not self.faster:
            self.play_game_music(faster=True)

        if len(self.alien_group) == 0 and not self.UFO.alive:
            self.bullets.empty()
            self.ai_settings.increase_speed()

            self.stats.level += 1
            self.sb.prep_level()

            self.create_fleet()
            self.UFO.reset()

            self.play_game_music(faster=False)

        bunker_collision= pygame.sprite.groupcollide(groupa=self.bunker, groupb=self.enemy_bullets,
                                                     dokilla=False, dokillb=True,
                                                     collided=pygame.sprite.collide_rect_ratio(2))




    def ship_hit(self):
        self.stats.ships_left -= 1
        print(self.stats.ships_left)
        if self.stats.ships_left > 0:
            # Update the scoreboard
            self.sb.prep_ships()

            # Empty list of aliens and bullets
            self.alien_group.empty()
            self.bullets.empty()
            self.enemy_bullets.empty()

            # create_fleet
            self.create_fleet()
            self.ship.center_ship()
            self.create_bunker()

            # Pause
            sleep(0.5)

        else:
            for i in range(6):
                self.ship.explode()
                sleep(0.3)
            self.ship.explosion_timer.reset()
            self.stats.game_active = False
            pygame.mouse.set_visible(True)
            self.high_score.update_score(self.stats.score)

    def update_screen(self):
        self.screen.fill(self.ai_settings.bg_color)
        self.bullets.draw(self.screen)
        self.enemy_bullets.draw(self.screen)

        self.ship.blitme()
        for alien in self.alien_group:
            alien.blitme()

        if self.UFO.alive:
            self.UFO.blitme()

        for bunker in self.bunker:
            bunker.draw()

        self.sb.show_score()

        pygame.display.flip()

    def start_screen_play(self):
        self.start_screen.play_music()
        while self.display_start:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit()
                elif e.type == pygame.MOUSEBUTTONDOWN:
                    _mouse_x, _mouse_y = pygame.mouse.get_pos()
                    if self.start_screen.check_play_button(_mouse_x, _mouse_y):
                        self.display_start = False
                        continue
                    if self.start_screen.check_high_score_button(_mouse_x, _mouse_y):
                        self.display_high_score = True

                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_SPACE:
                        self.display_high_score = False
            if self.display_high_score:
                self.high_score.draw()
            else:
                self.start_screen.draw()

            pygame.display.flip()

        pygame.mixer.music.stop()

    def gameOver_play(self):
        self.gameover.draw()
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN:
                if e.type == pygame.QUIT:
                    sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                _mouse_x, _mouse_y = pygame.mouse.get_pos()
                if self.gameover.check_play_button(_mouse_x=_mouse_x, _mouse_y=_mouse_y):
                    self.new_game()
                    self.stats.game_active = True
                elif self.gameover.check_quit_button(_mouse_x=_mouse_x, _mouse_y=_mouse_y):
                    self.quit = True

    def play_game_music(self, faster):
        pygame.mixer.music.stop()
        if faster:
            pygame.mixer.music.load(self.play_music_faster)
            self.faster = True
        else:
            pygame.mixer.music.load(self.play_music)
            self.faster = False
        pygame.mixer.music.play(-1, 0.0)

    def update_bullets(self):
        self.bullets.update()
        self.enemy_bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        for bullet in self.enemy_bullets.copy():
            if bullet.rect.top >= self.ai_settings.screen_height:
                self.enemy_bullets.remove(bullet)

        self.fire_enemy_bullet()

        if pygame.sprite.spritecollideany(self.ship, self.enemy_bullets):
            self.ship_hit()
        self.check_bullet_alien_collisions()

    def change_fleet_direction(self):
        for alien in self.alien_group:
            alien.rect.y += self.ai_settings.fleet_drop_speed
        self.ai_settings.fleet_direction *= -1

    def check_fleet_edges(self):
        for alien in self.alien_group:
            if alien.check_edges():
                self.change_fleet_direction()
                break

    def check_aliens_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.alien_group:
            if alien.rect.bottom >= screen_rect.bottom:
                self.ship_hit()
                break

    def update_aliens(self):
        self.check_fleet_edges()
        self.alien_group.update()
        if pygame.sprite.spritecollideany(self.ship, self.alien_group):
            self.ship_hit()
        if self.UFO.alive:
            self.update_UFO()
        self.check_aliens_bottom()

    def update_UFO(self):
        if self.UFO.check_edges():
            self.ai_settings.UFO_direction *= -1
        self.UFO.update()

    def play(self):
        self.start_screen_play()

        self.new_game()
        self.play_game_music(faster=False)
        while not self.quit:
            if self.stats.game_active:
                self.check_events()
                self.ship.update()
                self.update_bullets()
                self.update_aliens()
                self.update_screen()

            else:
                self.gameOver_play()
                pygame.display.flip()

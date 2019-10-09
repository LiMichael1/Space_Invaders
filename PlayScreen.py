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

        self.alien1 = Alien1(ai_settings=self.ai_settings, screen=self.screen)
        self.alien2 = Alien2(ai_settings=self.ai_settings, screen=self.screen)
        self.alien3 = Alien3(ai_settings=self.ai_settings, screen=self.screen)

        self.aliens = [self.alien1, self.alien2, self.alien3]

        self.UFO = UFO(ai_settings=self.ai_settings, screen=self.screen)

        self.bullets = Group()
        self.alien1_group = Group()
        self.alien2_group = Group()
        self.alien3_group = Group()
        self.alien_group = [self.alien1_group, self.alien2_group, self.alien3_group]

        self.play_music = 'sounds/play.mp3'
        self.missile_sound = pygame.mixer.Sound('sounds/missile.wav')

        self.bunker = []
        for x in range(3):
            self.bunker.append(Bunker(ai_settings=ai_settings, screen=screen,
                                      centerx=x * 400 + 200, centery=self.ai_settings.screen_height - 100))

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

        for alien_group in self.alien_group:
            alien_group.empty()
        self.bullets.empty()

        # create fleet
        self.create_fleet()

        self.ship.center_ship()

    def fire_bullet(self):
        if len(self.bullets) < self.ai_settings.bullets_allowed:
            new_bullet = Bullet(ai_settings=self.ai_settings, screen=self.screen, ship=self.ship)
            self.bullets.add(new_bullet)
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
        self.alien_group[which_alien].add(one_alien)

    def create_fleet(self):
        rows = self.get_number_rows()
        aliens_per_row = self.get_number_aliens_x()
        for row_number in range(rows):
            which_alien = int(row_number / 2)
            for alien_number in range(aliens_per_row):
                self.create_alien(which_alien=which_alien, row_number=row_number, alien_number=alien_number)

    def check_bullet_alien_collisions(self):

        collisions = []

        for alien_group in self.alien_group:
            collisions.append(pygame.sprite.groupcollide(self.bullets, alien_group, True, False))

        if pygame.sprite.spritecollideany(self.UFO, self.bullets):
            self.UFO.explode()
            self.UFO.kill()

        for i in range(len(collisions)):
            for aliens in collisions[i].values():
                for alien in aliens:
                    alien.explode()
                    alien.kill()
                    # needs to update settings for alien points
                    self.stats.score += self.ai_settings.alien_points * len(aliens)
                    self.sb.prep_score()

        if len(self.alien_group[0]) == 0 and len(self.alien_group[1]) == 0 and len(self.alien_group[2]) == 0:
            self.bullets.empty()
            self.ai_settings.increase_speed()

            self.stats.level += 1
            self.sb.prep_level()

            self.create_fleet()



    def ship_hit(self):
        self.stats.ships_left -= 1

        if self.stats.ships_left > 0:
            # Update the scoreboard
            self.sb.prep_ships()

            # Empty list of aliens and bullets
            for alien_group in self.alien_group:
                alien_group.empty()
            self.bullets.empty()

            # create_fleet
            self.create_fleet()
            self.ship.center_ship()

            # Pause
            sleep(0.5)

        else:
            print('lost')
            self.stats.game_active = False
            pygame.mouse.set_visible(True)
            self.high_score.update_score(self.stats.score)

    def update_screen(self):
        self.screen.fill(self.ai_settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullets()

        self.ship.blitme()
        for alien_group in self.alien_group:
            for alien in alien_group:
                alien.blitme()

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

    def play(self):
        self.start_screen_play()

        self.new_game()
        self.play_game_music()
        while self.stats.game_active:
            self.check_events()

            self.ship.update()
            self.update_bullets()
            self.update_aliens()

            self.update_screen()

    # @staticmethod
    # def stop_music(self):
    #     pygame.mixer.music.stop()

    def play_game_music(self):
        pygame.mixer.music.load(self.play_music)
        pygame.mixer.music.play(-1, 0.0)

    def update_bullets(self):
        self.bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self.check_bullet_alien_collisions()

    def check_fleet_edges(self):
        for alien_group in self.alien_group:
            for alien in alien_group.sprites():
                if alien.check_edges():
                    self.change_fleet_direction()
                    break

    def change_fleet_direction(self):
        for alien_group in self.alien_group:
            for alien in alien_group:
                alien.rect.y += self.ai_settings.fleet_drop_speed
        self.ai_settings.fleet_direction *= -1

    def check_aliens_bottom(self):

        screen_rect = self.screen.get_rect()
        for alien_group in self.alien_group:
            for alien in alien_group:
                if alien.rect.bottom >= screen_rect.bottom:
                    self.ship_hit()
                    break

    def update_aliens(self):
        self.check_fleet_edges()
        for alien_group in self.alien_group:
            alien_group.update()
            if pygame.sprite.spritecollideany(self.ship, alien_group):
                self.ship.explode()
                self.ship_hit()
        self.update_UFO()
        self.check_aliens_bottom()

    def update_UFO(self):
        if self.UFO.check_edges():
            self.ai_settings.UFO_direction *= -1
        self.UFO.update()
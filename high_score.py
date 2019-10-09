import pygame
from settings import Settings
import sys
RED = (255, 0, 0)


class High_Score:
    def __init__(self, ai_settings, screen):

        self.font = pygame.font.Font('fonts/Wingko.ttf', 30)
        self.ai_settings = ai_settings
        self.screen = screen


        self.title_card()
        self.read_txt()
        self.update()
        self.write_txt()

    def title_card(self):
        self.title = self.font.render('High Scores', True, RED)
        self.title_rect = self.title.get_rect()
        self.title_rect.centerx = self.screen.get_rect().centerx
        self.title_rect.centery = 30

    def read_txt(self):
        f = open('high_score.txt', 'a+')
        self.read = f.read()
        self.scores = [int(n) for n in self.read.split()]
        while len(self.scores) < 10:
            self.scores.append(0)
        f.close()

    def write_txt(self):
        txt = open('high_score.txt', 'w')
        for score in self.scores:
            txt.write(str(score) + '\n')
        txt.close()

    def update(self):
        self.scores_message = []
        self.scores_rect = []
        for i in range(len(self.scores)):
            self.scores_message.append(self.font.render(str(i+1) + '. ' + str(self.scores[i]) + ' points', True, RED))
            self.scores_rect.append(self.scores_message[i].get_rect())
            self.scores_rect[i].centerx = self.screen.get_rect().centerx
            self.scores_rect[i].centery = (60 * i) + 100

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.title, self.title_rect)
        for i in range(len(self.scores_message)):
            self.screen.blit(self.scores_message[i], self.scores_rect[i])

    def update_score(self, new_score):
        for i in range(len(self.scores)):
            if new_score > self.scores[i]:
                self.scores.insert(i, new_score)
                del self.scores[-1]
                self.update()
                self.write_txt()
                break


if __name__ == '__main__':
    pygame.init()
    settings = Settings()
    _screen = pygame.display.set_mode((settings.screen_width,
                                       settings.screen_height))

    high_scores = High_Score(settings, _screen)
    clock = pygame.time.Clock()
    #high_scores.update_score(21300)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()

        high_scores.draw()
        pygame.display.update()
        clock.tick(150)


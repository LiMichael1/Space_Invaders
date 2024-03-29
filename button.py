import pygame.ftfont

class Button:
    def __init__(self, ai_settings, screen, msg, centerx=0, centery=0):
        """Initialize button attributes"""
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Set the dimensions and properties of the button
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont("comicsansms", 48)

        # Build the button's rect object and center it

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        if centery !=0:
            self.rect.centerx = centerx
            self.rect.centery = centery
            self.button_color = (55, 141, 123)
        else:
            self.rect.center = screen.get_rect().center

        # The button message needs to be prepped only once
        self.prep_msg(msg)

    def prep_msg(self, msg):
        """ Turn the msg into a render image and center text on button"""
        self.msg_image = self.font.render(msg, True, self.text_color,
                                          self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # Draw blank button and then draw message
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
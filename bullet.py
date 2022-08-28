import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):

    def __init__(self,ai_game):
        # create a new Bullet at ships position
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.colour = self.settings.bullet_colour

        #create a bullet rect at (0,0)
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop
        self.y = float(self.rect.y)
    
    def update(self):
        # move bullet up the screen
        self.y -= self.settings.bullet_speed # update position of bullet
        self.rect.y = self.y # update rect position

    def draw_bullet(self):
        # draw bullet to screen
        pygame.draw.rect(self.screen, self.colour, self.rect)


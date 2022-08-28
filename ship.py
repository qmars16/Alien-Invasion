import pygame
 
class Ship: # a class to manage the ship.
 
    def __init__(self, ai_game): # Initialize the ship and set its starting position.
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Load the ship image and get its rect. (rectangles)
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # Start each new ship at the bottom center of the screen.
        self.x = float(self.rect.x)
        self.rect.midbottom = self.screen_rect.midbottom
        self.center_ship()
        self.moving_right = False # movement flag
        self.moving_left = False # movement flag
    
    def update(self): # updates ship movement based on the flag
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        self.rect.x = self.x 

    def blitme(self): # Initialize the ship and set its starting position.
        self.screen.blit(self.image, self.rect)
    
    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

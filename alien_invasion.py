import sys
import pygame
from time import sleep
 
from settings import Settings
from game_stats import Gamestats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion: 
    # main class to manage the game
    def __init__(self):
        pygame.init() # initializes the background settings for the game
        self.settings = Settings()
        # creates a display window for the game
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height)) 
        pygame.display.set_caption("Alien Invasion")
        self.stats = Gamestats(self)
        self.sb = Scoreboard(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        # make play button
        self.play_button = Button(self, "Play")

    def run_game(self): 
        # starts the main game loop
        while True: 
            self._check_events()
            if self.stats.game_active :
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()
            
    def _check_events(self):
         # keyboard and mouse events are handled
        for event in pygame.event.get(): # event loop
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
    
    def _check_play_button(self, mouse_pos):
        # start a new game when pressed play 
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            #reset game settings
            self.settings.initialize_dynamic_settings()
            # reset game stats
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            # get rid of remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()
            # create new fleet and center ship
            self._create_fleet()
            self.ship.center_ship()
            #hide cursor
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event): # responds to key presses
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:    
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self.firing_bullets()
    
    def _check_keyup_events(self, event): # responds to key releases
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
    
    def check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
            
    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
    
    def firing_bullets(self): # create a new bullet and add it to group
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
    
    def _update_bullets(self): # removes old bullets
        self.bullets.update() # update bullet positions
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0 :
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()
    
    def _check_bullet_alien_collisions(self): # to check bullet collisions with aliens
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
        if not self.aliens : # check if aliens group empty, respawn the fleet
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

    def _update_aliens(self): # update position of aliens
        self.check_fleet_edges() # check if fleet at edges
        self.aliens.update() 
        if pygame.sprite.spritecollideany(self.ship, self.aliens) :
            self._ship_hit() # calling ship_hit method
        self._check_aliens_bottom() # check if any aliens hit bottom
        
    def _ship_hit(self):
        if self.stats.ships_left > 0 :
            # reduce no. of ships by 1
            self.stats.ships_left -= 1
            # empty all bullets and aliens form screen
            self.bullets.empty()
            self.aliens.empty()
            # create new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()
            # pausing game for a sec
            sleep(0.5)
        else :
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _create_fleet(self): # create a fleet of aliens
        alien = Alien(self) # single alien created which is not included in the group of aliens
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width) # to find available space for horizontal space
        number_aliens_x = self.settings.screen_width // (2 * alien_width) # to find out number of aliens on screen
        ship_height = self.ship.rect.height # to find available space for vertical space
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x): # for loop for first row of aliens
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number): # create alien and put in the row
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        alien_width = alien.rect.width
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_aliens_bottom(self): 
        # check if any aliens reached bottom of the screen
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites() :
            if alien.rect.bottom >= screen_rect.bottom:
                # treat this as aliens hit ship
                self._ship_hit()
                break

    def _update_screen(self):
        self.screen.fill(self.settings.bg_colour) # fills screen with colour each pass through loop
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        # draw the score info
        self.sb.show_score()
        if not self.stats.game_active :
            self.play_button.draw_button()
        pygame.display.flip() # tells Pygame to make the recently drawn screen visible

if __name__ == '__main__':
    # make a game instance and run the game
    ai = AlienInvasion()
    ai.run_game()



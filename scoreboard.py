import pygame.font

class Scoreboard:
    # class to show scores
    def __init__(self, ai_game):
        # initilaize attributes
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        #font settings for score info
        self.text_colour = (30,30,30)
        self.font = pygame.font.SysFont(None, 40)
        # prep the score image to be drawn to screen
        self.prep_score()
        self.prep_high_score()
    
    def prep_score(self):
        # turn score into a rendered image
        score_str = str(self.stats.score) # turn numerical score into a string
        self.score_image = self.font.render(score_str, True, self.text_colour, self.settings.bg_colour)
        #display score at top right of screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20 # placing 20 pixels from right of screen
        self.score_rect.top = 20 # 20 pixels from top screen
    
    def show_score(self):
        # draw score to screen
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
    
    def prep_high_score(self):
        # turn high score into rendered image
        high_score = round(self.stats.high_score, -1)
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_colour, self.settings.bg_colour)
        # center high score at top of screen
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def check_high_score(self):
        # check to see if any new high score
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()
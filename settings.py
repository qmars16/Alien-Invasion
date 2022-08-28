class Settings: # a class to store all settings for the game
    def __init__(self): # initialize static settings
        # screen settings
        self.screen_width = 700
        self.screen_height = 670
        self.bg_colour = (230,230,230)
        # ship settings
        self.ship_limit = 3
        # bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_colour = (255,0,0)
        self.bullets_allowed = 3
        # alien settings
        self.fleet_drop_speed = 1
        # how quickly the game speeds up
        self.speedup_scale = 1.1  # 1.1 times the current speed of game
        self.score_scale = 1.5 # 1.5 times score each time speed increases
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self): # initialize settings that change throughout the game
       self.ship_speed = 0.5
       self.bullet_speed = 0.6
       self.alien_speed = 0.2
       # (1) - right side, (-1) - left side
       self.fleet_direction = 1
       # scoring
       self.alien_points = 50
    
       
    def increase_speed(self):
        #incease speed settings and point values
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
        
        
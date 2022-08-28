class Gamestats: # track statistics for the game
    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.reset_stats()
        self.game_active = False  # creating "game_active" flag
        self.high_score = 0 # high_score should never reset

    def reset_stats(self):
        self.ships_left = self.settings.ship_limit
        self.score = 0

import pygame.font

class Button:
    def __init__(self, ai_game, msg):
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        # set properties of button
        self.width, self.height = 150, 50
        self.button_colour = (0,255,0)
        self.text_colour = (255,255,255)
        self.font = pygame.font.SysFont(None, 48) # 'None' tells to use default font, 48 is size of the text
        # get rect of button and center it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        # button needs to be prepped only once
        self._prep_msg(msg)
    
    def _prep_msg(self, msg):
        # turn msg into a rendered image and center text on button
        self.msg_image = self.font.render(msg, True, self.text_colour, self.button_colour) # 'True' is the boolean value that makes the edges of the button smoother
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
    
    def draw_button(self):
        # draw blank button and draw message
        self.screen.fill(self.button_colour, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

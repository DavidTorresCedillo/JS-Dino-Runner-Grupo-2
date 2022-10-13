import pygame
from pygame.sprite import Sprite
from dino_runner.utils.constants import FONT_STYLE
from dino_runner.utils.constants import SCREEN_HEIGHT, SCREEN_WIDTH
class Score(Sprite):
    def __init__(self):
       self.score = 0

    
    def update(self,game):
       self.score += 1
       if self.score % 100 ==0:
        game.game_speed +=1

    def draw(self,screen):
        fond=pygame.font.Font(FONT_STYLE,30)
        text = fond.render(f"Score: {self.score}",True,(0,0,0))
        text_rect = text.get_rect()
        text_rect.center = (1000,50)
        screen.blit(text,text_rect)
    
    def reset_score(self):
       self.score = 0
   
    def score_end(self,screen,position_Y):
        fond = pygame.font.Font(FONT_STYLE,30)
        text = fond.render(f"Score: {self.score}",True,(0,0,0))  
        text_rect = text.get_rect()
        text_rect.center = (SCREEN_WIDTH/2,position_Y)
        screen.blit(text,text_rect)
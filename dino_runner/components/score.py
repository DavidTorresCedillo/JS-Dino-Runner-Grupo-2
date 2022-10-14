import pygame
from pygame.sprite import Sprite
from dino_runner.utils.constants import FONT_STYLE
from dino_runner.utils.constants import SCREEN_HEIGHT, SCREEN_WIDTH
from dino_runner.components.print_all import Print_All
class Score(Sprite):
    def __init__(self):
        self.score = 0
        self.fond=pygame.font.Font(FONT_STYLE,30)
        self.print_all=Print_All()
    def update(self,game):
       self.score += 1
       if self.score % 100 ==0:
        game.game_speed +=1

    def draw(self,screen):
        self.print_all.printall(screen,0,1000,50,self.fond.render(f"Score: {self.score}",True,(0,0,0)))
    
    def reset_score(self):
       self.score = 0
   
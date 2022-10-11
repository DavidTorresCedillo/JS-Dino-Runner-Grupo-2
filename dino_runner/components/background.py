from pygame.sprite import Sprite

from dino_runner.utils.constants import BACKGROUND, RUNNING


class Backgroun(Sprite):
    def __init__(self):
        self.img = BACKGROUND
        self.back = self.img.get_rect()
        self.back.x=0
        self.back.y=0
        
    
    def update(self):
        pass
    def draw(self, screen):
        screen.blit(self.img,(self.back.x,self.back.y))

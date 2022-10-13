from operator import index
from random import randint
from turtle import Screen
from .obstacle import Obstacle
from dino_runner.utils.constants import BIRD

class Bird(Obstacle):
    def __init__(self,images):
        type = 0 
        super().__init__(images,type)
        self.rect.y=randint(250,330)
        self.index=0

    def draw(self, screen):
        if self.index >=9:
            self.index = 0
        screen.blit(self.images[self.index//5],self.rect)
        self.index+=1

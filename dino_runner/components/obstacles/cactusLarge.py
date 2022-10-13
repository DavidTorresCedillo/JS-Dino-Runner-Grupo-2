from random import randint
from .obstacle import Obstacle


class CactusLarge(Obstacle):
    def __init__(self,images):
        type = randint(0,2)
        super().__init__(images,type)
        self.rect.y=300
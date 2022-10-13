import pygame
from random import randint
from dino_runner.components.obstacles.cactusLarge import CactusLarge
from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.components.obstacles.bird import Bird
from dino_runner.utils.constants import  BIRD, SMALL_CACTUS,LARGE_CACTUS

class ObstacleManager:
    def __init__(self) :
        self.obstacles= []

    def update(self,game):
        if len(self.obstacles) == 0:
            NumRandom=randint(0,2)
            if NumRandom == 0:
                self.obstacles.append(Cactus(SMALL_CACTUS))
            elif NumRandom == 1:
                self.obstacles.append(CactusLarge(LARGE_CACTUS))
            elif NumRandom == 2:
                self.obstacles.append(Bird(BIRD))
            
        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)
            if game.player.dino_rect.colliderect(obstacle.rect):
                pygame.time.delay(500)
                game.playing = False
                break
    def draw(self,screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen) 
            

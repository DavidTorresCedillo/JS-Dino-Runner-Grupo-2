from random import randint
from dino_runner.components.obstacles.cactusLarge import CactusLarge
from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.components.obstacles.bird import Bird
from dino_runner.utils.constants import  BIRD, HAMMER_TYPE, SMALL_CACTUS,LARGE_CACTUS

class ObstacleManager:
    def __init__(self) :
        self.obstacles= []

    def update(self,game_speed,player,on_death):
        has_hammer=player.type==HAMMER_TYPE
        if not has_hammer :
            if len(self.obstacles) == 0:
                NumRandom=randint(0,2)
                if NumRandom == 0:
                    self.obstacles.append(Cactus(SMALL_CACTUS))
                elif NumRandom == 1:
                    self.obstacles.append(CactusLarge(LARGE_CACTUS))
                else:
                    self.obstacles.append(Bird(BIRD))
            
            for obstacle in self.obstacles:
                obstacle.update(game_speed, self.obstacles)
                if player.dino_rect.colliderect(obstacle.rect):
                    if on_death():
                        self.obstacles.remove(obstacle)
                    break
    def draw(self,screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen) 
            
    def reset_obstacles(self):
        self.obstacles=[]

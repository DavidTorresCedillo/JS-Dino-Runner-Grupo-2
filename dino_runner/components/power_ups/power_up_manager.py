from random import randint

from dino_runner.utils.constants import SOUNDPOWERUP
from .shield import Shield
from .hammer import Hammer
import pygame


class PowerUpManager:
    def __init__(self) -> None:
        self.power_ups=[]
        self.when_appears=0
        self.soundpower=pygame.mixer.Sound(SOUNDPOWERUP)
    def generate_power_up(self,score):
        if len(self.power_ups)==0 and self.when_appears == score:
            
            aleatorio=randint(0,2)
            if aleatorio==0:
                self.when_appears += randint(200,300)

                self.power_ups.append(Shield())
            elif aleatorio==1:
                self.when_appears += randint(200,300)
                self.power_ups.append(Hammer())
            

    def update(self,game_speed,player,score):
        self.generate_power_up(score)
        for power_up in self.power_ups:
            power_up.update(game_speed,self.power_ups)
            if player.dino_rect.colliderect(power_up.rect):
                start_time=pygame.time.get_ticks()
                player.on_pick_power_up(start_time,power_up.duration, power_up.type)
                self.power_ups.remove(power_up)
                self.soundpower.play()

    def draw(self,screen):
        for power_up in self.power_ups:
            power_up.draw(screen)

    def reset_power_ups(self):
        self.power_ups=[]
        self.when_appears = randint(200,300)
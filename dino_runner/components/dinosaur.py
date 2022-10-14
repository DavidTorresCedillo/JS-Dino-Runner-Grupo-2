import pygame

from pickle import TRUE
from pygame.sprite import Sprite
from dino_runner.utils.constants import DEFAULT_TYPE, DUCKING, DUCKING_HAMMER, DUCKING_SHIELD, HAMMER_TYPE, JUMPING, JUMPING_HAMMER, JUMPING_SHIELD, RUNNING, RUNNING_HAMMER, RUNNING_SHIELD, SHIELD_TYPE

DUCK_IMG = {DEFAULT_TYPE: DUCKING, SHIELD_TYPE:DUCKING_SHIELD,HAMMER_TYPE:DUCKING_HAMMER}
JUMP_IMG = {DEFAULT_TYPE: JUMPING, SHIELD_TYPE:JUMPING_SHIELD,HAMMER_TYPE:JUMPING_HAMMER}
RUN_IMG = {DEFAULT_TYPE: RUNNING, SHIELD_TYPE:RUNNING_SHIELD,HAMMER_TYPE:RUNNING_HAMMER}

class Dinosaur(Sprite):
    Y_POS = 310
    X_POS =80
    Y_POSDUCK = 340
    X_POSDUCK =80
    JUMP_VELOCITY = 8.5
    def __init__(self):
        self.type=  DEFAULT_TYPE
        self.image = RUN_IMG[self.type][0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x=self.X_POS
        self.dino_rect.y=self.Y_POS
        self.stop_index=0
        self.jump_velocity = self.JUMP_VELOCITY
       
        self.dino_running = True
        self.dino_jumping = False
        self.dino_duck = False

        self.has_power_up = False
        self.power_up_time_up=0
    
    def update(self,user_input):
        if self.dino_running:
            self.run()
        elif self.dino_jumping:
            self.jump()
        elif self.dino_duck:
            self.duck()

        if user_input[pygame.K_UP] and not self.dino_jumping:
            self.dino_jumping= True
            self.dino_duck= False
            self.dino_running=False
            
        elif user_input[pygame.K_DOWN] and not self.dino_jumping:
            self.dino_jumping= False
            self.dino_duck= True
            self.dino_running=False
        elif not self.dino_jumping:
            self.dino_jumping= False
            self.dino_running=True
            self.dino_duck= False

        if self.stop_index >=9:
            self.stop_index=0

    def run(self):
        self.image = RUN_IMG[self.type][self.stop_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x=self.X_POS
        self.dino_rect.y=self.Y_POS
        self.stop_index += 1

    def jump(self):
        self.image = JUMP_IMG[self.type]
        self.dino_rect.y -= self.jump_velocity * 4
        self.jump_velocity -= 0.8
        if self.jump_velocity < -self.JUMP_VELOCITY:
            self.dino_jumping = False
            self.dino_rect.y = self.Y_POS
            self.jump_velocity = self.JUMP_VELOCITY
    
    def duck(self):
        self.image = DUCK_IMG[self.type][self.stop_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x=self.X_POSDUCK
        self.dino_rect.y=self.Y_POSDUCK
        self.stop_index += 1
        
    def draw(self, screen):
        screen.blit(self.image,(self.dino_rect.x,self.dino_rect.y))

    def on_pick_power_up(self,start_time,duration,type):
        self.has_power_up=True
        self.power_up_time_up = start_time + (duration*1000)
        self.type=type
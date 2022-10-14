from unittest.mock import DEFAULT
import pygame
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.power_ups.power_up_manager import PowerUpManager
from dino_runner.components.score import Score
from dino_runner.components.background import Backgroun
from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.utils.constants import BG, DEFAULT_TYPE, DINO_START,DINO_DEAD, FONT_STYLE, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, SHIELD_TYPE, TITLE, FPS


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.game_speed = 20
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.pos_center_x = SCREEN_WIDTH/2
        self.pos_center_Y = SCREEN_HEIGHT/2
        self.text=""
        self.fond = pygame.font.Font(FONT_STYLE,30)

        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        self.power_up_manager=PowerUpManager()

        self.running=False
        self.score= Score()
        self.death_count=0
    #mostrar el menu cuando el juego este parado
    def execute(self):
        self.running = True
        while self.running:
            if not self.playing:
                 self.show_menu()
        pygame.quit()

    def run(self):
        # Game loop: events - update - draw
        self.playing = True
        self.obstacle_manager.reset_obstacles()
        self.score.reset_score()
        self.reset_game_speed()
        self.power_up_manager.reset_power_ups()
       
        while self.playing:
            self.events()
            self.update()
            self.draw()
    
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False

    def update(self):
        user_input= pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manager.update(self.game_speed,self.player,self.on_death)
        self.score.update(self)
        self.power_up_manager.update(self.game_speed, self.player,self.score.score)

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.score.draw(self.screen)
        self.power_up_manager.draw(self.screen)
        self.draw_active_power_up()
        pygame.display.update()
        pygame.display.flip()
 #pitar el camino
    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed

    def show_menu(self):
        #pintar el fondo 
        self.screen.fill((56, 54, 54))
        #mostrar un texto   
        if self.death_count<=0:
            self.text = self.fond.render("Press any key to start",True,(0,0,0))  
            self.print_menu()
            type_Dino=DINO_START
        else:
            #imprimir el restart y las muertes
            self.show_menu_restart()
            type_Dino=DINO_DEAD
            self.pos_center_Y=SCREEN_HEIGHT/2
        #mostrar una imagen como logo
        dino_rect= type_Dino.get_rect()
        dino_rect.center=(self.pos_center_x,self.pos_center_Y-80)
        self.screen.blit(type_Dino,dino_rect)
        #actualizar pantalla
        pygame.display.update()
        #manejar los eventos
        self.hanle_menu_events()
    #iniciar juego presionando un tecla
    def hanle_menu_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.run()
    #contador de muertes 
    def on_death(self):
        has_shield=self.player.type==SHIELD_TYPE
        if not has_shield:
            pygame.time.delay(500)
            self.playing=False
            self.death_count+=1
        
        return #has_shield
    
    #imprimir menu de restart
    def show_menu_restart(self):
        contador=0
        txt = ["Press any key to restart",f"Death count: {self.death_count}",f"Your score: {self.score.score}"]
        while contador<len(txt):
            self.text = self.fond.render(txt[contador],True,(0,0,0)) 
            self.print_menu()
            self.pos_center_Y+=40
            contador+=1
    #pintar menu 
    def print_menu(self):
        text_rect = self.text.get_rect()
        text_rect.center = (self.pos_center_x,self.pos_center_Y)
        self.screen.blit(self.text,text_rect)  
    #resetear la velocidada del juego
    def reset_game_speed(self):
        self.game_speed = 20
    #
    def draw_active_power_up(self):
        if self.player.has_power_up:
            time_to_show=round((self.player.power_up_time_up - pygame.time.get_ticks())/1000,2)
            if time_to_show>=0:
                text = self.fond.render(f"{self.player.type.capitalize()} enable for {time_to_show} seconds",True,(0,0,0))
                text_rect = text.get_rect()
                text_rect.center = (self.pos_center_x,50)
                self.screen.blit(text,text_rect)
            else:
                self.player.has_power_up=False
                self.player.type = DEFAULT_TYPE
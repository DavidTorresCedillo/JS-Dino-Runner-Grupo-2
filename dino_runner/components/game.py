from multiprocessing.spawn import is_forking
from unittest.mock import DEFAULT
import pygame
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.power_ups.power_up_manager import PowerUpManager
from dino_runner.components.print_all import Print_All
from dino_runner.components.score import Score
from dino_runner.components.background import Backgroun
from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.utils.constants import GAME_OVER,BG, HAMMER_TYPE,SMALL_HEART,CLOUD,RESET, DEFAULT_TYPE, DINO_START,DINO_DEAD, FONT_STYLE, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, SHIELD_TYPE, SOUNDBACK, SOUNDDEATH1, SOUNDGAMEOVER, TITLE, FPS


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
        self.heart_x=5
        self.heart_y=40
        self.text=""
        self.fond = pygame.font.Font(FONT_STYLE,30)
        self.colorcode=255
        self.conta=0
        self.luz="dia"
        self.soundgameover=pygame.mixer.Sound(SOUNDGAMEOVER)
        self.sounddeath=pygame.mixer.Sound(SOUNDDEATH1)

        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        self.power_up_manager=PowerUpManager()

        self.running=False
        self.score= Score()
        self.death_count=0
        self.heart=3
        self.print_all=Print_All()

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
        self.colorcode=250
        self.conta=0
        self.luz="dia"
        self.power_up_manager.reset_power_ups()
        pygame.mixer.music.load(SOUNDBACK)
        self.sounddeath.stop()
        pygame.mixer.music.play(100)
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
        self.conta+=1
        has_hammer=self.player.type==HAMMER_TYPE
        has_shield=self.player.type==SHIELD_TYPE
        if has_hammer:
            self.screen.fill((170, 250, 247 ))
        elif has_shield:
            self.screen.fill((255, 170, 170 ))
        else:
            self.screen.fill((self.colorcode, self.colorcode, self.colorcode))
        #hacer de noche y de dia
        
        if self.conta>5 and self.luz=="dia":
                self.conta=self.conta
                self.colorcode-=1
                self.conta=0
        if self.conta>5 and self.luz=="noche":
                self.conta=self.conta
                self.colorcode+=1
                self.conta=0
        if self.colorcode==0:
            self.luz="noche"
        if self.colorcode==250:
            self.luz="dia"
            
        self.draw_background()
        self.player.draw(self.screen)
        if not has_hammer:
            self.obstacle_manager.draw(self.screen)

        self.score.draw(self.screen)
        self.power_up_manager.draw(self.screen)
        self.draw_active_power_up()
        self.hearts(50,20)
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
        
    def draw_clouds(self):
      pass
    

    def show_menu(self):
        #pintar el fondo 
        self.screen.fill((56, 54, 54))
        #mostrar un texto   
        if self.death_count<=0:
            self.print_all.printall(self.screen,0,self.pos_center_x,self.pos_center_Y,self.fond.render("Press any key to start",True,(0,0,0)))
            type_Dino=DINO_START
            self.print_all.printall(self.screen,2,self.pos_center_x,self.pos_center_Y-80,type_Dino)
        elif self.death_count==3:
            self.print_all.printall(self.screen,1,self.pos_center_x-200,self.pos_center_Y,GAME_OVER)
            self.print_all.printall(self.screen,0,self.pos_center_x,self.pos_center_Y+50,self.fond.render("Press any key to exit",True,(0,0,0)))
            pygame.mixer.music.stop()
            self.soundgameover.play()
        else:
            #imprimir el restart y las muertes
            pygame.mixer.music.stop()
            self.show_menu_restart()
            type_Dino=DINO_DEAD
            self.pos_center_Y=SCREEN_HEIGHT/2
            #mostrar una imagen como logo
            self.print_all.printall(self.screen,2,self.pos_center_x,self.pos_center_Y-80,type_Dino)
        
        
        #actualizar pantalla
        pygame.display.update()
        #manejar los eventos
        self.hanle_menu_events()
    #iniciar juego presionando un tecla
    def hanle_menu_events(self):
        for event in pygame.event.get():
            if self.death_count==3:
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                     pygame.quit()
            else:
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    self.run()
    #contador de muertes 
    def on_death(self):
        has_shield=self.player.type==SHIELD_TYPE
        if not has_shield :
            pygame.time.delay(500)
            self.playing=False
            self.death_count+=1
            self.sounddeath.play()
        return #has_shield
    
    #imprimir menu de restart
    def show_menu_restart(self):
        contador=0
        self.print_all.printall(self.screen,2,self.pos_center_x,self.pos_center_Y+30,RESET)
        self.pos_center_Y+=70
        
        txt = ["Press any key to restart",f"Death count: {self.death_count}",f"Your score: {self.score.score}"]
        while contador<len(txt):
            self.print_all.printall(self.screen,0,self.pos_center_x,self.pos_center_Y,self.fond.render(txt[contador],True,(0,0,0)))
            self.pos_center_Y+=40
            contador+=1
        self.hearts(self.pos_center_x,self.pos_center_Y)        
    #resetear la velocidada del juego
    def reset_game_speed(self):
        self.game_speed = 20

    def draw_active_power_up(self):
        if self.player.has_power_up:
            time_to_show=round((self.player.power_up_time_up - pygame.time.get_ticks())/1000,2)
            if time_to_show>=0:
                self.print_all.printall(self.screen,0,self.pos_center_x,50,self.fond.render(f"{self.player.type.capitalize()} enable for {time_to_show} seconds",True,(0,0,0)))
            else:
                self.player.has_power_up=False
                self.player.type = DEFAULT_TYPE
    #imprime las vidas
    def hearts(self,PostX,PostY):

        self.print_all.printall(self.screen,0,PostX,PostY,self.fond.render("lives",True,(200, 4, 4)))
        self.heart_y=PostY+20
        self.heart_x=PostX-45
        contador=self.death_count
        while contador<self.heart:
            self.print_all.printall(self.screen,1,self.heart_x,self.heart_y,SMALL_HEART)
            self.heart_x+=30
            contador+=1

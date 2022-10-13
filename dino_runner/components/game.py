import pygame
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.score import Score
from dino_runner.components.background import Backgroun
from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.utils.constants import BG, DINO_START, FONT_STYLE, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS


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

        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()

        self.running=False
        self.score= Score()
        self.death_count=0
    
    def execute(self):
        self.running = True
        while self.running:
            if not self.playing:
                self.show_menu()

        pygame.quit()

    def run(self):
        # Game loop: events - update - draw
        self.obstacle_manager.reset_obstacles()
        self.playing = True
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

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.score.draw(self.screen)
        pygame.display.update()
        pygame.display.flip()

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
        pos_center_x = SCREEN_WIDTH/2
        pos_center_Y = SCREEN_HEIGHT/2
        #mostrar un texto
        if self.death_count<=0:
            fond = pygame.font.Font(FONT_STYLE,30)
            text = fond.render("Press any key to start",True,(0,0,0))
            text_rect = text.get_rect()
            text_rect.center = (pos_center_x,pos_center_Y)
            self.screen.blit(text,text_rect)
        else:
            #mostrar mensaje de reinicio
            #mostrar puntaje obtenido
            #mostrarr numero de muertes 
            pass
        #mostrar una imagen como logo
        dino_rect= DINO_START.get_rect()
        dino_rect.center=(pos_center_x,pos_center_Y-80)
        self.screen.blit(DINO_START,dino_rect)
        #actualizar pantalla
        pygame.display.update()
        #manejar los eventos
        self.hanle_menu_events()

    def hanle_menu_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.run()

    def on_death(self):
        self.playing=False
        self.death_count+=1
        print("he muerte:",self.death_count)

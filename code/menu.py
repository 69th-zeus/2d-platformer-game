from settings import *
from data import *
from support import *

class Menu:
    def __init__(self, switch_stage, text, data, audio_files, bg_music):
        self.display_surface = pygame.display.get_surface()
        self.text = text
        self.switch_stage = switch_stage
        self.data = data
        self.audio_files = audio_files
        self.bg_music = bg_music
        
        self.current_scene = 'menu'
        
        self.alpha = 0
        self.trans = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.trans.fill('black')
        self.scene_change = ""
        self.background_image = import_image('graphics', 'ui', 'background')
        self.background_rect = self.background_image.get_frect(topleft = (0,0)) 
    
    def input(self):
        global VOLUME
        self.volume = VOLUME
        self.keys = pygame.key.get_just_pressed()
        if self.keys[pygame.K_RETURN]:
            self.scene_change = 'overworld'
        elif self.keys[pygame.K_LSHIFT] or self.keys[pygame.K_RSHIFT]:
            self.current_scene = 'volume' if self.current_scene =='menu' else 'menu'
        elif self.keys[pygame.K_0]:
            VOLUME = 0.0
        elif self.keys[pygame.K_1]:
            VOLUME = 0.1
        elif self.keys[pygame.K_2]:
            VOLUME = 0.2
        elif self.keys[pygame.K_3]:
            VOLUME = 0.3
        elif self.keys[pygame.K_4]:
            VOLUME = 0.4
        elif self.keys[pygame.K_5]:
            VOLUME = 0.5
        elif self.keys[pygame.K_6]:
            VOLUME = 0.6
        elif self.keys[pygame.K_7]:
            VOLUME = 0.7
        elif self.keys[pygame.K_8]:
            VOLUME = 0.8
        elif self.keys[pygame.K_9]:
            VOLUME = 0.9
            
        if self.volume != VOLUME:
            self.change_volume()
    
    def change_volume(self):
        self.bg_music.set_volume(0.5 * VOLUME)
        self.audio_files['coin'].set_volume(0.4 * VOLUME)
        self.audio_files['damage'].set_volume(0.3 * VOLUME)
        self.audio_files['jump'].set_volume(0.6 * VOLUME)
        self.audio_files['damage'].set_volume(1 * VOLUME)
        self.audio_files['pearl'].set_volume(1 * VOLUME)
        self.audio_files['start'].set_volume(1 * VOLUME)
        self.audio_files['end'].set_volume(1 * VOLUME)
        self.audio_files['end_happy'].set_volume(1 * VOLUME)
     
    def draw_scene(self):
        self.display_surface.blit(self.background_image, self.background_rect)
        if self.current_scene == 'menu':
            self.text("Welcome to Pirate", (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 300), WHITE, 'GO')
            self.text("Return to Start", (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 250), WHITE, 'WC')
            self.text("Shift change Volume of BG Music", (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 300), WHITE, 'WC')
        elif self.current_scene == 'volume':
            self.text("Press 0 - 9 to change Volume", (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 200), WHITE, 'WC')
            self.text("0 for 0%, 1 for 10% and so on", (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 250), WHITE, 'WC')
            self.text("Shift to Go Back, Return to Start Game", (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 300), WHITE, 'WC')
            
    def run(self, dt):
        self.display_surface.fill((0,0,0))
        self.text("Welcome to Pirate", (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 150), WHITE, 'GO')
        
        # for event in pygame.event.get():
        #     if event.type == pygame.KEYDOWN:
        #         if event.key == pygame.K_RETURN:
        #             self.scene_change = 'overworld'
        self.draw_scene()
        self.input()
        
        if self.scene_change == 'overworld':
            self.trans.set_alpha(self.alpha)
            self.trans_rect = self.trans.get_frect()
            self.alpha += 300 * dt
            self.display_surface.blit(self.trans, self.trans_rect)
            self.text("Loading...", (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2), WHITE, 'ST')
            if self.alpha >= TRANSITION_TIME:
                self.scene_change = ""
                self.switch_stage('overworld', self.data.current_level)
        
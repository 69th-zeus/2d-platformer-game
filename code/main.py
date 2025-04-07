from settings import *
from level import Level
from pytmx.util_pygame import load_pygame 
from os.path import join
from support import *
from data import *
from ui import UI
from overworld import *
from menu import *

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.FULLSCREEN)
        self.icon = import_image('graphics', 'ui', 'icon')
        pygame.display.set_caption("Super Pirate World")
        pygame.display.set_icon(self.icon)
        self.clock = pygame.time.Clock()
        self.import_assets()
        
        self.ui = UI(self.font1, self.ui_frames)
        self.data = Data(self.ui) # type: ignore
        self.tmx_map = {0:load_pygame(join('data','levels','0.tmx')),
                        1:load_pygame(join('data','levels','1.tmx')),
                        2:load_pygame(join('data','levels','2.tmx')),
                        3:load_pygame(join('data','levels','3.tmx')),
                        4:load_pygame(join('data','levels','4.tmx')),
                        5:load_pygame(join('data','levels','5.tmx'))}
        self.tmx_overworld = load_pygame(join('data', 'overworld', 'overworld.tmx'))
        # self.current_stage = Overworld(self.tmx_overworld, self.data, self.overworld_frames, self.switch_stage, self.change_music, self.text)
        self.current_stage = Menu(self.switch_stage, self.text, self.data, self.audio_files, self.bg_music)
        self.bg_music.play(-1)
     
    def switch_stage(self, target, unlock = 0):
        if target == 'level':
            self.current_stage = Level(self.tmx_map[self.data.current_level], self.level_frames, self.audio_files, self.data, self.switch_stage, self.change_music, self.text)
        elif target == 'menu':
            self.current_stage = Menu(self.switch_stage, self.text, self.data, self.audio_files, self.bg_music)
        else: #overworld
            if unlock > 0:
                self.data.unlocked_level = unlock
            else:
                self.data.health -= 1
            self.current_stage = Overworld(self.tmx_overworld, self.data, self.overworld_frames, self.switch_stage, self.change_music, self.text)
            
    def change_music(self, target, success = False):
        if target == 'ol':
            self.audio_files['start'].play()
        elif target == 'lo':
            if success == False:
                self.audio_files['end'].play()
            else:
                self.audio_files['end_happy'].play()
        
    def import_assets(self):
        self.level_frames = {
            'flag' : import_folder('graphics', 'level', 'flag'),
            'saw'  : import_folder('graphics','enemies', 'saw', 'animation'),
            'floor_spike' : import_folder('graphics','enemies', 'floor_spikes'),
            'palms' : import_sub_folders('graphics','level', 'palms'),
            'candle' : import_folder('graphics','level', 'candle'),
            'window' : import_folder('graphics','level', 'window'),
            'big_chain' : import_folder('graphics','level', 'big_chains'),
            'small_chain' : import_folder('graphics','level', 'small_chains'),
            'candle_light' : import_folder('graphics','level', 'candle light'),
            'player' : import_sub_folders('graphics', 'player'),
            'saw' : import_folder('graphics', 'enemies', 'saw','animation'),
            'saw_chain' : import_image('graphics', 'enemies', 'saw', 'saw_chain'),
            'helicopter' : import_folder('graphics', 'level','helicopter'),
            'boat' : import_folder('graphics', 'objects', 'boat'),
            'spike' : import_image('graphics', 'enemies', 'spike_ball', 'Spiked Ball'),
            'spike_chain' : import_image('graphics', 'enemies', 'spike_ball', 'spiked_chain'),
            'tooth' : import_folder('graphics', 'enemies','tooth','run'),
            'shell' : import_sub_folders('graphics', 'enemies','shell'),
            'pearl' : import_image('graphics', 'enemies', 'bullets', 'pearl'),
            'items' : import_sub_folders('graphics','items'),
            'particle' : import_folder('graphics','effects', 'particle'),
            'water_top' :import_folder('graphics', 'level', 'water', 'top'),
            'water_body' : import_image('graphics', 'level', 'water', 'body'),
            'bg_tiles' : import_folder_dict('graphics', 'level', 'bg', 'tiles'),
            'cloud_small' : import_folder('graphics', 'level', 'clouds', 'small'),
            'cloud_large' : import_image('graphics', 'level', 'clouds', 'large_cloud')
        }
        
        #fonts
        self.font = pygame.font.Font(join('Fonts','font_n2.ttf'))
        self.font2 = pygame.font.Font(join('Fonts','font_n2.ttf'), 80)
        self.font3 = pygame.font.Font(join('Fonts','font_n2.ttf'), 40)
        self.font1 = pygame.font.Font(join('Fonts','runescape_uf.ttf'), 40)
        
        self.ui_frames = {
            'heart': import_folder('graphics','ui', 'heart'),
            'coin' : import_image('graphics', 'ui', 'coin')
        }
        
        self.overworld_frames = {
            'palms': import_folder('graphics', 'overworld', 'palm'),
            'water': import_folder('graphics','overworld', 'water'),
            'path': import_folder_dict('graphics', 'overworld', 'path'),
            'icon': import_sub_folders('graphics', 'overworld', 'icon')
        }
        
        self.audio_files = {
            'coin': pygame.mixer.Sound(join('audio', 'coin.wav')),
            'attack': pygame.mixer.Sound(join('audio', 'attack.wav')),
            'jump': pygame.mixer.Sound(join('audio', 'jump.wav')),
            'damage': pygame.mixer.Sound(join('audio', 'damage.wav')),
            'pearl': pygame.mixer.Sound(join('audio', 'pearl.wav')),
            'start': pygame.mixer.Sound(join('audio', 'start.mp3')),
            'end': pygame.mixer.Sound(join('audio', 'end.mp3')),
            'end_happy' : pygame.mixer.Sound(join('audio', 'end_happy.mp3'))
       }
        
        self.bg_music = pygame.mixer.Sound(join('audio', 'background.mp3'))
        self.bg_music.set_volume(0.5)
        
    def text(self, text, position, color, type):
        surf = self.font.render(text, True, color)
        if type == 'fps':
            rect = surf.get_frect(topright = position )
        elif type == 'GO':
            surf = self.font2.render(text, True, color)
            rect = surf.get_frect(center = position)
        elif type == 'WC':
            surf = self.font3.render(text, True, color)
            rect = surf.get_frect(center = position)
        elif type == 'ST':
            surf = self.font2.render(text, True, color)
            rect = surf.get_frect(center = position)
        self.display_surface.blit(surf, rect)
    
    def check_game_over(self):
        if self.data.health <= 0:
            self.game_end = True
            # pygame.quit()
            # sys.exit()
    
    def run(self):
        while True:
            #delta time
            dt = self.clock.tick() / 1000
            self.fps = self.clock.get_fps()
            
            #event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_INSERT:
                        self.data.save_state()
                    if event.key == pygame.K_HOME:
                        self.data.load_state(dt)
            
            
            self.check_game_over()
            self.current_stage.run(dt)
            if type(self.current_stage) != Menu:
                self.ui.update(dt)
            self.text('fps:'+str(round(self.fps)), (WINDOW_WIDTH - 5,0), 'white','fps')
            pygame.display.update()
            
if __name__ == '__main__':            
    game = Game()
    game.run()
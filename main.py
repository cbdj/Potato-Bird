import sys
import os     
os.environ['SDL_HINT_RENDER_SCALE_QUALITY'] = '2'
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
import Settings
from pygame._sdl2.video import Window, Renderer, Texture, Image
from SpriteHandler import SpriteHandler
import pygame as pg
# import pygame.freetype as ft
import Exfont 

__version__ = "1.1.0"


class App:
    def __init__(self):
        pg.init()
        if Settings.platform=='android':
            from AdManager import AdManager 
            from Android.PlayGamesServices import PlayGamesServices
            self.ad_manager = AdManager()
            self.playgamesservices = PlayGamesServices(Settings.LEADERBOARD_ID)
        pg.mixer.init()
        self.dt = 0.0
        screen_info = pg.display.Info()
        self.window = Window(title='flap.py', size=(screen_info.current_w,screen_info.current_h), fullscreen=Settings.FULLSCREEN)
        self.window.set_icon(pg.image.load(os.path.join(Settings.ASSETS_DIR_PATH,'favicon.png')))
        self.renderer = Renderer(self.window)
        self.sprite_handler = SpriteHandler(self)
        self.renderer.scale = (self.sprite_handler.scale, self.sprite_handler.scale)
        self.clock = pg.time.Clock()
        self.font = pg.font.SysFont('Verdana', Settings.FONT_SIZE//2)
        self.fps_size = (Settings.FONT_SIZE * 13, Settings.FONT_SIZE//2)
        self.speed = Settings.SPEED
        self.running = True
        self.display_fps = False
        self.background = False
        

    def update(self):
        self.sprite_handler.update()
        self.dt = self.clock.tick(Settings.FPS) * 0.001

    def draw_fps(self):
        # img = Image(Texture.from_surface(self.renderer, Exfont.text_speech(self.font, f'{self.clock.get_fps() :.0f} FPS | {self.sprite_handler.count_sprites()} SPRITES','green', True, 1, 'black')))
        img = Image(Texture.from_surface(self.renderer, self.font.render(f'{self.clock.get_fps() :.0f} FPS | {self.sprite_handler.count_sprites()} SPRITES', True, 'green')))
        img.draw(img.get_rect(),img.get_rect())
        

    def draw(self):
        self.renderer.clear()
        self.sprite_handler.draw()
        if self.display_fps:
            self.draw_fps()
        self.renderer.present()

    def check_events(self):
        for e in pg.event.get():
            if e.type == 259 :#pg.APP_WILLENTERBACKGROUND
                print("pygame APP_WILLENTERBACKGROUND")
                self.background = True
            elif e.type == 262: #pg.APP_DIDENTERFOREGROUND
                print("pygame APP_DIDENTERFOREGROUND")
                self.background = False
            elif e.type == pg.QUIT or e.type == 257: #pg.APP_TERMINATING
                self.running = False
            elif e.type == pg.MOUSEBUTTONDOWN:
                self.sprite_handler.on_mouse_press()
            elif e.type == pg.MOUSEBUTTONUP:
                self.sprite_handler.on_mouse_unpress()
            elif e.type == pg.KEYDOWN:
                if e.key == pg.K_ESCAPE:
                    self.running = False
                if e.key == pg.K_d:
                    self.display_fps = not self.display_fps
                else:
                    self.sprite_handler.on_key_press(e.key)
            elif e.type == Settings.EVENT_DAY_NIGHT:
                if self.sprite_handler._started : 
                    self.sprite_handler.background.toggle_day_night()
                    self.speed += Settings.SPEED_INCREASE_FACTOR
                    self.sprite_handler.update_speed(self.speed)
                    self.sprite_handler.sounds['swoosh'].play()
            elif e.type == Settings.EVENT_AD:
                print('EVENT_AD')
                self.ad_manager.on_timeout()

    def run(self):
        while self.running:
            self.check_events()
            if not self.background:
                self.update()
                self.draw()
        self.sprite_handler.quit()
        pg.mixer.quit()
        pg.quit()

if __name__ == '__main__':
    app = App()
    app.run()

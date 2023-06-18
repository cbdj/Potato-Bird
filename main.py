import sys
import os     
os.environ['SDL_HINT_RENDER_SCALE_QUALITY'] = '2'
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
import Settings        
if Settings.platform=='android':
    from AdManager import AdManager 
    from Android.PlayGamesServices import PlayGamesServices
from pygame._sdl2.video import Window, Renderer, Texture, Image
from SpriteHandler import SpriteHandler
from SoundHandler import SoundHandler
from Configuration import Configuration
import pygame as pg
# import pygame.freetype as ft
import Exfont 
import random
from pygame._sdl2.video import Texture

__version__ = "1.1.6"
class App:
    def __init__(self):
        if Settings.platform=='android':
            self.ad_manager = AdManager()
            self.playgamesservices = PlayGamesServices(Settings.LEADERBOARD_ID)
        pg.init()
        pg.mixer.init()
        self.dt = 0.0
        self.speed = int(Settings.SPEED*Settings.speed_multiplier)
        screen_info = pg.display.Info()
        size=(screen_info.current_w,screen_info.current_h)
        self.window = Window(title='flap.py', size=size, fullscreen=Settings.FULLSCREEN)
        self.window.set_icon(pg.image.load(os.path.join(Settings.ASSETS_DIR_PATH,'favicon.png')))
        self.renderer = Renderer(self.window, target_texture = True)
        self.target = Texture(self.renderer, size=size, target = True)
        self.sprite_handler = SpriteHandler(self)
        self.configuration = Configuration(self, Settings.WIN_W,Settings.WIN_H)
        self.sound_handler = SoundHandler(Settings.AUDIO_DIR_PATH)
        self.clock = pg.time.Clock()
        self.font = pg.font.SysFont('Verdana', Settings.FONT_SIZE)
        self.fps_size = (Settings.FONT_SIZE * 13, Settings.FONT_SIZE)
        self.running = True
        self.display_fps = False
        self.background = False
        
        self.shake_intensity = 0
        self.shake_duration = 0

    def set_dark_mode(self,on):
        self.sprite_handler.set_dark_mode(on)

    def mute(self):
        self.sound_handler.mute()

    def unmute(self):
        self.sound_handler.unmute()

    def update(self):
        self.sprite_handler.update()
        self.dt = self.clock.tick(Settings.FPS) * 0.001

    def draw_fps(self):
        fps_texture = Texture.from_surface(self.renderer, self.font.render(f'{self.clock.get_fps() :.0f} FPS | {self.sprite_handler.count_sprites()} SPRITES', True, 'green'))
        fps_texture.draw(fps_texture.get_rect(),fps_texture.get_rect())

    def draw(self):
        self.renderer.clear()
        self.renderer.target = self.target 
        self.sprite_handler.draw()
        if self.display_fps:
            self.draw_fps()
        if self.configuration.is_enabled():
            self.configuration.draw(self.renderer)
        self.renderer.target = None
        dest_rect = self.target.get_rect()
        if self.shake_duration > 0:
            self.shake_duration -= 1
            offset_x = random.randint(-self.shake_intensity, self.shake_intensity)
            offset_y = random.randint(-self.shake_intensity, self.shake_intensity)
            dest_rect.x,  dest_rect.y= dest_rect.x + offset_x, dest_rect.y + offset_y
        self.target.draw(self.target.get_rect(), dest_rect)
        self.renderer.present()
        
        # self.screen_renderer.present()

    def check_events(self):
        super_events_types = (pg.QUIT,pg.APP_WILLENTERBACKGROUND,pg.APP_DIDENTERFOREGROUND,pg.APP_TERMINATING,Settings.EVENT_SOUND,Settings.EVENT_AD)
        events = pg.event.get(eventtype=super_events_types)
        for e in events:
            if e.type == pg.APP_WILLENTERBACKGROUND:
                self.background = True
            elif e.type == pg.APP_DIDENTERFOREGROUND:
                self.background = False
            if e.type == pg.QUIT or e.type == pg.APP_TERMINATING:
                self.running = False
            elif e.type == Settings.EVENT_SOUND:
                self.sound_handler.play(e.sound)
            elif e.type == Settings.EVENT_AD:
                print('EVENT_AD')
                self.ad_manager.on_timeout()
        events = pg.event.get(exclude=super_events_types)
        if self.configuration.is_enabled():
            self.configuration.update(events)
        else:
            for e in events:
                if e.type == pg.KEYDOWN:
                    if e.key == pg.K_ESCAPE:
                        self.running = False
                    if e.key == pg.K_d:
                        self.display_fps = not self.display_fps
                    else:
                        self.sprite_handler.on_key_press(e.key)
                elif e.type == pg.MOUSEBUTTONDOWN:
                    self.sprite_handler.on_mouse_press()
                elif e.type == pg.MOUSEBUTTONUP:
                    self.sprite_handler.on_mouse_unpress()
                elif e.type == Settings.EVENT_DAY_NIGHT:
                    if self.sprite_handler._started and not self.sprite_handler.bird.hit: 
                        self.sprite_handler.background.toggle_day_night()
                        self.speed += Settings.SPEED_INCREASE_FACTOR
                        self.sprite_handler.update_speed(self.speed)
                        pg.event.post(pg.event.Event(Settings.EVENT_SOUND, sound = 'swoosh'))
                elif e.type == Settings.SHAKE_SCREEN:
                    self.shake_intensity = e.intensity
                    self.shake_duration = e.duration

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
    App().run()

import sys
import os     
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
import Settings        
if Settings.platform=='android':
    from AdManager import AdManager 
    from Android.PlayGamesServices import PlayGamesServices
    from android import loadingscreen
from pygame._sdl2.video import Window, Renderer, Texture, Image
from SpriteHandler import SpriteHandler
from SoundHandler import SoundHandler
from Configuration import Configuration
from PlayGamesIntents import PlayGamesIntents
import pygame as pg
# import pygame.freetype as ft
import Exfont 
import random
from pygame._sdl2.video import Texture
from Sprites.Bull import Bull

__version__ = "1.4.1"
class App:
    def __init__(self):
        if Settings.platform=='android':
            self.ad_manager = AdManager()
            self.playgamesservices = PlayGamesServices()
        pg.init()
        try:
            pg.mixer.init()
        except:
            print("Couldn't init mixer : no sound")
        self.dt = 0.0
        self._speed = Settings.SPEED
        screen_info = pg.display.Info()
        size=(screen_info.current_w,screen_info.current_h)
        self.window = Window(title='flap.py', size=size, fullscreen=Settings.FULLSCREEN)
        self.window.set_icon(pg.image.load(os.path.join(Settings.ASSETS_DIR_PATH,'favicon.png')))
        self.renderer = Renderer(self.window, target_texture = True)
        self.target = Texture(self.renderer, size=size, target = True)
        self.sprite_handler = SpriteHandler(self)
        if Settings.platform=='android':
            self.play_games_intents = PlayGamesIntents(self, Settings.WIN_W,Settings.WIN_H)
        self.sound_handler = SoundHandler(Settings.AUDIO_DIR_PATH)
        self.clock = pg.time.Clock()
        self.font = pg.font.Font(None, Settings.FONT_SIZE)
        self.fps_size = (Settings.FONT_SIZE * 13, Settings.FONT_SIZE)
        self.running = True
        self.display_fps = False
        self.background = False
        self.configuration = Configuration(self, Settings.WIN_W,Settings.WIN_H)
                
        self.shake_intensity = 0
        self.shake_duration = 0
        self.sprite_handler.reset()
        if Settings.platform=='android':
            loadingscreen.hide_loading_screen()

        self._bull_gamble = Bull.gamble

    @property
    def speed(self):
        return self._speed 
    @speed.setter
    def speed(self, value):
        self._speed = value
        self.sprite_handler.update_speed(self._speed)

    def set_dark_mode(self,on):
        self.sprite_handler.set_dark_mode(on)
        
    def set_show_fps(self,on):
        self.display_fps = on

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
        # self.renderer.clear()
        self.renderer.target = self.target 
        self.renderer.clear()
        self.sprite_handler.draw()
        if self.display_fps:
            self.draw_fps()
        if self.configuration.is_enabled():
            self.configuration.draw(self.renderer)
        if Settings.platform=='android':
            if self.play_games_intents.is_enabled():
                self.play_games_intents.draw(self.renderer)
        self.renderer.target = None
        dest_rect = self.target.get_rect()
        if self.shake_duration > 0:
            self.shake_duration -= 1
            offset_x = random.randint(-self.shake_intensity, self.shake_intensity)
            offset_y = random.randint(-self.shake_intensity, self.shake_intensity)
            dest_rect.x,  dest_rect.y= dest_rect.x + offset_x, dest_rect.y + offset_y
        self.target.draw(self.target.get_rect(), dest_rect)
        self.renderer.present()
        
    def exit_prompt(self):
        # ret = messagebox('Warning','Do you really want to exit ?',warn = True, buttons = ('Yes', 'No'), return_button = 0, escape_button = 1)
        ret=0
        return ret == 0
    def check_events(self):
        super_events_types = (pg.QUIT,pg.APP_WILLENTERBACKGROUND,pg.APP_DIDENTERFOREGROUND,pg.APP_TERMINATING,Settings.EVENT_SOUND,Settings.EVENT_AD)
        events = pg.event.get(eventtype=super_events_types)
        for e in events:
            if e.type == pg.APP_WILLENTERBACKGROUND:
                self.background = True
            elif e.type == pg.APP_DIDENTERFOREGROUND:
                self.background = False
            if e.type == pg.QUIT or e.type == pg.APP_TERMINATING:
                self.running = not self.exit_prompt()
            elif e.type == Settings.EVENT_SOUND:
                self.sound_handler.play(e.sound)
            elif e.type == Settings.EVENT_AD:
                print('EVENT_AD')
                self.ad_manager.on_timeout()
        events = pg.event.get(exclude=super_events_types)
        if self.configuration.is_enabled():
            self.configuration.update(events)
        elif Settings.platform=='android' and self.play_games_intents.is_enabled():
            self.play_games_intents.update(events)
        else:
            for e in events:
                if e.type == pg.KEYDOWN:
                    if e.key == pg.K_ESCAPE or e.key == pg.K_AC_BACK:
                        self.running = not self.exit_prompt()
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
                elif e.type == Settings.INCREMENT_SPEED and self.speed !=0:
                    self.speed += e.increment
                elif e.type == Bull.event:
                    if e.phase==0:
                        if random.randint(1,self._bull_gamble) == 1:
                            pg.time.set_timer(Bull.event, 0)
                            self._bull_gamble = Bull.gamble
                            self.sprite_handler.bull.ready = True
                            self.sprite_handler.group_bonus.add(self.sprite_handler.bull)
                            # print('bull gamble succeed')
                        else:
                            self._bull_gamble -= 1
                            # print('bull gamble failed')
                    if e.phase==1:
                        pg.event.post(pg.event.Event(Settings.INCREMENT_SPEED, increment = -Bull.speed_increment))
                        pg.time.set_timer(pg.event.Event(Bull.event,phase=2), Bull.timeout//10)
                    elif e.phase==2:
                        self.sprite_handler.bird.bull = False
                        self.sprite_handler.bull.x = self.sprite_handler.bull.orig_x
                        pg.time.set_timer(pg.event.Event(Bull.event,phase=0), Bull.timeout)

    def run(self):
        while self.running:
            self.check_events()
            if self.background:
                continue
            self.update()
            self.draw()
        self.sprite_handler.quit()
        pg.mixer.quit()
        pg.quit()
        
if __name__ == '__main__':
    App().run()

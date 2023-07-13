import pygame_menu
import pygame as pg
from pygame._sdl2.video import Renderer, Texture, Image
import Settings
import os
import json

default_configuration = {
    'sound':True,
    'dark_mode':False,
    'show_fps':False,
    'speed_multiplier':1.0
}

class Configuration:
    def __init__(self, app, width, height, touchscreen = True):
        self.configuration_path = os.path.join(Settings.base_path, 'configuration.json')
        try:
            with open(self.configuration_path) as f:
                self.configuration = json.load(f)
        except:
            self.configuration = default_configuration
        self.app = app
        self.screen_size = (width,height)
        self.surface = pg.Surface(self.screen_size)
        self.menu : pygame_menu.Menu = pygame_menu.Menu('Configuration',
                                        self.screen_size[0],
                                        self.screen_size[1],
                                        theme = pygame_menu.Theme(title_font_size = 100, widget_font_size = 80),
                                        mouse_enabled=True,
                                        surface = self.surface,
                                        screen_dimension = self.screen_size,
                                        enabled = False,
                                        touchscreen=touchscreen,
                                        touchscreen_motion_selection=touchscreen)
        # def are_you_a_god(text):
        #     pass

        # self.menu.add.text_input('GodMode password :', password=True,onchange=are_you_a_god)
        def set_speed_multiplier(multiplier):
            self.configuration['speed_multiplier'] = multiplier
        self.menu.add.range_slider('Speed x', self.configuration['speed_multiplier'],(1.0,2.0), 0.1, onchange=set_speed_multiplier, width = 600)
        # self.menu.add.selector('Sound :', [('On', True), ('Off', False)], onchange=set_sound)
        def set_sound(on):
            self.configuration['sound'] = on
            self.synchronize()
        self.menu.add.toggle_switch('Sound :',default=self.configuration['sound'],onchange=set_sound)
        def set_dark_mode(value):
            self.configuration['dark_mode'] = value
            
        self.menu.add.toggle_switch('Dark mode :',default=self.configuration['dark_mode'],onchange=set_dark_mode)
        def set_show_fps(value):
            self.configuration['show_fps'] = value
        self.menu.add.toggle_switch('Show FPS :',default=self.configuration['show_fps'],onchange=set_show_fps)
        def on_play():
            self.synchronize()
            self.save_configuration()
            pg.event.post(pg.event.Event(Settings.EVENT_SOUND, sound = 'button_press'))
            self.disable()
        self.menu.add.button('Play', on_play)
        def on_quit():
            self.save_configuration()
            pg.event.post(pg.event.Event(Settings.EVENT_SOUND, sound = 'button_press'))
            pg.event.post(pg.event.Event(pg.QUIT))
        self.menu.add.button('Quit', on_quit)
        self.synchronize()
        
    def synchronize(self):
        Settings.speed_multiplier=self.configuration['speed_multiplier']
        if self.configuration['sound']:
            print('PotatoBird : unmute')
            self.app.unmute()
            pg.mixer.unpause()
        else:
            print('PotatoBird : mute')
            self.app.mute()
            pg.mixer.pause()
        self.app.set_dark_mode(self.configuration['dark_mode'])
        self.app.set_show_fps(self.configuration['show_fps'])
        
    def save_configuration(self):
        with open(self.configuration_path, 'w') as f:
            json.dump(self.configuration,f)
            
    def update(self, events):
        self.menu.update(events)
        for e in events:
            if e.type == pg.KEYDOWN:
                if e.key == pg.K_ESCAPE:
                    self.disable()
                elif e.key == pg.K_AC_BACK:
                    pg.event.post(pg.event.Event(pg.QUIT))
        
    def draw(self, renderer : Renderer):
        self.menu.draw(self.surface)
        img = Image(Texture.from_surface(renderer, pg.transform.scale(self.surface, self.screen_size)))
        img.draw(None,img.get_rect())

    def is_enabled(self):
        return self.menu.is_enabled()
    
    def enable(self):
        self.menu.enable()
    
    def disable(self):
        self.menu.disable()


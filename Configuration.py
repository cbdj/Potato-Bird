import pygame_menu
import pygame as pg
from pygame._sdl2.video import Renderer, Texture, Image
import Settings

class Configuration:
    def __init__(self, app, width, height, touchscreen = True):

        self.app = app
        self.screen_size = (width,height)
        self.surface = pg.Surface(self.screen_size)
        self.menu = pygame_menu.Menu('Configuration',
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
            self.app.speed=int(Settings.SPEED*multiplier)
            pass
        self.menu.add.range_slider('Speed x', 1.0,(1.0,2.0), 0.1, onchange=set_speed_multiplier, width = 600)
        # self.menu.add.selector('Sound :', [('On', True), ('Off', False)], onchange=set_sound)
        def set_sound(on):
            if on:
                print('PotatoBird : unmute')
                self.app.unmute()
                pg.mixer.unpause()
            else:
                print('PotatoBird : mute')
                self.app.mute()
                pg.mixer.pause()
        self.menu.add.toggle_switch('Sound :',default=True,onchange=set_sound)
        self.menu.add.toggle_switch('Dark mode :',default=False,onchange=self.app.set_dark_mode)
        def on_play():
            pg.event.post(pg.event.Event(Settings.EVENT_SOUND, sound = 'button_press'))
            self.disable()
        self.menu.add.button('Play', on_play)
        def on_quit():
            pg.event.post(pg.event.Event(Settings.EVENT_SOUND, sound = 'button_press'))
            pg.event.post(pg.event.Event(pg.QUIT))
        self.menu.add.button('Quit', on_quit)

    def update(self, events):
        self.menu.update(events)
        for e in events:
            if e.type == pg.KEYDOWN:
                if e.key == pg.K_ESCAPE:
                    self.disable()
        
    def draw(self, renderer : Renderer):
        self.menu.draw(self.surface)
        img = Image(Texture.from_surface(renderer, pg.transform.scale(self.surface, self.screen_size)))
        img.draw(img.get_rect(),img.get_rect())

    def is_enabled(self):
        return self.menu.is_enabled()
    
    def enable(self):
        self.menu.enable()
    
    def disable(self):
        self.menu.disable()


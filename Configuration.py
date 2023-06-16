import pygame_menu
import Settings
import pygame as pg
from pygame._sdl2.video import Renderer, Texture, Image

class Configuration:
    def __init__(self, app):
        def set_sound(on):
            if on:
                print('PotatoBird : unmute')
                self.app.unmute()
                pg.mixer.unpause()
            else:
                print('PotatoBird : mute')
                self.app.mute()
                pg.mixer.pause()

        self.app = app
        self.screen_size = (Settings.WIN_W,Settings.WIN_H)
        scaled_screen = (Settings.WIN_W*self.app.sprite_handler.scale,Settings.WIN_H*self.app.sprite_handler.scale)
        self.surface = pg.Surface(scaled_screen)
        self.menu = pygame_menu.Menu('Configuration',
                                        scaled_screen[0],
                                        scaled_screen[1],
                                        mouse_enabled=True,
                                        surface = self.surface,
                                        screen_dimension = scaled_screen,
                                        enabled = False,
                                        touchscreen=Settings.platform=='android')
        def are_you_a_god(text):
            print(text)

        self.menu.add.text_input('GodMode password :', password=False,onchange=are_you_a_god)
        # self.menu.add.range_slider()
        # self.menu.add.selector('Sound :', [('On', True), ('Off', False)], onchange=set_sound)
        self.menu.add.toggle_switch('Sound :',default=True,onchange=set_sound)
        self.menu.add.button('Play', self.disable)
        self.menu.add.button('Quit', lambda : pg.event.post(pg.event.Event(pg.QUIT)))

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
        return self.menu.enable()
    
    def disable(self):
        return self.menu.disable()


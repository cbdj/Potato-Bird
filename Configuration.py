import pygame_menu
import Settings
import pygame as pg
from pygame._sdl2.video import Renderer, Texture, Image

class Configuration:
    def __init__(self, app):
        def set_sound(value, on):
            if on:
                print('PotatoBird : unmute')
                self.app.unmute()
                pg.mixer.unpause()
            else:
                print('PotatoBird : mute')
                self.app.mute()
                pg.mixer.pause()

        def start_the_game():
            self.disable()
        self.app = app
        screen_size = (Settings.WIN_W,Settings.WIN_H)
        self.surface = pg.Surface(screen_size)
        self.menu = pygame_menu.Menu('Configuration', screen_size[0], screen_size[1],mouse_enabled=True,
                            surface = self.surface, screen_dimension = screen_size, enabled = False, touchscreen=Settings.platform=='android')
        # self.menu.add.text_input('Name :', default='John Doe')
        # self.menu.add.range_slider()
        self.menu.add.selector('Sound :', [('On', True), ('Off', False)], onchange=set_sound)
        self.menu.add.button('Play', start_the_game)
        self.menu.add.button('Quit', pygame_menu.events.EXIT)

    def update(self, events):
        self.menu.update(events)
        for e in events:
            if e.type == pg.KEYDOWN:
                if e.key == pg.K_ESCAPE:
                    self.disable()
        
    def draw(self, renderer : Renderer):
        self.menu.draw(self.surface)
        img = Image(Texture.from_surface(renderer, self.surface))
        img.draw(img.get_rect(),img.get_rect())

    def is_enabled(self):
        return self.menu.is_enabled()
    
    def enable(self):
        return self.menu.enable()
    
    def disable(self):
        return self.menu.disable()


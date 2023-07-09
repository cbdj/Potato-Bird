import pygame_menu
import pygame as pg
from pygame._sdl2.video import Renderer, Texture, Image
import Settings
import os

class PlayGamesIntents:
    def __init__(self, app, width, height, touchscreen = True):

        self.app = app
        self.screen_size = (width,height)
        self.surface = pg.Surface(self.screen_size)
        self.menu : pygame_menu.Menu = pygame_menu.Menu('Google Play',
                                        self.screen_size[0],
                                        self.screen_size[1],
                                        theme = pygame_menu.Theme(title_font_size = 100, widget_font_size = 80),
                                        mouse_enabled=True,
                                        surface = self.surface,
                                        screen_dimension = self.screen_size,
                                        enabled = False,
                                        touchscreen=touchscreen,
                                        touchscreen_motion_selection=touchscreen)
                                        
        self.menu.add.image(os.path.join(Settings.SPRITE_DIR_PATH,'games_leaderboards_green.png'), scale=(0.5,0.5),selectable=False)
        def on_show_leaderboards():
            pg.event.post(pg.event.Event(Settings.EVENT_SOUND, sound = 'button_press'))
            self.app.playgamesservices.leaderboards_client.show_leaderboards()
        self.menu.add.button('Show leaderboards', on_show_leaderboards)
        self.menu.add.image(os.path.join(Settings.SPRITE_DIR_PATH,'games_achievements_green.png'), scale=(0.5,0.5),selectable=False)
        def on_show_achievements():
            pg.event.post(pg.event.Event(Settings.EVENT_SOUND, sound = 'button_press'))
            self.app.playgamesservices.achievements_client.show_achievements()
        self.menu.add.button('Show achievements', on_show_achievements)
        def on_back():
            pg.event.post(pg.event.Event(Settings.EVENT_SOUND, sound = 'button_press'))
            self.disable()
        self.menu.add.button('Back', on_back)

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


import pathlib
from random import randrange
import Settings
from SpriteHandler import SpriteHandler
import pygame as pg
# import pygame.freetype as ft
import sys
from pygame._sdl2.video import Window, Renderer, Texture     


class App:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        screen_info = pg.display.Info()
        self.window = Window(title='flap.py', size=(screen_info.current_w,screen_info.current_h))
        self.window.set_icon(pg.image.load(Settings.ASSETS_DIR_PATH +'/favicon.ico'))
        self.renderer = Renderer(self.window)
        self.sprite_handler = SpriteHandler(self)
        self.renderer.scale = (self.sprite_handler.scale, self.sprite_handler.scale)
        self.clock = pg.time.Clock()
        self.dt = 0.0
        self.font = pg.font.SysFont('Verdana', Settings.FONT_SIZE)
        # self.font = ft.SysFont('Verdana', Settings.FONT_SIZE)
        self.fps_size = [Settings.FONT_SIZE * 13, Settings.FONT_SIZE]
        pg.time.set_timer(Settings.EVENT_DAY_NIGHT, Settings.DAY_NIGHT_TIME_MS)
        self.speed = Settings.SPEED
        self.running = True
        self.display_fps = False

    def update(self):
        self.sprite_handler.update()
        self.dt = self.clock.tick(60) * 0.001

    def draw_fps(self):
        fps = f'{self.clock.get_fps() :.0f} FPS | {self.sprite_handler.count_sprites()} SPRITES'
        # surf_black, rect = self.font.render(text=fps, fgcolor='black')
        # surf_black, rect = self.font.render(text=fps, fgcolor='green')
        surf_black = self.font.render(fps, False, 'black')
        surf = self.font.render(fps, False, 'green')
        tex1 = Texture.from_surface(self.renderer, surf_black)
        tex2 = Texture.from_surface(self.renderer, surf)
        tex1.draw(tex1.get_rect(),(2,0,tex1.width, tex1.height))
        tex1.draw(tex1.get_rect(),(0,2,tex1.width, tex1.height))
        tex1.draw(tex1.get_rect(),(-2,0,tex1.width, tex1.height))
        tex1.draw(tex1.get_rect(),(0,-2,tex1.width, tex1.height))
        tex2.draw(tex1.get_rect(),(0,0,tex1.width, tex1.height))

    def draw(self):
        self.renderer.clear()
        self.sprite_handler.draw()
        if self.display_fps:
            self.draw_fps()
        self.renderer.present()

    def check_events(self):
        for e in pg.event.get():
            if e.type == pg.QUIT:
                self.running = False
            elif e.type == pg.MOUSEBUTTONDOWN:
                self.sprite_handler.on_mouse_press()
            elif e.type == pg.KEYDOWN:
                if e.key == pg.K_ESCAPE:
                    self.running = False
                if e.key == pg.K_d:
                    self.display_fps = not self.display_fps
                else:
                    self.sprite_handler.on_key_press(e.key)
            elif e.type == Settings.EVENT_DAY_NIGHT:
                if self.sprite_handler._started and not self.sprite_handler._paused: 
                    self.sprite_handler.background.toggle_day_night()
                    self.speed = Settings.SPEED_INCREASE_FACTOR*self.speed
                    self.sprite_handler.update_speed(self.speed)
                    self.sprite_handler.sounds['swoosh'].play()

    def run(self):
        while self.running:
            self.check_events()
            self.update()
            self.draw()
        self.sprite_handler.quit()
        pg.mixer.quit()
        pg.quit()

if __name__ == '__main__':
    app = App()
    app.run()
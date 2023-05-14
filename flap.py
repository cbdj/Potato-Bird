import pathlib
from random import randrange
from Settings import *
from SpriteHandler import SpriteHandler
import pygame as pg
import pygame.freetype as ft
import sys
from pygame._sdl2.video import Window, Renderer, Texture     

class App:
    def __init__(self):
        pg.init()
        self.window = Window(size=WIN_SIZE)
        self.renderer = Renderer(self.window)
        self.renderer.draw_color = (0, 0, 0, 255)
        self.clock = pg.time.Clock()
        self.sprite_handler = SpriteHandler(self)
        self.dt = 0.0
        self.font = ft.SysFont('Verdana', FONT_SIZE)
        self.fps_size = [FONT_SIZE * 13, FONT_SIZE]
        self.fps_surf = pg.Surface(self.fps_size)
        pg.time.set_timer(EVENT_DAY_NIGHT, DAY_NIGHT_TIME_MS)
        self.speed = SPEED
        self.running = True
        self.display_fps = False

    def update(self):
        self.sprite_handler.update()
        self.dt = self.clock.tick(60) * 0.001

    def draw_fps(self):
        self.fps_surf.fill('black')
        fps = f'{self.clock.get_fps() :.0f} FPS | {self.sprite_handler.count_sprites()} SPRITES'
        self.font.render_to(self.fps_surf, (0, 0), text=fps, fgcolor='green', bgcolor='black')
        tex = Texture.from_surface(self.renderer, self.fps_surf)
        tex.draw((0, 0, *self.fps_size), (0, 0, *self.fps_size))

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
            elif e.type == EVENT_DAY_NIGHT:
                if self.sprite_handler._started and not self.sprite_handler._paused: 
                    self.sprite_handler.toggle_day()
                    self.speed = SPEED_INCREASE_FACTOR*self.speed
                    self.sprite_handler.update_speed(self.speed)

    def run(self):
        while self.running:
            self.check_events()
            self.update()
            self.draw()
        pg.quit()

if __name__ == '__main__':
    app = App()
    app.run()
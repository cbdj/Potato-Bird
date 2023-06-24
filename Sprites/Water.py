import pygame as pg
from pygame._sdl2 import Image, Texture
from .SpriteUnit import SpriteUnit
Point = pg.Vector2
blue = (0,0,255, 240)
white = pg.Color('white')

class _WaterSpring:
    def __init__(self, x, target_height):
        self.target_height = target_height
        self.dampening = 0.05  # adjust accordingly
        self.tension = 0.01
        self.height = self.target_height
        self.vely = 0
        self.x = x
        self.orig_x = x

    def translate(self, delta):
        self.x = self.orig_x + delta
        
    def reset(self):
        self.x = self.orig_x
        self.vely = 0
        self.height = self.target_height
        
    def update(self):
        dh = self.target_height - self.height
        if abs(dh) < 0.01:
            self.height = self.target_height
        self.vely += self.tension * dh - self.vely * self.dampening
        self.height += self.vely

    def draw(self):
        pass
        # renderer.draw_color = white
        # renderer.draw_rect((self.x, self.height,2,2))

class Wave:
    def __init__(self, handler, rect : pg.Rect):
        self.diff = 20
        self.rect = rect
        self.orig_rect = rect.copy()
        self.bottom = self.rect.bottom
        self.handler = handler
        self.renderer = handler.renderer
        print(rect)
        self.springs = [_WaterSpring(x=i* self.diff, target_height = self.rect.y - self.rect.h/2) for i in range(self.rect.width //  self.diff+2)]
        self.points = [Point(i.x, i.height) for i in self.springs]
        self.vel_x = 0
        self.delta = 0
        self.triggered = False # optimisation to improve performance. 

    def _get_spring_index_for_x_pos(self, x):
        delta = self.rect.x - self.orig_rect.x
        index = int((x - delta) // self.diff)
        if index < 0 or index > len(self.springs):
            return None
        return index

    def get_rect(self):
        return self.rect
    
    def get_target_height(self):
        return self.rect.top

    def set_target_height(self, height):
        self.rect.h = height
        self.rect.bottom =  self.bottom
        for i in self.springs:
            i.target_height = self.rect.top

    def _get_volume(self):
        return self.rect.h * self.rect.w
    
    def add_volume(self, volume):
        self.set_target_height((self._get_volume() + volume)/self.rect.w)

    def update_speed(self, speed):
        self.vel_x = speed
        
    def translate(self):
        # delta = self.vel_x * self.handler.app.dt
        delta = 0
        self.rect.x += delta
        if self.rect.x < self.orig_rect.x - self.rect.width//2 :
            self.rect.x = self.orig_rect.x
        for i in self.springs:
            i.translate(self.rect.x - self.orig_rect.x)
            
    def reset(self):
        for i in self.springs:
            i.reset()
        self.rect = self.orig_rect
        self.update()
        self.triggered = False
        
    def update(self):
        self.translate()
        if not self.triggered :
            self.points = [Point(self.springs[0].x, self.springs[0].height),Point(self.springs[-1].x, self.springs[-1].height)]
            return
        for i in self.springs:
            i.update()
        self._spread_wave()
        self.points = [Point(i.x, i.height) for i in self.springs]

    def draw(self):
        # tmp = self.renderer.draw_blend_mode
        # self.renderer.draw_color = (0,255,0,50)
        self.renderer.draw_blend_mode = 2
        # self.renderer.fill_rect((0,980,1920,200))
        for i in self.springs:
            i.draw()
        self._draw_lines()
        self._draw_quads()
        # self.renderer.draw_blend_mode = tmp

    def _draw_quads(self):
        self.renderer.draw_color = blue
        for i in range(len(self.points)-1):
            point1=self.points[i]
            point2=self.points[i+1]
            self.renderer.fill_quad(point1,point2,(point2[0], self.rect.bottom), (point1[0], self.rect.bottom))

    def _draw_lines(self):
        self.renderer.draw_color = white
        for i in range(len(self.points)-1):
            point1=self.points[i]
            point2=self.points[i+1]
            self.renderer.draw_line(point1, point2)

    def _spread_wave(self):
        spread = 0.1
        for i in range(1,len(self.springs)-1):
            self.springs[i - 1].vely += spread * (self.springs[i].height - self.springs[i - 1].height)
            self.springs[i + 1].vely += spread * (self.springs[i].height - self.springs[i + 1].height)

    def splash(self, x, vel):
        index = self._get_spring_index_for_x_pos(x)
        if index is None:
            return None
        self.triggered = True
        self.springs[index].vely += vel
        return self.springs[index]

    # def splash(self, rect : pg.Rect, vel):
    #     if self.rect.bottom < rect.bottom < self.rect.top:
    #         return self.splash(rect.x)
    #     return None

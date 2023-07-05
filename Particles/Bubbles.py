import pygame as pg
import random
from pygame._sdl2 import Texture, Image, Renderer
import pygame.gfxdraw as gfx

class Bubble:
    def __init__(self, renderer : Renderer, texture : Texture, alpha : int, x, y, max_y):
        self.x = x+random.randrange(-40,40)*0.1*texture.get_rect().w
        self.y = y
        self.scale = 1.0
        self.texture = texture
        self.alpha = alpha
        self.alpha_rate = 1
        self.alive = True
        self.vy = 0
        self.vx = 0
        self.max_y = max_y
        self.src_rect = self.texture.get_rect()
        self.dest_rect = self.src_rect.copy()

    def update(self):
        self.y += self.vy
        self.vy = -1
        if self.scale < 4:
            self.scale += 0.01
        self.alpha -= self.alpha_rate
        if self.alpha < 0:
            self.alpha = 0
        self.alive = self.y > self.max_y
        self.dest_rect.w = self.src_rect.w*self.scale
        self.dest_rect.h = self.src_rect.h*self.scale
        self.dest_rect.center = (self.x, self.y)

    def draw(self):
        self.texture.alpha = self.alpha
        self.texture.draw(self.src_rect, self.dest_rect)

class Bubbles:
    def __init__(self, renderer, x, y, max_y):
        self.max_y = max_y
        surface = pg.Surface((6,6), pg.SRCALPHA)
        gfx.circle(surface,surface.get_rect().w//2, surface.get_rect().h//2,surface.get_rect().w//2,  pg.Color('white'))
        self.texture = Texture.from_surface(renderer, surface)
        self.alpha = surface.get_alpha()
        self.x = x
        self.y = y
        self.vel_x = 0
        self.vel_y = 0
        self.renderer = renderer
        self.particles = []
        self.counter = 0

    def set_source_position(self,x,y):
        self.x = x
        self.y = y

    def update(self):
        self.particles = [i for i in self.particles if i.alive]
        self.counter += 1
        if self.counter > 10:
            self.counter = 0
            self.particles.append(Bubble(self.renderer,self.texture,self.alpha, self.x,self.y, self.max_y))
        for particle in self.particles:
            particle.update()

    def draw(self):
        for particle in self.particles:
            particle.draw()

    def reset(self):
        self.particles.clear()

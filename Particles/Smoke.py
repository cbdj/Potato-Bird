import pygame as pg
import random
import numpy as np
from pygame._sdl2 import Texture, Image, Renderer

def scale(img: pg.Surface, factor):
    w, h = img.get_width() * factor, img.get_height() * factor
    return pg.transform.scale(img, (int(w), int(h)))

class SmokeParticle:
    def __init__(self, renderer, textures, x, y, vel_x, vel_y):
        self.x = x
        self.y = y
        self.index_scale_k = 0
        self.textures = textures
        self.img = self.textures[0]
        self.alpha = 255
        self.alpha_rate = 3
        self.alive = True
        self.vy = vel_y
        self.vx = vel_x
        self.k = 0.01 * random.random() * random.choice([-1, 1])

    def update(self):
        self.y += self.vy
        self.vy += self.k
        self.x -= self.vx
        self.vx *= 0.99
        self.index_scale_k += 1
        self.alpha -= self.alpha_rate
        if self.alpha < 0:
            self.alpha = 0
            self.alive = False
        self.alpha_rate -= 0.1
        if self.alpha_rate < 1.5:
            self.alpha_rate = 1.5
        self.img = self.textures[min(self.index_scale_k, len(self.textures))]
        self.img.alpha = self.alpha

    def draw(self):
        dest_rect = self.img.get_rect()
        dest_rect.center=(self.x, self.y)
        self.img.draw(self.img.get_rect(), dest_rect)



class Smoke:
    def __init__(self, renderer, surface, x, y):
        self.textures = [Image(Texture.from_surface(renderer, scale(surface, factor))) for factor in np.arange(0.1,1,0.005)]
        self.x = x
        self.y = y
        self.vel_x = 0
        self.renderer = renderer
        self.surface = surface
        self.particles = []
        self.frames = 0

    def set_source_position(self,x,y):
        self.x = x
        self.y = y

    def set_speed(self,vel_x, vel_y):
        self.vel_x = vel_x
        self.vel_y = vel_y

    def update(self):
        self.particles = [i for i in self.particles if i.alive]
        self.frames += 1
        if self.frames % 2 == 0 and (self.vel_x or self.vel_y):
            self.particles.append(SmokeParticle(self.renderer,self.textures,self.x,self.y, self.vel_x, self.vel_y))
            self.frames = 0
        for i in self.particles:
            i.update()

    def draw(self):
        for particle in self.particles:
            particle.draw()
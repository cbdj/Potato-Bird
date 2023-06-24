import pygame as pg
import random
from pygame._sdl2 import Texture, Image, Renderer
from pygame import Rect

class SmokeParticle:
    def __init__(self, renderer : Renderer, texture : Texture, alpha : int, x, y, vel_x, vel_y):
        self.x = x
        self.y = y
        self.scale = 1.0
        self.texture = texture
        self.alpha = alpha
        self.alpha_rate = 3
        self.alive = True
        self.vy = vel_y
        self.vx = vel_x
        self.k = 0.01 * random.random() * random.choice([-1, 1])
        self.src_rect = self.texture.get_rect()
        self.dest_rect = self.src_rect.copy()

    def update(self):
        self.y += self.vy
        self.vy += self.k
        self.x -= self.vx
        self.vx *= 0.99
        self.scale -= 0.01
        self.alpha -= self.alpha_rate
        if self.alpha <= 0 or self.scale <= 0:
            self.alpha = 0
            self.scale = 0
            self.alive = False
        self.alpha_rate -= 0.1
        if self.alpha_rate < 1.5:
            self.alpha_rate = 1.5
        self.dest_rect.w = self.src_rect.w*self.scale
        self.dest_rect.h = self.src_rect.h*self.scale
        self.dest_rect.center = (self.x, self.y)

    def draw(self):
        self.texture.alpha = self.alpha
        self.texture.draw(self.src_rect, self.dest_rect)

class Smoke:
    def __init__(self, renderer, surface, x, y, trigger_speed = 0):
        self.trigger_speed = trigger_speed
        self.texture = Texture.from_surface(renderer, surface)
        self.alpha = surface.get_alpha()
        self.x = x
        self.y = y
        self.vel_x = 0
        self.renderer = renderer
        self.particles = []

    def set_source_position(self,x,y):
        self.x = x
        self.y = y

    def set_speed(self,vel_x, vel_y):
        self.vel_x = vel_x
        self.vel_y = vel_y

    def update(self):
        self.particles = [i for i in self.particles if i.alive]
        if self.vel_x >= self.trigger_speed or self.vel_y >= self.trigger_speed:
            self.particles.append(SmokeParticle(self.renderer,self.texture,self.alpha, self.x,self.y, self.vel_x, self.vel_y))
        for particle in self.particles:
            particle.update()

    def draw(self):
        for particle in self.particles:
            particle.draw()

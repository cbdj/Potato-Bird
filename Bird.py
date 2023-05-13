from SpriteUnit import SpriteUnit
from Settings import *
import pygame as pg
class Bird(SpriteUnit):
    def __init__(self, handler, image, x, y):
        super().__init__(handler, image, x, y)
        self.angle = 0
        self.mass = 0.1
        self.dead=True

    def translate(self):
        if not self.dead:
            self.vel_y = self.vel_y  + 9.81*1000*self.mass*self.handler.app.dt
            self.y += self.vel_y * self.handler.app.dt
            if self.y < 0 or self.y > WIN_H-50:
                self.vel_y *= -1
        self.rect.center = self.x, self.y

    def rotate(self):
        self.image.angle += self.vel_y * self.handler.app.dt

    def bump(self, speed):
        self.vel_y = -speed

    def update(self):
        self.translate() 
        if pg.sprite.spritecollideany(self, self.handler.group_collide):
            self.handler.stop()
            self.dead = True
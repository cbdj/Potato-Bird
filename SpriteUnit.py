import pygame as pg
from random import randrange
from pygame._sdl2.video import Image, Texture
from pygame import mask

class SpriteUnit(pg.sprite.Sprite):
    def __init__(self, handler, image, x, y):
        super().__init__()
        self.handler = handler
        self.mask = mask.from_surface(image)
        self.image = Image(Texture.from_surface(self.handler.renderer, image))
        self.rect = self.image.get_rect()
        self.orig_rect = self.rect.copy()
        self.orig_x, self.orig_y = x, y
        self.x, self.y = x, y
        self.vel_x, self.vel_y = 0, 0
        self.rect.center = self.x, self.y

    def translate(self):
        self.x += self.vel_x * self.handler.app.dt
        self.y += self.vel_y * self.handler.app.dt
        self.rect.center = self.x, self.y

    def update(self):
        self.translate()

    def update_image(self, image : Image):
        angle = self.image.angle
        self.image = image
        self.image.angle =  angle
        self.rect = self.image.get_rect()
        self.rect.center = self.x, self.y

    def reset(self):
        self.x = self.orig_x
        self.y = self.orig_y 
        self.vel_x = 0
        self.vel_y = 0
        self.image.angle=0

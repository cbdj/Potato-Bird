import pygame as pg
from random import randrange
from pygame._sdl2.video import Image

class SpriteUnit(pg.sprite.Sprite):
    def __init__(self, handler, image, x, y):
        super().__init__()
        self.handler = handler
        self.update_image(image)
        self.orig_x, self.orig_y = x, y
        self.x, self.y = x, y
        self.vel_x, self.vel_y = 0, 0

    def translate(self):
        self.x += self.vel_x * self.handler.app.dt
        self.y += self.vel_y * self.handler.app.dt
        self.rect.center = self.x, self.y

    def update(self):
        self.translate()

    def update_image(self, image):
        self.image = Image(image)
        self.rect = self.image.get_rect()
        self.orig_rect = self.rect.copy()

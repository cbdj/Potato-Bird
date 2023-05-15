from SpriteUnit import SpriteUnit
from Settings import *
from pygame._sdl2 import Image, Texture
import pygame as pg
class Bird(SpriteUnit):
    def __init__(self, handler, image_down, image_middle, image_up, x, y):
        super().__init__(handler, image_middle, x, y)
        self.image_down = Image(Texture.from_surface(self.handler.renderer, image_down))
        self.image_middle = Image(Texture.from_surface(self.handler.renderer, image_middle))
        self.image_up = Image(Texture.from_surface(self.handler.renderer, image_up))
        self.image = image_middle
        self.angle = 0
        self.mass = 0.1

    def translate(self):
        self.vel_y = self.vel_y  + 9.81*1000*self.mass*self.handler.app.dt
        self.y += self.vel_y * self.handler.app.dt
        if self.y < 0 :
            self.vel_y *= -1
        self.rect.center = self.x, self.y
        if self.vel_y > BUMP_SPEED//10:
            self.update_image(self.image_up)
        elif self.vel_y < -BUMP_SPEED//10: 
            self.update_image(self.image_down)
        else : 
            self.update_image(self.image_middle)

    def rotate(self):
        self.image.angle += self.vel_y * self.handler.app.dt

    def bump(self, speed):
        self.vel_y = -speed
        self.handler.sounds['wing'].play()

    def update(self):
        self.translate() 
        if  self.y > WIN_H - self.handler.base.image.get_rect().height or pg.sprite.spritecollideany(self, self.handler.group_collide, pg.sprite.collide_mask):
            self.handler.sounds['hit'].play()
            self.handler.sounds['die'].play()
            self.handler.game_over()
            

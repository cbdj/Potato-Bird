from .SpriteUnit import SpriteUnit
from pygame._sdl2 import Image, Texture
import pygame as pg

class Bird(SpriteUnit):
    def __init__(self, handler, image_down, image_middle, image_up, x, y, bump_speed, mass):
        super().__init__(handler, image_middle, x, y)
        self.image_down = Image(Texture.from_surface(self.handler.renderer, image_down))
        self.image_middle = Image(Texture.from_surface(self.handler.renderer, image_middle))
        self.image_up = Image(Texture.from_surface(self.handler.renderer, image_up))
        self.image = self.image_middle
        self.floor = self.handler.base.y - self.handler.base.rect.h//2 - self.image.get_rect().h//2
        self.mass = mass
        self.weight = 0.0
        self.dead = False
        self.hit = False
        self.bump_speed = bump_speed

    def translate(self):
        if self.x < 2*self.orig_x/3:
            self.vel_x = 0
        else:
            self.x += self.vel_x * self.handler.app.dt
        self.vel_y = self.vel_y  + 9.81*1000*self.weight*self.handler.app.dt
        self.y += self.vel_y * self.handler.app.dt
        if self.y < 0 :
            self.vel_y *= -1
        self.rect.center = self.x, self.y
        if self.vel_y > self.bump_speed/5 or self.vel_y < -70*self.bump_speed/100:
            self.update_image(self.image_up)
        elif self.vel_y < -self.bump_speed/5: 
            self.update_image(self.image_down)
        else : 
            self.update_image(self.image_middle)
        if self.vel_y > 0 and self.image.angle < 45 or self.vel_y < 0 and self.image.angle > -45:
            self.rotate()

    def rotate(self):
        self.image.angle += self.vel_y * self.handler.app.dt

    def bump(self, speed):
        if self.hit:
            return
        self.weight = self.mass
        self.vel_y = -speed
        self.handler.sounds['wing'].play()

    def update(self):
        self.translate() 
        if self.dead:
            return
        if not self.hit and pg.sprite.spritecollideany(self, self.handler.group_collide, pg.sprite.collide_mask):
            self.hit = True
            self.vel_x = 0
            self.handler.update_speed(0)
            self.handler.sounds['hit'].play()
            if self.y < self.floor:
                self.handler.sounds['die'].play()

        if  self.y > self.floor:
            if not self.dead:
                self.handler.sounds['hit'].play()
            self.hit = True
            self.dead= True
            self.vel_x = 0
            self.vel_y = 0
            self.weight = 0.0
            self.handler.game_over()

    def reset(self):
        super().reset()
        self.dead=False
        self.hit=False
        self.weight = 0.0
            

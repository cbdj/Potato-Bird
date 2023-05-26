from SpriteUnit import SpriteUnit
import Settings
from pygame._sdl2 import Image, Texture
import pygame as pg
class Bird(SpriteUnit):
    def __init__(self, handler, image_down, image_middle, image_up, x, y):
        super().__init__(handler, image_middle, x, y)
        self.image_down = Image(Texture.from_surface(self.handler.renderer, image_down))
        self.image_middle = Image(Texture.from_surface(self.handler.renderer, image_middle))
        self.image_up = Image(Texture.from_surface(self.handler.renderer, image_up))
        self.image = self.image_middle
        self.floor = self.handler.base.y - self.handler.base.rect.h//2 - self.image.get_rect().h//2
        self.mass = 0.0
        self.dead = False
        self.hit = False

    def translate(self):
        if self.x < Settings.WIN_W/3:
            self.vel_x = 0
        else:
            self.x += self.vel_x * self.handler.app.dt
        self.vel_y = self.vel_y  + 9.81*1000*self.mass*self.handler.app.dt
        self.y += self.vel_y * self.handler.app.dt
        if self.y < 0 :
            self.vel_y *= -1
        self.rect.center = self.x, self.y
        if self.vel_y > Settings.BUMP_SPEED/5 or self.vel_y < -70*Settings.BUMP_SPEED/100:
            self.update_image(self.image_up)
        elif self.vel_y < -Settings.BUMP_SPEED/5: 
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
        self.mass = Settings.BIRD_MASS_KG
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
            self.handler.sounds['die'].play()

        if  self.y > self.floor:
            if not self.dead:
                self.handler.sounds['hit'].play()
            self.hit = True
            self.dead= True
            self.vel_x = 0
            self.vel_y = 0
            self.mass = 0.0
            self.handler.game_over()

    def reset(self):
        super().reset()
        self.dead=False
        self.hit=False
        self.mass = 0.0
            

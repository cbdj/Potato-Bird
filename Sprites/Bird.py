from .SpriteUnit import SpriteUnit
from pygame._sdl2 import Image, Texture
import pygame as pg
import Settings
from Particles.Smoke import Smoke
from Particles.Bubbles import Bubbles
from .Bull import Bull

class Bird(SpriteUnit):
    def __init__(self, handler, image_down, image_middle, image_up, x, y, bump_speed, mass, trainee : pg.Surface):
        super().__init__(handler, image_middle, x, y)
        self._image_down = Image(Texture.from_surface(self.handler.renderer, image_down))
        self._image_middle = Image(Texture.from_surface(self.handler.renderer, image_middle))
        self._image_up = Image(Texture.from_surface(self.handler.renderer, image_up))
        self._angry_down = Image(Texture.from_surface(self.handler.renderer, self.handler.images['angrybird-downflap']))
        self._angry_middle = Image(Texture.from_surface(self.handler.renderer, self.handler.images['angrybird-midflap']))
        self._angry_up = Image(Texture.from_surface(self.handler.renderer, self.handler.images['angrybird-upflap']))
        self.image_down = self._image_down
        self.image_middle = self._image_middle
        self.image_up = self._image_up
        self.image : Image = self.image_middle
        self.floor = self.handler.base.rect.y - self.handler.base.rect.h//2 - self.image.get_rect().h//2
        self.mass = mass
        self.weight = 0.0
        self.dead = False
        self.hit = False
        self.bump_speed = bump_speed
        self.smoke = Smoke(self.handler.renderer, trainee,self.x,self.y, Settings.SPEED)
        self.bubbles = Bubbles(self.handler.renderer,self.x,self.y, self.handler.base.rect.y - self.handler.base.rect.h//2)
        self.trainee = self.smoke
        self.bottom = Settings.WIN_H - self.image.get_rect().w//4
        self._bull = False
        self._collided = False

    def translate(self):
        if self.x < 2*self.orig_x/3:
            self.vel_x = 0
        else:
            self.x += self.vel_x * self.handler.app.dt
        if self.weight > 0.0:
            self.vel_y = self.vel_y  + 9.81*1000*self.weight*self.handler.app.dt
            self.y += self.vel_y * self.handler.app.dt
        if self.y < 0 :
            self.vel_y = abs(self.vel_y)
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
        self.image.angle += 0.5*self.vel_y * self.handler.app.dt

    def bump(self, speed):
        if self.hit:
            return
        self.weight = self.mass
        self.vel_y = -speed
        pg.event.post(pg.event.Event(Settings.EVENT_SOUND, sound = 'wing'))

    @property
    def bull(self):
        return self._bull
    @bull.setter
    def bull(self, value:bool):
        self._bull = value
        if value:
            self.image_down = self._angry_down
            self.image_middle = self._angry_middle
            self.image_up = self._angry_up
            pg.time.set_timer(pg.event.Event(Bull.event,phase=1), Bull.timeout)
        else:
            self.image_down = self._image_down
            self.image_middle = self._image_middle
            self.image_up = self._image_up

    def update(self):
        self.translate() 
        bonus = pg.sprite.spritecollide(self, self.handler.group_bonus,dokill=True,collided=pg.sprite.collide_mask)
        if len(bonus):
            for bonu in bonus:
                if isinstance(bonu, Bull) and not self.bull:
                    pg.event.post(pg.event.Event(Settings.EVENT_SOUND, sound = 'roar'))
                    self.bull = True
                    pg.event.post(pg.event.Event(Settings.INCREMENT_SPEED, increment = Bull.speed_increment))
                    bonu.ready = False
        colliding = pg.sprite.spritecollideany(self, self.handler.group_collide, pg.sprite.collide_mask)
        if colliding is None:
            self._collided = False
        if not self.dead and not self.hit and not self._collided and colliding is not None:
            self._collided = True
            if not self.bull:
                self.hit = True
                self.vel_x = 0
                self.handler.app.speed = 0
                pg.event.post(pg.event.Event(Settings.EVENT_SOUND, sound = 'hit'))
                if self.y < self.floor:
                    pg.event.post(pg.event.Event(Settings.EVENT_SOUND, sound = 'die'))
            else:
                pg.event.post(pg.event.Event(Settings.EVENT_SOUND, sound = 'explosion'))
                colliding.smash(self.y)
            pg.event.post(pg.event.Event(Settings.SHAKE_SCREEN, duration = 20, intensity = 10))

        if  self.y > self.floor:
            self.trainee = self.bubbles
            if not self.dead:
                pg.event.post(pg.event.Event(Settings.EVENT_SOUND, sound = 'splash'))
                pg.event.post(pg.event.Event(Settings.SHAKE_SCREEN, duration = 20, intensity = 10))
                self.handler.base.splash(self.x, self.vel_y/20)
                self.hit = True
                self.dead= True
                self.vel_x = 0
                self.vel_y = self.vel_y/20
                self.weight /= 20
                self.handler.game_over()
        else:
            self.trainee = self.smoke
            self.smoke.set_speed(-self.handler.base.vel_x*self.handler.app.dt, -self.vel_y*self.handler.app.dt/20)

        if  self.y > self.bottom:
            self.vel_y = 0
            self.weight = 0.0

        self.trainee.set_source_position(self.x, self.y)
        self.trainee.update()
            
    def draw(self):
        self.trainee.draw()
        self.image.draw(None, self.rect)

    def reset(self):
        super().reset()
        self.bull = False
        self.dead=False
        self.hit=False
        self.weight = 0.0
        self.bubbles.reset()
        self.smoke.reset()
            

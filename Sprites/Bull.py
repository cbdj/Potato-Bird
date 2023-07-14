from .SpriteUnit import SpriteUnit
from pygame._sdl2 import Image, Texture
import pygame as pg
import Settings
from Particles.Smoke import Smoke
from Particles.Bubbles import Bubbles
import random

class Bull(SpriteUnit):
    timeout = 6000
    event = pg.event.custom_type()
    speed_increment = 300
    gamble = 8 # minimum 1, the greater, the less chance to hit
    def __init__(self, handler, image, x, y):
        super().__init__(handler, image, x, y)
        self.height = image.get_height()
        self._ready = False
        pg.time.set_timer(pg.event.Event(Bull.event,phase=0), Bull.timeout)

    def translate(self):
        self.x += self.vel_x * self.handler.app.dt
        self.rect.center = self.x+random.randint(-2, 2), self.y+random.randint(-2, 2)

    def update(self):
        x=self.x
        self.translate() 
        if self.x < 0 and x > 0:
            self.ready = False
            pg.time.set_timer(pg.event.Event(Bull.event,phase=0), Bull.timeout)

    def reset(self):
        super().reset()
        self._ready = False
        pg.time.set_timer(pg.event.Event(Bull.event,phase=0), Bull.timeout)

    @property
    def ready(self):
        return self._ready
    
    @ready.setter
    def ready(self, value:bool):
        self._ready = value
            

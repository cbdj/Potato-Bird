from .SpriteUnit import SpriteUnit
from pygame._sdl2 import Image, Texture
import pygame as pg
import Settings
from Particles.Smoke import Smoke
from Particles.Bubbles import Bubbles

class Bull(SpriteUnit):
    timeout = 10
    event = pg.event.custom_type()
    speed_increment = 30
    def __init__(self, handler, image, x, y):
        super().__init__(handler, image, x, y)
        self.height = image.get_height()
        self._ready = True

    def translate(self):
        self.x += self.vel_x * self.handler.app.dt
        self.rect.center = self.x, self.y

    def update(self):
        self.translate() 

    def reset(self):
        super().reset()

    @property
    def ready(self):
        return self._ready
    
    @ready.setter
    def ready(self, value:bool):
        self._ready = value
            

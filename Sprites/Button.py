from .SpriteUnit import SpriteUnit
from pygame._sdl2 import Image, Texture
import pygame as pg
import Settings

class Button(SpriteUnit):
    def __init__(self, handler, image_unpressed, image_pressed, x, y, callback):
        self.image_unpressed = Image(Texture.from_surface(handler.renderer, image_unpressed))
        if image_pressed == image_unpressed:
            self.image_pressed = Image(Texture.from_surface(handler.renderer, (pg.transform.scale_by(image_pressed,0.5))))
        else:
            self.image_pressed  = Image(Texture.from_surface(handler.renderer, image_pressed))
        self.callback = callback
        self.pressed=False
        super().__init__(handler, self.image_unpressed, x, y)

    def translate(self):
        self.x += self.vel_x * self.handler.app.dt
        if self.x < self.orig_x - self.rect.width//2 :
            self.x = self.orig_x
        self.rect.center = self.x, self.y

    def press(self):
        self.update_image(self.image_pressed)
        self.pressed=True

    def unpress(self):
        pg.event.post(pg.event.Event(Settings.EVENT_SOUND, sound = 'button_press'))
        self.update_image(self.image_unpressed)
        self.pressed=False
        self.callback()
from .Base import Base
from pygame._sdl2 import Image, Texture

class Background(Base):
    def __init__(self, handler, image_day, image_night, x, y):
        super().__init__(handler, image_day, x, y)
        self.day_image = Image(Texture.from_surface(self.handler.renderer, image_day))
        self.night_image = Image(Texture.from_surface(self.handler.renderer, image_night))
        self.day = True
        self.dark_mode = False
        
    def toggle_day_night(self):
        if self.dark_mode:
            self.update_image(self.night_image)
            return
        if self.day:
            self.update_image(self.night_image)
        else:
            self.update_image(self.day_image)
        self.day = not self.day

    def reset(self):
        if self.dark_mode:
            self.update_image(self.night_image)
            return
        self.day = True
        self.update_image(self.day_image)

    def set_dark_mode(self,on):
        self.dark_mode = on
        if on:
            self.update_image(self.night_image)
        else:
            self.update_image(self.day_image)

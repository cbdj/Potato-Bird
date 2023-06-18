import pygame as pg
import os
from pygame._sdl2 import Image, Texture
from .SpriteUnit import SpriteUnit

def upscale(surface, scale):
    return pg.transform.scale(surface, (surface.get_rect().w * scale, surface.get_rect().h * scale))

class Score(SpriteUnit):
    def __init__(self, handler, x, y, font_size, scale = 1.0):
        self.score=0
        self.font_size = font_size
        self.scale = scale
        super().__init__(handler, self._get_image(handler),x,y)

    def _get_image(self, handler):
        surface = pg.font.SysFont('Verdana', self.font_size).render( str(self.score), True, 'white')
        return Image(Texture.from_surface(handler.renderer, upscale(surface,self.scale)))

    def update_slow(self):
        self.update_image(self._get_image(self.handler))

    def reset(self):
        super().reset()
        self.score=0
        self.update_slow()

    def increment(self, points=1):
        self.score += points
        self.update_slow()

    def get(self):
        return self.score
    
    def set(self, score):
        self.score = score
        self.update_slow()

class Best(Score):
    def __init__(self, handler, x, y, save_path, font_size, scale = 1.0):
        super().__init__(handler, x, y, font_size, scale)
        self.remote_best=0
        self.orig_w = self.image.get_rect().w
        self.score_path = os.path.join(save_path, 'record.txt')
        print(f'Record file path : {os.path.abspath(self.score_path)}')
        if os.path.exists(self.score_path):
            with open(self.score_path,'r') as score_file:
                self.set(int(score_file.read()))
                
    def update(self):
        if self.remote_best > self.score:
            self.set(self.remote_best)
        super().update()

    def update_slow(self):
        # Specific treatment for align left
        new_image = self._get_image(self.handler)
        offset = new_image.get_rect().w - self.orig_w
        self.update_image(new_image)
        if offset > 0:
            self.x = self.orig_x + offset//2

    def reset(self):
        pass

    def set_remote_best(self, best):
        self.remote_best = best

    def save(self):
        with open(self.score_path,'w') as score_file:
            score_file.write(str(self.score))

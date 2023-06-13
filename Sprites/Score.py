import pygame as pg
import os
from pygame._sdl2 import Image, Texture
from .SpriteUnit import SpriteUnit

class Score(SpriteUnit):
    def __init__(self, handler, x, y, font_size):
        self.best=0
        self.remote_best=0
        self.score=0
        self.font_size = font_size
        current_path = '.'
        self.score_path = os.path.join(current_path, 'record.txt')
        print(f'Record file path : {os.path.abspath(self.score_path)}')
        if os.path.exists(self.score_path):
            with open(self.score_path,'r') as score_file:
                self.best=int(score_file.read())
        super().__init__(handler, self.get_surface(),x,y)
        
    def set_remote_best(self, best):
        self.remote_best = best
        
    def update(self):
        if self.remote_best > self.best:
            self.best = self.remote_best
            self.update_slow()
        super().update()
        
    def update_slow(self):
        self.update_image(Image(Texture.from_surface(self.handler.renderer, self.get_surface())))

    def reset(self):
        super().reset()
        self.score=0
        self.update_slow()

    def increment(self, points=1):
        self.score += points
        if self.score > self.best:
            self.best = self.score
        self.update_slow()
    
    def save_best(self):
            with open(self.score_path,'w') as score_file:
                score_file.write(str(self.best))

    def get_surface(self):
        surface = pg.font.SysFont('Verdana', self.font_size).render( f'Best : {self.best}  Score : {self.score}', True, 'white')
        return surface
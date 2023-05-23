
import pygame as pg
import os
from pygame._sdl2 import Image, Texture
from SpriteUnit import SpriteUnit
import Exfont
import Settings

class Score(SpriteUnit):
    def __init__(self, handler, images, x, y):
        self.images=images
        self.best=0
        self.score=0
        path = '.'
        try :
            path = pg.system.get_pref_path()
        except Exception as e:
            print(f'Erreur : {e}')
        self.score_path = os.path.join(path, 'score.txt')
        print(f'score file path : {self.score_path}')
        if os.path.exists(self.score_path):
            with open(self.score_path,'r') as score_file:
                self.best=int(score_file.read())
        super().__init__(handler, self.get_score_surface(self.best),x,y)

    def display_best(self):
        self.score=0
        self.update_image(Image(Texture.from_surface(self.handler.renderer, self.get_score_surface(0))))

    def reset(self):
        super().reset()
        self.score=0
        self.update_image(Image(Texture.from_surface(self.handler.renderer, self.get_score_surface(self.score))))

    def increment(self, points=1):
        self.score += points
        if self.score > self.best:
            self.best = self.score
        self.update_image(Image(Texture.from_surface(self.handler.renderer, self.get_score_surface(self.score))))
    
    def save_best(self):
            with open(self.score_path,'w') as score_file:
                score_file.write(str(self.best))

    def get_score_surface(self, score : int):
        prefix_best = Exfont.text_speech(pg.font.SysFont(None, Settings.FONT_SIZE), f'Best : ', 'white', True, 2, 'black')
        surface_best = Exfont.text_speech(pg.font.SysFont(None, Settings.FONT_SIZE), f'{self.best}', 'white', True, 2, 'black')
        prefix_score = Exfont.text_speech(pg.font.SysFont(None, Settings.FONT_SIZE), f'Score : ', 'white', True, 2, 'black')
        surface_score = Exfont.text_speech(pg.font.SysFont(None, Settings.FONT_SIZE), f'{score}', 'white', True, 2, 'black')
        w_prefix = max(prefix_best.get_width(),prefix_score.get_width())
        w = w_prefix+max(surface_best.get_width(),surface_score.get_width())
        h_best = max(prefix_best.get_height(),prefix_score.get_height())
        h = h_best + max(surface_best.get_height(),surface_score.get_height())
        score_surf = pg.Surface((w, h), pg.SRCALPHA)
        score_surf.blits(((prefix_best, (0, 0)),(prefix_score, (0, h_best)),(surface_best, (w_prefix, 0)),(surface_score, (w_prefix, h_best))), False)
        return score_surf

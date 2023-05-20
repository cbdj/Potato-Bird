
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
            print(e)
            pass
        self.score_path = os.path.join(path, 'score.txt')
        print(f'score file path : {self.score_path}')
        try:
            with open(self.score_path,'r') as score_file:
                self.best=int(score_file.read())
        except Exception as e:
            print(e)
            pass
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
        prefix_best = Exfont.text_speech(pg.font.SysFont(None, 3*Settings.FONT_SIZE), 'Best : ', 'white', True, 3, 'black')
        prefix_score = Exfont.text_speech(pg.font.SysFont(None, 3*Settings.FONT_SIZE), 'Score : ', 'white', True, 3, 'black')
        prefix_width = max(prefix_best.get_width(),prefix_score.get_width())
        score_width = prefix_width
        score_height = prefix_best.get_height() + prefix_score.get_height()
        str_score = str(score)
        str_best = str(self.best)
        if score > self.best:
            for c in str_score:
                score_width += self.images[c].get_width()
        else:
            for c in str_best:
                score_width += self.images[c].get_width()

        score_surf = pg.Surface((score_width, score_height), pg.SRCALPHA)
        tmp=0
        score_surf.blit(prefix_best, (tmp, 0))
        score_surf.blit(prefix_score, (tmp, prefix_best.get_height()))
        tmp+=prefix_width
        tmp2 = tmp
        for c in str_best:
            score_surf.blit(self.images[c], (tmp, 0))
            tmp+=self.images[c].get_width()
        for c in str_score:
            score_surf.blit(self.images[c], (tmp2, prefix_best.get_height()))
            tmp2+=self.images[c].get_width()
        return score_surf


import pygame as pg
from pygame import Surface
from pygame._sdl2 import Image, Texture
from .SpriteUnit import SpriteUnit
import Settings
import Exfont
import pygame.gfxdraw as gfx

class Menu(SpriteUnit):
    def __init__(self, handler, images, x, y, title : str, bird : Surface, font_size : int):
        surface = pg.Surface((x,y), pg.SRCALPHA)
        font = pg.font.SysFont(None, font_size)
        half_font = pg.font.SysFont(None, font_size//2)
        title = Exfont.text_speech(font, title, 'white', True, 2, 'black')
        get_ready = Exfont.text_speech(font, 'GET READY!', 'green', True, 2, 'black')
        def grayscale(surface : pg.Surface):
            ret = surface.copy()
            for x in range(surface.get_width()):
                for y in range(surface.get_height()):
                    pixel: pg.Color = surface.get_at((x, y))
                    grey_pixel = 0.299 * pixel.r + 0.587 * pixel.g + 0.114 * pixel.b
                    ret.set_at((x,y), (grey_pixel, grey_pixel, grey_pixel, pixel.a))
            return ret
        grey_bird = grayscale(bird)
        index_w = index_w_bird = surface.get_width()//2-grey_bird.get_width()//2
        index_h = index_h_bird = surface.get_height()//2 - grey_bird.get_height()//2
        surface.blit(grey_bird, (index_w, index_h))
        index_w = surface.get_width()//2-get_ready.get_width()//2
        index_h -= 2*get_ready.get_height()
        surface.blit(get_ready, (index_w, index_h))
        index_w = surface.get_width()//2-title.get_width()//2
        index_h -= 2*title.get_height()
        surface.blit(title, (index_w, index_h))
        # Building arrows
        gfx.box(surface, (index_w_bird - 2*grey_bird.get_width(), index_h_bird, grey_bird.get_width(), grey_bird.get_height()), (255,0,0))
        gfx.box(surface, (index_w_bird + 2*grey_bird.get_width(), index_h_bird, grey_bird.get_width(), grey_bird.get_height()), (255,0,0))
        gfx.filled_trigon(surface,index_w_bird - grey_bird.get_width(), index_h_bird, index_w_bird, index_h_bird + grey_bird.get_height()//2,index_w_bird - grey_bird.get_width(), index_h_bird +2*grey_bird.get_height()//2, (255,0,0))
        gfx.filled_trigon(surface,index_w_bird + 2*grey_bird.get_width(), index_h_bird, index_w_bird + grey_bird.get_width(), index_h_bird + grey_bird.get_height()//2,index_w_bird + 2*grey_bird.get_width(), index_h_bird +2*grey_bird.get_height()//2, (255,0,0))
        # Building arrows legends
        tap = Exfont.text_speech(half_font, 'TAP!', 'white', True, 1, 'black')
        surface.blit(tap, (index_w_bird - 3*grey_bird.get_width()/2, index_h_bird+grey_bird.get_height()/4))
        surface.blit(tap, (index_w_bird + 3*grey_bird.get_width()/2, index_h_bird+grey_bird.get_height()/4))
        super().__init__(handler, surface, x, y)

   
import pygame as pg
from pygame import Surface
from pygame._sdl2 import Image, Texture
from .SpriteUnit import SpriteUnit
import Settings
import Exfont
import pygame.gfxdraw as gfx

class Menu(SpriteUnit):
    def __init__(self, handler, x, y, title : str, bird : Surface, font_size : int, scale = 1.0):
        x,y=int(x),int(y)
        surface = pg.Surface((2*x,2*y), pg.SRCALPHA)
        font = pg.font.Font(None, font_size)
        half_font = pg.font.Font(None, font_size//2)
        def upscale(surface, scale):
            return pg.transform.scale(surface, (surface.get_rect().w * scale, surface.get_rect().h * scale))
        title = upscale(Exfont.text_speech(font, title, 'white', True, 2, 'black'), scale)
        get_ready = upscale(Exfont.text_speech(font, 'GET READY!', 'green', True, 2, 'black'), scale)
        grey_bird = pg.transform.grayscale(bird)
        pos_x, pos_y = x,y
        surface.blit(grey_bird, (pos_x-grey_bird.get_width()//2, pos_y-grey_bird.get_height()//2))
        pos_y -= 2*get_ready.get_height()
        surface.blit(get_ready, (pos_x-get_ready.get_width()//2, pos_y-get_ready.get_height()//2))
        pos_y -= 2*title.get_height()
        surface.blit(title, (pos_x-title.get_width()//2, pos_y-title.get_height()//2))
        tap = upscale(Exfont.text_speech(half_font, 'TAP!', 'white', True, 1, 'black'), scale)
        # Building arrows
        gfx.box(surface, (x - grey_bird.get_width() - 1.2*tap.get_width(), y-tap.get_height()//2, 1.2*tap.get_width(), tap.get_height()), (255,0,0))
        gfx.filled_trigon(surface,x - grey_bird.get_width(), y-tap.get_height()//2, x-grey_bird.get_width()//2,y ,x - grey_bird.get_width() , y +tap.get_height()//2, (255,0,0))
        gfx.box(surface, (x + grey_bird.get_width(), y-tap.get_height()//2, 1.2*tap.get_width(), tap.get_height()), (255,0,0))
        gfx.filled_trigon(surface,x + grey_bird.get_width(), y-tap.get_height()//2, x + grey_bird.get_width()//2, y ,x + grey_bird.get_width(), y +tap.get_height()//2, (255,0,0))
        # Building arrows legends
        surface.blit(tap, (x - grey_bird.get_width() - 1.1*tap.get_width(), y-tap.get_height()//2))
        surface.blit(tap, (x  + grey_bird.get_width() + 0.1*tap.get_width(), y-tap.get_height()//2))
        super().__init__(handler, surface, x, y)

   
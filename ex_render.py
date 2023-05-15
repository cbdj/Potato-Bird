import pygame, pygame.font, pygame.image
from pygame.locals import *
import pygame as pg


def textHollow(font, message, fontcolor):
    notcolor = [c^0xFF for c in fontcolor]
    base, rect = font.render(message, 0, pg.color.Color(*fontcolor), pg.color.Color(*notcolor))
    size = rect.width, rect.height
    img = pygame.Surface(size, 16)
    img.fill(pg.color.Color(*notcolor))
    base.set_colorkey(0)
    img.blit(base, (0, 0))
    img.blit(base, (2, 0))
    img.blit(base, (0, 2))
    img.blit(base, (2, 2))
    base.set_colorkey(0)
    # base.set_palette_at(1, pg.color.Color(*notcolor))
    img.blit(base, (1, 1))
    img.set_colorkey(pg.color.Color(*notcolor))
    return img

def textOutline(font, message, fontcolor, outlinecolor):
    base, rect = font.render(message, 0, fontcolor)
    outline = textHollow(font, message, outlinecolor)
    img = pygame.Surface(outline.get_size(), 16)
    img.blit(base, (1, 1))
    img.blit(outline, (0, 0))
    img.set_colorkey(0)
    return img
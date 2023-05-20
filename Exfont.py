import pygame as pg

def text_speech(font : pg.font.Font, text : str, color : pg.Color, bold : bool, outline: int, outline_color : pg.Color):
    # font = pygame.font.Font(font,size)
    font.set_bold(bold)
    if outline > 0:
        outlineSurf = font.render(text, True, outline_color)
        outlineSize = outlineSurf.get_size()
        textSurf = pg.Surface((outlineSize[0] + outline*2, outlineSize[1] + 2*outline), pg.SRCALPHA)
        textRect = textSurf.get_rect()
        offsets = [(ox, oy) 
            for ox in range(-outline, 2*outline, outline)
            for oy in range(-outline, 2*outline, outline)
            if ox != 0 or ox != 0]
        for ox, oy in offsets:   
            px, py = textRect.center
            textSurf.blit(outlineSurf, outlineSurf.get_rect(center = (px+ox, py+oy))) 
        innerText = font.render(text, True, color)
        textSurf.blit(innerText, innerText.get_rect(center = textRect.center)) 
    else:
        textSurf = font.render(text, True, color)
    return textSurf
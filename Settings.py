import pygame as pg
# WIN_SIZE = WIN_W, WIN_H = 336, 512
WIN_SIZE = WIN_W, WIN_H = 1280, 512
SPRITE_DIR_PATH = 'flappy-bird-assets/sprites'
PIPE_DENSITY = 6
BUMP_SPEED = 300
FONT_SIZE = 40
SPEED = 100 # initial pipe and base speed
SPEED_INCREASE_FACTOR = 1.3 # speed increase at each day/night event
DAY_NIGHT_TIME_MS = 3000
EVENT_DAY_NIGHT = pg.USEREVENT+1

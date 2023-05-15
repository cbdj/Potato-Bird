import pygame as pg
import sys
import os

try:
# PyInstaller creates a temp folder and stores path in _MEIPASS
    base_path = sys._MEIPASS
except Exception:
    base_path = os.path.abspath(".")

# WIN_SIZE = WIN_W, WIN_H = 336, 512
WIN_SIZE = WIN_W, WIN_H = 1280, 512
ASSETS_DIR_PATH = base_path + '/assets'
SPRITE_DIR_PATH = ASSETS_DIR_PATH + '/sprites'
PIPE_DENSITY = 6
BUMP_SPEED = 300
FONT_SIZE = 20
SPEED = 100 # initial pipe and base speed
SPEED_INCREASE_FACTOR = 1.3 # speed increase at each day/night event
DAY_NIGHT_TIME_MS = 10000
EVENT_DAY_NIGHT = pg.USEREVENT+1

import pygame as pg
import sys
import os

try:
# PyInstaller creates a temp folder and stores path in _MEIPASS
    base_path = sys._MEIPASS
except Exception:
    base_path = os.path.abspath(".")

# Those two settings will be identified at app startup depending on screen resolution and assets dimensions
WIN_W = 0
WIN_H = 0

# CONSTANTS
ASSETS_DIR_PATH = base_path + '/assets'
SPRITE_DIR_PATH = ASSETS_DIR_PATH + '/sprites'
AUDIO_DIR_PATH = ASSETS_DIR_PATH + '/audio'
PIPE_DENSITY = 6
BUMP_SPEED = 300
FONT_SIZE = 20
SPEED = 100 # initial pipe and base speed
SPEED_INCREASE_FACTOR = 1.3 # speed increase at each day/night event
DAY_NIGHT_TIME_MS = 10000
EVENT_DAY_NIGHT = pg.USEREVENT+1

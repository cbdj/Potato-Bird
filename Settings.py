import pygame as pg
import sys
import os

from sys import platform as _sys_platform
import os

def get_platform():
    if 'ANDROID_ARGUMENT' in os.environ:
        return "android"
    elif _sys_platform in ('linux', 'linux2','linux3'):
        return "linux"
    elif _sys_platform in ('win32', 'cygwin'):
        return 'win'
platform = get_platform()
if platform=="android":
    base_path=os.path.abspath("/data/data/org.cbdj.flappy/files/app/")
elif platform=="win":
    try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
elif platform=="linux":
    base_path = os.path.abspath(".")

# Those two settings will be identified at app startup depending on screen resolution and assets dimensions
WIN_W = 0
WIN_H = 0

# CONSTANTS
USE_OFFICIAL_ASSETS = False
if USE_OFFICIAL_ASSETS : 
    ASSETS_DIR_PATH = os.path.join(base_path,'official_assets')
else:
    ASSETS_DIR_PATH = os.path.join(base_path,'assets')
SPRITE_DIR_PATH = os.path.join(ASSETS_DIR_PATH , 'sprites')
AUDIO_DIR_PATH = os.path.join(ASSETS_DIR_PATH, 'audio')
BIRD_COLOR = 'yellow'
PIPE_DENSITY = 6
BUMP_SPEED = 300
FONT_SIZE = 40
SPEED = 100 # initial pipe and base speed
SPEED_INCREASE_FACTOR = 1.3 # speed increase at each day/night event
DAY_NIGHT_TIME_MS = 10000
EVENT_DAY_NIGHT = pg.USEREVENT+1
BIRD_MASS_KG = 0.1

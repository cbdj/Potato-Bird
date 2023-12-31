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

package_domain="com.cldejessey"
package_name="flappy"
# try :
#     base_path = pg.system.get_pref_path(package_domain,package_name)
# except:
if platform=="android":
    base_path=os.path.abspath(f"/data/data/{package_domain}.{package_name}/files/app/")
elif platform=="win":
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
else:
    base_path = os.path.abspath(".")
print(f"base path : {base_path}")
# Those two settings will be identified at app startup depending on screen resolution and assets dimensions
WIN_W = 0
WIN_H = 0

# CONSTANTS
INTERSTITIAL_ID="ca-app-pub-4493613666001226/1483234688"
BANNER_ID="ca-app-pub-4493613666001226/5140290547"
TITLE = 'Potato Bird'
FULLSCREEN= platform == "android"
FPS = 120
ASSETS_DIR_PATH = os.path.join(base_path,'assets')
SPRITE_DIR_PATH = os.path.join(ASSETS_DIR_PATH , 'sprites')
PARTICLES_DIR_PATH = os.path.join(ASSETS_DIR_PATH , 'particles')
AUDIO_DIR_PATH = os.path.join(ASSETS_DIR_PATH, 'audio')
BIRD_COLOR = 'yellow'
PIPE_DENSITY = 6
BUMP_SPEED = 400
FONT_SIZE = 40
SPEED = 120 # initial pipe and base speed 
speed_multiplier = 1.0 # parameter that can be modified in configuration menu
SPEED_INCREASE_FACTOR = 10 # speed increase at each day/night event
DAY_NIGHT_TIME_MS = 10000
EVENT_DAY_NIGHT = pg.event.custom_type()
BIRD_MASS_KG = 0.15

AD_TIME_MS = 30000
EVENT_AD = pg.event.custom_type()
EVENT_SOUND = pg.event.custom_type()
SHAKE_SCREEN = pg.event.custom_type()
INCREMENT_SPEED = pg.event.custom_type()

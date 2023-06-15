import pathlib
import pygame as pg

class SoundHandler:
    def __init__(self, sounds_path):
        
        def load_sounds(sounds_path):
            """ from .ogg to pygame Sound """
            exts=['.ogg','.mp3']
            sounds = dict([(path.stem, pg.mixer.Sound(str(path))) for path in pathlib.Path(sounds_path).rglob('*.*') if path.is_file() and path.suffix in exts])
            return sounds
        self.sounds = load_sounds(sounds_path)
        self._muted = False

    def play(self, sound : str):
        if not self._muted:
            self.sounds[sound].play()

    def mute(self):
        self._muted = True

    def unmute(self):
        self._muted = False
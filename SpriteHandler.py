import Settings
from Background import Background
from Base import Base
from Pipe import Pipe
from Bird import Bird
from Score import Score
import pygame as pg
from pygame._sdl2.video import Image, Texture
import pathlib
from random import randrange, uniform
from SpriteUnit import SpriteUnit
import time

class SpriteHandler:
    def __init__(self, app):
        self.app = app
        self.renderer = self.app.renderer
        self.images = self.load_images() # load textures from *.jpg
        self.sounds = self.load_sounds()

        # Adapting dimensions to screen resolution
        Settings.WIN_W, Settings.WIN_H = self.compute_size()
        screen_info = pg.display.Info()
        scale_w= screen_info.current_w/Settings.WIN_W
        scale_h= screen_info.current_h/Settings.WIN_H
        self.scale = min(scale_w, scale_h)
        Settings.WIN_W = float(Settings.WIN_W)*float(screen_info.current_w)//(float(Settings.WIN_W)*self.scale)
        self.extend_world(Settings.WIN_W)

        # Creating backgrounds sprites
        self.background = Background(self, self.images['background-day'], self.images['background-night'], Settings.WIN_W//2, (Settings.WIN_H-self.images['base'].get_height())//2 )
            
        # Creating Pipes sprites
        pipe_default_ypos = Settings.WIN_H + self.images['pipe-green'].get_height()//2 - self.images['base'].get_height()
        pipe_reversed_default_ypos = -self.images['pipe-green'].get_height()//2
        self.pipes = []
        x=-self.images['pipe-green'].get_width()
        for i in range(Settings.PIPE_DENSITY):
            self.pipes.append((Pipe(self, self.images['pipe-green'],x, pipe_default_ypos ),Pipe(self, self.images['reversed-pipe-green'],x, pipe_reversed_default_ypos)))

        # Creating Base sprite
        self.base=Base(self, self.images['base'], Settings.WIN_W, Settings.WIN_H-self.images['base'].get_height()//2)

        # Creating Bird sprite
        self.bird = Bird(self, self.images['yellowbird-downflap'], self.images['yellowbird-midflap'], self.images['yellowbird-upflap'], Settings.WIN_W // 2, Settings.WIN_H // 2)

        # Creating menu
        self.menu = SpriteUnit(self,self.images['message'], Settings.WIN_W // 2, Settings.WIN_H // 2)
        self._gameover = SpriteUnit(self,self.images['gameover'], Settings.WIN_W // 2, Settings.WIN_H // 2)
        self.score=Score(self,self.images, Settings.WIN_W // 2, Settings.WIN_H //6)

        # Creating groups
        self.group_background = pg.sprite.GroupSingle(self.background)
        self.group_collide = pg.sprite.Group(self.pipes, self.base) # special group for sprites that Bird can collide on
        self.group_bird = pg.sprite.GroupSingle(self.bird)
        self.group_foreground = pg.sprite.Group(self.score)
        
        self._started = False
        self._paused = False

        self.pipe_width = self.images['pipe-green'].get_width()
        self.pipe_requeue_interval = self.rand_pipe_requeue_interval(Settings.SPEED)
        self.pipe_reque_time = 0.0
        self.reset()

    def reset(self):
        self.day=True
        self._started = False
        self._paused = False
        self.background.reset()
        self.score.reset()
        self.score.display_best()
        self.bird.x = self.bird.orig_x
        self.bird.y = self.bird.orig_y 
        for pipe, pipe_reversed in self.pipes:
            pipe.x = pipe_reversed.x = pipe.orig_x
            pipe.point_given = True
        self.group_foreground.empty()
        self.group_foreground.add(self.menu, self.score)
        self.update_speed(Settings.SPEED)
        self.app.dt=0.0
        self.group_background.update()
        self.group_collide.update()
        self.group_bird.update()
        self.group_foreground.update()
           
    def count_sprites(self):
        return len(self.group_bird) + len(self.group_collide) + len(self.group_background) + len(self.group_foreground)

    def rand_pipe_requeue_interval(self, speed):
        interval = uniform(2.0,8.0)*(1000.0*(float(self.pipe_width))//float(speed))*0.001
        return interval
    
    def update_speed(self, speed):
        self.base.vel_x = -speed
        for (pipe, pipe_reversed) in self.pipes :
            pipe.vel_x = -speed
            pipe_reversed.vel_x = -speed
        if speed > 0:
            self.pipe_requeue_interval = self.rand_pipe_requeue_interval(speed)

    def compute_size(self):
        w = self.images['background-day'].get_width()
        h = self.images['background-day'].get_height() + self.images['base'].get_height()
        return w,h

    def load_images(self):
        """ from .png to pygame Surfaces """
        images = dict([(path.stem, pg.image.load(str(path))) for path in pathlib.Path(Settings.SPRITE_DIR_PATH).rglob('*.png') if path.is_file()])
        images.update(dict([(f'reversed-{path.stem}', pg.transform.flip(pg.image.load(str(path)), False, True)) for path in pathlib.Path(Settings.SPRITE_DIR_PATH).rglob('*.png') if path.is_file() and 'pipe' in str(path)]))
        return images
    
    def extend_world(self, new_width):
        def extend_image(image, new_width):
            extended_image = pg.Surface((new_width, image.get_height()))
            for i in range(1+int(new_width//image.get_width())):
                extended_image.blit(image, (i*image.get_width(), 0))
            return extended_image
        
        # extend base and background to match screen width
        self.images['background-day'] = extend_image(self.images['background-day'], new_width)
        self.images['background-night'] = extend_image(self.images['background-night'], new_width)
        self.images['base'] = extend_image(self.images['base'], 2*new_width)

    def load_sounds(self):
        """ from .ogg to pygame Sound """
        sounds = dict([(path.stem, pg.mixer.Sound(str(path))) for path in pathlib.Path(Settings.AUDIO_DIR_PATH).rglob('*.ogg') if path.is_file()])
        return sounds


    def maybe_requeue_pipes(self):

        def pipe_requeue(pipe, pipe_reversed):
            """ 
            Reque pipes 
            Used when pipes are out of camera range
            """
            pipe.y = pipe.orig_y - randrange(pipe.rect.height//2, 2*pipe.rect.height//3)
            pipe_reversed.y = pipe_reversed.orig_y + randrange(pipe.rect.height//2, 3*pipe.rect.height//4)
            pipe.x = pipe_reversed.x = Settings.WIN_W + pipe.rect.width//2

        self.pipe_reque_time += self.app.dt
        if self.pipe_reque_time > self.pipe_requeue_interval:
            for (pipe1,pipe2) in self.pipes:
                if pipe1.x < -pipe1.rect.width :
                    # requeue one Pipe that is out of screen
                    self.pipe_reque_time = 0.0
                    self.pipe_requeue_interval = self.rand_pipe_requeue_interval(-pipe1.vel_x)
                    pipe_requeue(pipe1, pipe2)
                    break

    def update_score(self):
        for (pipe1,pipe2) in self.pipes:
            if pipe1.x < self.bird.x and not pipe1.point_given:
                self.sounds['point'].play()
                self.score.increment()
                pipe1.point_given = True
            if pipe1.x > self.bird.x:
                pipe1.point_given = False


    def update(self):
        if self._paused:
            return
        if not self._started:
            return
        self.update_score()
        self.maybe_requeue_pipes()
                
        # Update bird's wings position
       
        self.group_background.update()
        self.group_collide.update()
        self.group_bird.update()
        self.group_foreground.update()

    def draw(self):
        self.group_background.draw(self.renderer)
        self.group_collide.draw(self.renderer)
        self.group_bird.draw(self.renderer)
        self.group_foreground.draw(self.renderer)

    def on_mouse_press(self):
        mouse_button = pg.mouse.get_pressed()
        if mouse_button[0]:
            x, y = pg.mouse.get_pos()
            self.on_action()
        elif mouse_button[2]:
            pass

    def on_key_press(self, key):
        if key == pg.K_SPACE:
            self.on_action()

    def on_action(self):
        if self._paused:
            self._paused = False
            self.reset()
        elif not self._started:
            self.start()
            self.bird.bump(Settings.BUMP_SPEED)
        else:
            self.bird.bump(Settings.BUMP_SPEED)

    def start(self):
        self.app.speed=Settings.SPEED
        self.score.reset()
        self.group_foreground.empty()
        self.group_foreground.add(self.score)
        self.update_speed(Settings.SPEED)
        self._started = True

    def stop(self):
        self.update_speed(0)
        self._started = False

    def game_over(self):
        self.group_foreground.add(self._gameover)
        self.score.save_best()
        self.update_speed(0)
        self._paused = True

    def quit(self):
        self.score.save_best()

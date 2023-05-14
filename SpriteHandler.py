from Settings import *
from Base import Base
from Pipe import Pipe
from Bird import Bird
import pygame as pg
from pygame._sdl2.video import Image
import pathlib
from random import randrange
from SpriteUnit import SpriteUnit

class SpriteHandler:
    def __init__(self, app):
        self.app = app
        self.renderer = self.app.renderer
        self.images = self.load_images() # load textures from *.jpg

        # Creating backgrounds sprites
        self.background = Base(self, self.images['background-day'], WIN_W//2, WIN_H//2)
            
        # Creating Pipes sprites
        pipe_default_ypos = WIN_H + self.images['pipe-green'].get_height()//2 - self.images['base'].get_height()
        pipe_reversed_default_ypos = -self.images['pipe-green'].get_height()//2
        self.pipes = []
        x=-self.images['pipe-green'].get_width()
        for i in range(PIPE_DENSITY):
            self.pipes.append((Pipe(self, self.images['pipe-green'],x, pipe_default_ypos ),Pipe(self, self.images['reversed-pipe-green'],x, pipe_reversed_default_ypos)))

        # Creating Base sprite
        self.base=Base(self, self.images['base'], WIN_W, WIN_H-self.images['base'].get_height()//2)

        # Creating Bird sprite
        self.bird = Bird(self, self.images['yellowbird-midflap'], WIN_W // 2, WIN_H // 2)

        # Creating menu
        self.menu = SpriteUnit(self,self.images['message'], WIN_W // 2, WIN_H // 2)
        self.gameover = SpriteUnit(self,self.images['gameover'], WIN_W // 2, WIN_H // 2)

        # Creating groups
        self.group_background = pg.sprite.GroupSingle(self.background)
        self.group_collide = pg.sprite.Group() # special group for sprites that Bird can collide on
        self.group_bird = pg.sprite.GroupSingle(self.bird)
        self.group_foreground = pg.sprite.Group()

        # Adding sprites to respective groups
        for pipe, pipe_reversed in self.pipes:
            self.group_collide.add(pipe,pipe_reversed)
        self.group_collide.add(self.base)
        
        self.day=True
        self._started = False
        self._paused = False

        self.pipe_requeue_interval = (WIN_W//(len(self.pipes)+1))//SPEED
        self.pipe_reque_time = 0.0
        self.reset()

    def reset(self):
        self.day=True
        self._started = False
        self._paused = False
        self.background.update_image(self.images['background-day'])
        self.bird.x = self.bird.orig_x
        self.bird.y = self.bird.orig_y 
        for i in range(len(self.pipes)):
            self.pipes[i][0].x= self.pipes[i][1].x = -self.images['pipe-green'].get_width()
        self.group_foreground.empty()
        self.group_foreground.add(self.menu)
        self.update_speed(SPEED)
        self.app.dt=0.0
        self.group_background.update()
        self.group_collide.update()
        self.group_bird.update()
        self.group_foreground.update()
           
    def count_sprites(self):
        return len(self.group_bird) + len(self.group_collide) + len(self.group_background)
    
    def toggle_day(self):
        if self._paused:
            return
        if self.day:
            image = self.images['background-night']
        else:
            image = self.images['background-day']
        self.background.update_image(image)
        self.day = not self.day

    def update_speed(self, speed):
        self.base.vel_x = -speed
        for (pipe, pipe_reversed) in self.pipes :
            pipe.vel_x = -speed
            pipe_reversed.vel_x = -speed
        if speed > 0:
            self.pipe_requeue_interval = (1000*(float(WIN_W)//float(len(self.pipes)+1))//float(speed))*0.001
            print(self.pipe_requeue_interval)

    def load_images(self):
        """ from .png to pygame Textures"""
        images = dict([(path.stem, pg.image.load(str(path))) for path in pathlib.Path(SPRITE_DIR_PATH).rglob('*.png') if path.is_file()])
        images.update(dict([(f'reversed-{path.stem}', pg.transform.flip(pg.image.load(str(path)), False, True)) for path in pathlib.Path(SPRITE_DIR_PATH).rglob('*.png') if path.is_file() and 'pipe' in str(path)]))
        
        def extend_image(image, new_width):
            extended_image = pg.Surface((new_width, image.get_height()), pg.SRCALPHA)
            for i in range(1+int(new_width//image.get_width())):
                extended_image.blit(image, (i*image.get_width(), 0))
            return extended_image
        
        images['background-day'] = extend_image(images['background-day'], WIN_W)
        images['background-night'] = extend_image(images['background-night'], WIN_W)
        images['base'] = extend_image(images['base'], 2*WIN_W)
        
        return images
        

    def pipe_requeue(self, pipe, pipe_reversed):
        """ 
        Reque pipes 
        Used when pipes are out of camera range
        """
        pipe.y = pipe.orig_y - randrange(pipe.rect.height//4, pipe.rect.height//2)
        pipe_reversed.y = pipe_reversed.orig_y + randrange(pipe.rect.height//4, pipe.rect.height//2)
        pipe.x = pipe_reversed.x = WIN_W + randrange(pipe.rect.width//2, (WIN_W//(len(self.pipes)+1))-pipe.rect.width//2 )

    def update(self):
        if self._paused:
            return
        if not self._started:
            return
        self.pipe_reque_time += self.app.dt
        # print(self.pipe_reque_time)
        if self.pipe_reque_time > self.pipe_requeue_interval:
            for (pipe1,pipe2) in self.pipes:
                # requeue Pipes that are out of screen
                if pipe1.x < -pipe1.rect.width :
                    self.pipe_reque_time = 0.0
                    self.pipe_requeue(pipe1, pipe2)
                    break
                
        # Update bird's wings position
        if self.bird.vel_y > BUMP_SPEED//10:
            self.bird.update_image(self.images['yellowbird-upflap'])
        elif self.bird.vel_y < -BUMP_SPEED//10: 
            self.bird.update_image(self.images['yellowbird-downflap'])
        else : 
            self.bird.update_image(self.images['yellowbird-midflap'])
       
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
            self.bird.bump(BUMP_SPEED)
        else:
            self.bird.bump(BUMP_SPEED)

    def start(self):
        self.app.speed=SPEED
        self.group_foreground.empty()
        self.update_speed(SPEED)
        self._started = True

    def stop(self):
        self.update_speed(0)
        self._started = False

    def pause(self):
        self.group_foreground.add(self.gameover)
        self.update_speed(0)
        self._paused = True

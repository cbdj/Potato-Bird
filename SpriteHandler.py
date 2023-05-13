from Settings import *
from Base import Base
from Pipe import Pipe
from Bird import Bird
import pygame as pg
from pygame._sdl2.video import Texture
import pathlib
from random import randrange

class SpriteHandler:
    def __init__(self, app):
        self.app = app
        self.renderer = self.app.renderer
        self.images = self.load_images() # load textures from *.jpg

        # Adding backgrounds sprites
        x = 0
        self.backgrounds=[]
        while x < WIN_W + self.images['background-day'].width:
            self.backgrounds.append(Base(self, self.images['background-day'], x, WIN_H/2))
            x+=self.images['background-day'].width
            
        # Adding Pipes sprites
        pipe_default_ypos = WIN_H - self.images['pipe-green'].height//2 - self.images['base'].height//2
        pipe_reversed_default_ypos = -self.images['pipe-green'].height//2 - self.images['base'].height//2
        self.pipes = []
        for i in range(PIPE_DENSITY):
            x=WIN_W + i*WIN_W//PIPE_DENSITY
            self.pipes.append((Pipe(self, self.images['pipe-green'],x, pipe_default_ypos ),Pipe(self, self.images['reversed-pipe-green'],x, pipe_reversed_default_ypos)))
        for pipe1, pipe2 in self.pipes:
            self.pipe_requeue(pipe1, pipe2)

        # Adding Bases sprites
        x = 0
        self.bases=[]
        while x < WIN_W + self.images['base'].width:
            self.bases.append(Base(self, self.images['base'], x, WIN_H-self.images['base'].height//2))
            x+=self.images['base'].width //2

        # Adding Bird sprite
        self.bird = Bird(self, self.images['yellowbird-midflap'], WIN_W // 2, WIN_H // 2)

        self.group_bird = pg.sprite.GroupSingle()
        self.group_collide = pg.sprite.Group() # special group for sprites that Bird can collide on
        self.group_background = pg.sprite.Group()
        
        for background in self.backgrounds:
            self.group_background.add(background)
        for pipe1, pipe2 in self.pipes:
            self.group_collide.add(pipe1)
            self.group_collide.add(pipe2)
        for base in self.bases:
            self.group_collide.add(base)
        self.group_bird.add(self.bird)

        self.day=True
        self.started=False
        
    def count_sprites(self):
        return len(self.group_bird) + len(self.group_collide) + len(self.group_background)
    
    def toggle_day(self):
        if self.day:
            image = self.images['background-night']
        else:
            image = self.images['background-day']
        for background in self.group_background:
            background.update_image(image)
        self.day = not self.day

    def update_speed(self, speed):
        # print(speed)
        for base in self.bases :
            base.vel_x = -speed
        for (pipe, pipe_reversed) in self.pipes :
            pipe.vel_x = -speed
            pipe_reversed.vel_x = -speed

    def load_images(self):
        images = dict([(path.stem, Texture.from_surface(self.renderer, pg.image.load(str(path)))) for path in pathlib.Path(SPRITE_DIR_PATH).rglob('*.png') if path.is_file()])
        images.update(dict([(f'reversed-{path.stem}', Texture.from_surface(self.renderer, pg.transform.flip(pg.image.load(str(path)), False, True))) for path in pathlib.Path(SPRITE_DIR_PATH).rglob('*.png') if path.is_file() and 'pipe' in str(path)]))
        return images

    def pipe_requeue(self, pipe1, pipe2):
        pipe1.y = pipe1.orig_y + pipe1.rect.height//2 + randrange(-pipe1.rect.height//4, pipe1.rect.height//4)
        pipe2.y = pipe2.orig_y + pipe2.rect.height//2 + randrange(-pipe2.rect.height//4, pipe2.rect.height//4)
        pipe1.x = pipe2.x = pipe1.orig_x + randrange(0, WIN_W//4)

    def update(self):
        for (pipe1,pipe2) in self.pipes:
            # requeue Pipes that are out of screen
            if pipe1.x < -pipe1.rect.width :
                self.pipe_requeue(pipe1, pipe2)

        if self.bird.vel_y > BUMP_SPEED//10:
            self.bird.update_image(self.images['yellowbird-upflap'])
        elif self.bird.vel_y < -BUMP_SPEED//10: 
            self.bird.update_image(self.images['yellowbird-downflap'])
        else : 
            self.bird.update_image(self.images['yellowbird-midflap'])
       
        self.group_background.update()
        self.group_collide.update()
        self.group_bird.update()

    def draw(self):
        self.group_background.draw(self.renderer)
        self.group_collide.draw(self.renderer)
        self.group_bird.draw(self.renderer)

    def on_mouse_press(self):
        mouse_button = pg.mouse.get_pressed()
        if mouse_button[0]:
            if not self.started:
                self.start()
            x, y = pg.mouse.get_pos()
            self.bird.bump(BUMP_SPEED)
        elif mouse_button[2]:
            pass

    def on_key_press(self, key):
        if key == pg.K_SPACE:
            if not self.started:
                self.start()
            self.bird.bump(BUMP_SPEED)

    def start(self):
        self.update_speed(SPEED)
        self.bird.dead=False
        self.started = True

    def stop(self):
        self.update_speed(0)
        self.bird.dead=True
        self.started = False
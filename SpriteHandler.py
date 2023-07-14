import Settings
from Sprites.Background import Background
from Sprites.Base import Base
from Sprites.Pipe import Pipe
from Sprites.Bird import Bird
from Sprites.Bull import Bull
from Sprites.Score import Score, Best
from Sprites.Menu import Menu
from Sprites.Button import Button
from Sprites.Water import Wave
from Sprites.SpriteUnit import SpriteUnit
import pygame as pg
import pathlib
from random import randrange, uniform, random
import Exfont

class SpriteHandler:
    def __init__(self, app):
        self.app = app
        self.renderer = self.app.renderer
        self.images = self.load_png(Settings.SPRITE_DIR_PATH)
        self.particles = self.load_png(Settings.PARTICLES_DIR_PATH)

        screen_info = pg.display.Info()
        Settings.WIN_W, Settings.WIN_H = screen_info.current_w,screen_info.current_h
        # Adapting dimensions to screen resolution
        background_sprite_w, background_sprite_h = self.compute_size()
        scale = screen_info.current_h/background_sprite_h
        Settings.BUMP_SPEED = Settings.BUMP_SPEED * scale
        Settings.SPEED = Settings.SPEED * scale
        Bull.speed_increment = Bull.speed_increment * scale
        Settings.SPEED_INCREASE_FACTOR = Settings.SPEED_INCREASE_FACTOR * scale
        Settings.BIRD_MASS_KG = Settings.BIRD_MASS_KG * scale
        for key, image in self.images.items():
            self.images[key] = pg.transform.scale(image, (image.get_rect().w * scale, image.get_rect().h * scale))
        self.extend_world(Settings.WIN_W)

        # Creating backgrounds sprites
        self.background = Background(self, self.images['background-day'], self.images['background-night'], Settings.WIN_W//2, Settings.WIN_H//2 )
            
        # Creating Pipes sprites
        h = self.images['pipe-green'].get_height()
        pipe_default_ypos = Settings.WIN_H + h/2 - h/3
        pipe_reversed_default_ypos = pipe_default_ypos - h - 4*self.images[Settings.BIRD_COLOR + 'bird-midflap'].get_height()
        self.pipes = []
        x=-self.images['pipe-green'].get_width()/2 # pipes are hidden on the left of the screen by default
        for i in range(Settings.PIPE_DENSITY):
            self.pipes.append((Pipe(self, self.images['pipe-green'],x, pipe_default_ypos ),Pipe(self, self.images['reversed-pipe-green'],x, pipe_reversed_default_ypos)))

        # Creating Base sprite
        # self.base=Base(self, self.images['base'], self.images['base'].get_width()/2, Settings.WIN_H-self.images['base'].get_height()/2)
        rect = pg.Rect(self.images['base'].get_width()/2,Settings.WIN_H-self.images['base'].get_height()/2,self.images['base'].get_width(), self.images['base'].get_height())
        print(rect)
        self.base=Wave(self, rect)

        # Creating Bird sprite
        trainee = pg.transform.scale(self.particles['smoke'],(1.5*self.images[Settings.BIRD_COLOR + 'bird-downflap'].get_rect().height, 1.5*self.images[Settings.BIRD_COLOR + 'bird-downflap'].get_rect().height))
        trainee.set_alpha(50)
        def offset_color(surface: pg.Surface, offset):
            for i in range(surface.get_width()):
                for j in range(surface.get_height()):
                    pixel = surface.get_at((i,j))
                    pixel.r = min(max(0,pixel.r+offset),255)
                    pixel.g = min(max(0,pixel.g+offset),255)
                    pixel.b = min(max(0,pixel.b+offset),255)
                    surface.set_at((i,j), pixel)
        offset_color(trainee,60)
        self.bird = Bird(self, self.images[Settings.BIRD_COLOR + 'bird-downflap'], self.images[Settings.BIRD_COLOR + 'bird-midflap'], self.images[Settings.BIRD_COLOR + 'bird-upflap'], Settings.WIN_W // 2, Settings.WIN_H // 2, Settings.BUMP_SPEED, Settings.BIRD_MASS_KG, trainee)
        self.bull = Bull(self, self.images['bull'],x,Settings.WIN_H//2)
        # Creating menu
        if Settings.USE_OFFICIAL_ASSETS:
            self.menu = SpriteUnit(self, self.images['message'], Settings.WIN_W / 2, Settings.WIN_H / 2)
        else:
            self.menu = Menu(self, Settings.WIN_W / 2, Settings.WIN_H / 2, Settings.TITLE, self.images[Settings.BIRD_COLOR + 'bird-midflap'], Settings.FONT_SIZE, scale)
        def show_leaderboard():
            if Settings.platform == 'android' and len(self.leaderboards) > 0:
                id = list(self.leaderboards.keys())[-1]
                print(f"showing {id}")
                self.app.playgamesservices.leaderboards_client.show_leaderboard(id)
        self.leaderboard_button = Button(self, self.images['cup'], self.images['cup'],self.images['cup'].get_width()//2, self.images['cup'].get_height()//2, show_leaderboard)
        self.best = Best(self, self.leaderboard_button.x + self.leaderboard_button.image.get_rect().w, self.leaderboard_button.y, Settings.base_path, Settings.FONT_SIZE, scale)
        self.leaderboards = {}
        self.achievements = {}
        if Settings.platform == 'android':
            def get_leaderboards_cb(leaderboards):
                self.leaderboards = leaderboards
                if len(leaderboards) > 0:
                    self.app.playgamesservices.leaderboards_client.get_remote_best(list(leaderboards.keys())[-1],self.best.set_remote_best)
            self.app.playgamesservices.leaderboards_client.get_leaderboards(get_leaderboards_cb)
            def get_achievements_cb(achievements):
                self.achievements = achievements
            self.app.playgamesservices.achievements_client.get_achievements(get_achievements_cb)
            
        self.show_settings_button = Button(self, self.images['settings'], self.images['settings'], Settings.WIN_W - self.images['settings'].get_width()//2, self.images['settings'].get_height()//2, lambda : self.app.configuration.enable())
        if Settings.platform == 'android':
            show_google_play_services_button_surface = self.images['games_controller']
            show_google_play_services_button_surface = pg.transform.scale_by(show_google_play_services_button_surface, self.images['settings'].get_height()/show_google_play_services_button_surface.get_height())
            self.show_google_play_services_button = Button(self, show_google_play_services_button_surface, show_google_play_services_button_surface, Settings.WIN_W - self.images['settings'].get_width() - show_google_play_services_button_surface.get_width()/2, show_google_play_services_button_surface.get_height()//2, lambda : self.app.play_games_intents.enable())
        self._gameover = SpriteUnit(self,self.images['gameover'], Settings.WIN_W / 2, Settings.WIN_H / 2)
        self.score=Score(self, Settings.WIN_W / 2, Settings.WIN_W / 8, Settings.FONT_SIZE, scale)
        

        # Creating groups
        self.group_background = pg.sprite.GroupSingle(self.background)
        self.group_collide = pg.sprite.Group(self.pipes) # special group for sprites that Bird can collide on
        self.group_bonus = pg.sprite.Group(self.bull)
        self.group_bird = pg.sprite.GroupSingle(self.bird)
        self.group_foreground = pg.sprite.Group(self.score, self.score, self.leaderboard_button)
        
        self._started = False

        self.pipe_width = self.images['pipe-green'].get_width()
        self.pipe_requeue_interval = self.rand_pipe_requeue_interval(self.app.speed)
        self.pipe_reque_time = 0.0

    def reset(self):
        self._started = False
        self.background.reset()
        self.bull.reset()
        self.base.reset()
        self.score.reset()
        self.bird.reset()
        for pipe, pipe_reversed in self.pipes:
            pipe.reset()
            pipe_reversed.reset()
        self.group_foreground.empty()
        self.group_foreground.add(self.menu, self.score, self.leaderboard_button, self.best, self.show_settings_button)
        if Settings.platform == 'android':
            self.group_foreground.add(self.show_google_play_services_button)
        self.app.dt=0.0
        self.app.speed = 0
        self.group_background.update()
        self.group_collide.update()
        self.group_bonus.update()
        self.group_bird.update()
        self.group_foreground.update()
           
    def count_sprites(self):
        return len(self.group_bird) + len(self.group_collide) + len(self.group_background) + len(self.group_foreground)

    def rand_pipe_requeue_interval(self, speed):
        offset = speed/Settings.SPEED
        return uniform(2.5 + offset,7.0 + offset)*self.pipe_width/speed
    
    def update_speed(self, speed):
        # print(f"update speed : {speed}")
        self.base.update_speed(-speed)
        self.bird.vel_x = -speed/4
        self.bull.vel_x = -speed
        for (pipe, pipe_reversed) in self.pipes :
            pipe.vel_x = -speed
            pipe_reversed.vel_x = -speed
        if speed > 0:
            self.pipe_requeue_interval = self.rand_pipe_requeue_interval(speed)

    def compute_size(self):
        w = self.images['background-day'].get_width()
        h = self.images['background-day'].get_height()
        return w,h
    
    def load_png(self, path):
        """ from .png to pygame Surfaces """
        # loading .png images
        images = dict([(png_path.stem, pg.image.load(str(png_path))) for png_path in pathlib.Path(path).rglob('*.png') if png_path.is_file()])
        # reversing pipes
        images.update(dict([(f'reversed-{png_path.stem}', pg.transform.flip(pg.image.load(str(png_path)), False, True)) for png_path in pathlib.Path(path).rglob('*.png') if png_path.is_file() and 'pipe' in str(png_path)]))
        #
        if not Settings.USE_OFFICIAL_ASSETS :
            font = pg.font.Font(None, Settings.FONT_SIZE)
            # create 'gameover' asset
            images['gameover'] = Exfont.text_speech(font, 'GAME OVER', 'orange', True, 2, 'white')
            # create 'message' asset
        return images
    
    def extend_world(self, new_width):
        def extend_image(image, new_width):
            n = 1+int(new_width/image.get_width())
            extended_image = pg.Surface((n*image.get_width(), image.get_height()))
            extended_image.blits([(image, (i*image.get_width(), 0)) for i in range(n)])
            return extended_image
        
        # extend base and background to match screen width
        self.images['background-day'] = extend_image(self.images['background-day'], new_width)
        self.images['background-night'] = extend_image(self.images['background-night'], new_width)
        self.images['base'] = extend_image(self.images['base'], 2*new_width)

    def maybe_requeue_pipes(self):
        def pipe_requeue(pipe, pipe_reversed):
            """ 
            Reque pipes 
            Used when pipes are out of camera range
            """
            vel_x = pipe.vel_x
            factor = randrange(0, 2*pipe.orig_rect.height//3)
            pipe.reset()
            pipe.y = pipe.orig_y - factor
            pipe.vel_x = vel_x
            pipe_reversed.reset()
            pipe_reversed.y = pipe_reversed.orig_y - factor
            pipe_reversed.vel_x = vel_x
            pipe.x = pipe_reversed.x = Settings.WIN_W + pipe.rect.width/2
        def bull_requeue():
            """ 
            Reque bull 
            Used when bull is out of camera range
            """
            factor = randrange(-1,3,2)*randrange(0, 4*self.bull.rect.height)
            self.bull.y = self.bull.orig_y + factor
            self.bull.x = Settings.WIN_W + self.bull.rect.width/2

        self.pipe_reque_time += self.app.dt
        if self.pipe_reque_time > self.pipe_requeue_interval:
            if self.bull.vel_x != 0 and self.bull.x < -self.bull.rect.width and self.bull.ready:
                self.pipe_reque_time = 0.0
                self.pipe_requeue_interval = self.rand_pipe_requeue_interval(-self.bull.vel_x)
                bull_requeue()
                return
            for (pipe1,pipe2) in self.pipes:
                if pipe1.vel_x != 0 and pipe1.x < -pipe1.rect.width :
                    # requeue one Pipe that is out of screen
                    self.pipe_reque_time = 0.0
                    self.pipe_requeue_interval = self.rand_pipe_requeue_interval(-pipe1.vel_x)
                    pipe_requeue(pipe1, pipe2)
                    break
            
            
    def update_score(self):
        for (pipe1,pipe2) in self.pipes:
            if pipe1.x < self.bird.x and not pipe1.point_given:
                pg.event.post(pg.event.Event(Settings.EVENT_SOUND, sound = 'point'))
                self.score.increment()
                score = self.score.get()
                if score > self.best.get():
                    self.best.set(score)
                if Settings.platform == 'android':
                    if score == 20:
                        self.app.playgamesservices.achievements_client.unlock('CgkIzdaAt-geEAIQBg') #sparrow
                    if score == 40:
                        self.app.playgamesservices.achievements_client.unlock('CgkIzdaAt-geEAIQBw') #swallow
                    if score == 50:
                        self.app.playgamesservices.achievements_client.unlock('CgkIzdaAt-geEAIQCA') #wild goose
                    if score == 70:
                        self.app.playgamesservices.achievements_client.unlock('CgkIzdaAt-geEAIQCQ') #migratory bird
                    if score == 80:
                        self.app.playgamesservices.achievements_client.unlock('CgkIzdaAt-geEAIQCg') #potato bird
                pipe1.point_given = True
                break
            elif pipe1.x > self.bird.x:
                pipe1.point_given = False


    def update(self):
        self.update_score()
        self.maybe_requeue_pipes()
        self.group_background.update()
        self.group_collide.update()
        self.group_bonus.update()
        self.base.update()
        self.group_bird.update()
        self.group_foreground.update()

    def draw(self):
        self.group_background.draw(self.renderer)
        self.group_collide.draw(self.renderer)
        self.group_bonus.draw(self.renderer)
        self.bird.draw()
        self.base.draw()
        self.group_foreground.draw(self.renderer)

    def on_mouse_press(self):
        mouse_button = pg.mouse.get_pressed()
        if mouse_button[0]:
            x, y = pg.mouse.get_pos()
            if self.leaderboard_button.alive() and self.leaderboard_button.rect.collidepoint((x, y)):
                self.leaderboard_button.press()
            elif self.show_settings_button.alive() and self.show_settings_button.rect.collidepoint((x, y)):
                self.show_settings_button.press()
            elif Settings.platform == 'android' and self.show_google_play_services_button.alive() and self.show_google_play_services_button.rect.collidepoint((x, y)):
                self.show_google_play_services_button.press()
            else:
                self.on_action()
        elif mouse_button[2]:
            pass
            
    def on_mouse_unpress(self):
        mouse_button = pg.mouse.get_pressed()
        if not mouse_button[0] and self.leaderboard_button.pressed:
            self.leaderboard_button.unpress()
        if not mouse_button[0] and self.show_settings_button.pressed:
            self.show_settings_button.unpress()
        if Settings.platform == 'android' and not mouse_button[0] and self.show_google_play_services_button.pressed:
            self.show_google_play_services_button.unpress()

    def on_key_press(self, key):
        if key == pg.K_SPACE:
            self.on_action()

    def on_action(self):
        if not self._started:
            if self.bird.dead:
                self.reset()
            else:
                self.start()
                self.bird.bump(Settings.BUMP_SPEED)
        else:
            self.bird.bump(Settings.BUMP_SPEED)

    def start(self):
        self._started = True
        if Settings.platform=='android':
            self.app.ad_manager.reload()
        self.score.reset()
        self.group_foreground.empty()
        self.group_foreground.add(self.score, self.leaderboard_button, self.best, self.show_settings_button)
        if Settings.platform == 'android' : 
            self.group_foreground.add(self.show_google_play_services_button)
        self.app.speed = int(Settings.SPEED*Settings.speed_multiplier)
        pg.time.set_timer(Settings.EVENT_DAY_NIGHT, Settings.DAY_NIGHT_TIME_MS)

    def stop(self):
        self._started = False
        self.app.speed = 0
        pg.time.set_timer(Settings.EVENT_DAY_NIGHT, 0)

    def game_over(self):
        self.stop()
        self.group_foreground.add(self._gameover)
        self.best.save()
        if Settings.platform=='android':
            for id in self.leaderboards.keys():
                self.app.playgamesservices.leaderboards_client.submit_score(id, self.score.get())
            if self.score.get() < self.best.get():
                # get punished
                self.app.ad_manager.may_show()

    def quit(self):
        self.best.save()

    def set_dark_mode(self,on):
        self.background.set_dark_mode(on)
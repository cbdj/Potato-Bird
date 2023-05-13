from SpriteUnit import SpriteUnit
from random import randrange

class Pipe(SpriteUnit):
    def __init__(self, handler, image, x, y):
        super().__init__(handler, image, x, y)

    def translate(self):
        self.x += self.vel_x * self.handler.app.dt
        self.rect.center = self.x, self.y
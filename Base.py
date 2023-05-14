from SpriteUnit import SpriteUnit

class Base(SpriteUnit):
    def __init__(self, handler, image, x, y):
        super().__init__(handler, image, x, y)

    def translate(self):
        self.x += self.vel_x * self.handler.app.dt
        if self.x < self.orig_x - self.rect.width//2 :
            self.x = self.orig_x
        self.rect.center = self.x, self.y
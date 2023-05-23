from SpriteUnit import SpriteUnit

class Pipe(SpriteUnit):
    def __init__(self, handler, image, x, y):
        super().__init__(handler, image, x, y)
        self.point_given = True

    def translate(self):
        self.x += self.vel_x * self.handler.app.dt
        self.rect.center = self.x, self.y
        
    def reset(self):
        super().reset()
        self.point_given = True
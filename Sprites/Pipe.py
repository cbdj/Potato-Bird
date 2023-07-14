from .SpriteUnit import SpriteUnit

class Pipe(SpriteUnit):
    def __init__(self, handler, image, x, y):
        super().__init__(handler, image, x, y)
        self.point_given = True
        self.rotate_speed = 0
        self.shrink_factor = 1.0

    def translate(self):
        self.x += self.vel_x * self.handler.app.dt
        self.rect.center = self.x, self.y
        self.image.angle += self.rotate_speed * self.handler.app.dt
        self.rect.w *= self.shrink_factor
        self.rect.h *= self.shrink_factor

    def smash(self, point):
        if point > self.y:
            self.rotate_speed = self.vel_x 
        else:
            self.rotate_speed = -self.vel_x 
        self.shrink_factor = 0.99

    def reset(self):
        super().reset()
        self.point_given = True
        self.rotate_speed = 0
        self.shrink_factor = 1.0
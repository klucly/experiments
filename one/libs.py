import numpy
from PIL import Image

class Object2D:
    def __init__(self, position) -> None:
        self.position = numpy.array(position, numpy.float64)
        self._to_draw = False
    def draw(self):
        self._to_draw = True

class Sprite(Object2D):
    def __init__(self, image, position, size) -> None:
        super().__init__(position)
        self.size = numpy.array(size)
        self.image_array = Image.open(image)
        self.image_array = self.image_array.resize(size)
        self.image_array = numpy.array(self.image_array)

class Light_source(Object2D):
    def __init__(self, position, glow_level, color) -> None:
        super().__init__(position)
        self.glow_level = glow_level
        self.color = color

class Bullet(Sprite):
    def __init__(self, image, position, size, direction) -> None:
        super().__init__(image, position, size)
        self.delete = False
        self.glow = None
        self.direction = numpy.array(direction)

    def draw(self):
        self.position += self.direction
        super().draw()

class Bullet_glow(Light_source):
    def __init__(self, bullet: Bullet) -> None:
        super().__init__(bullet.position, 10, [0, 0, 255])
        bullet.glow = self
        self.direction = numpy.array(bullet.direction)
        self.bullet = bullet

    def draw(self):
        self.position = self.bullet.position+self.bullet.size/2
        super().draw()

def get_vector_lenght(vector):
    return numpy.sqrt(vector[0]**2+vector[1]**2)

def normalize(v):
    norm = numpy.linalg.norm(v)
    if norm == 0: 
       return v
    return v / norm
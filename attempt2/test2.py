import numba
from numba import int32, float32
import numpy
from pygame.sndarray import array

spec = [
    ('position', float32[:]),
    ('radius', float32),
]

@numba.experimental.jitclass(spec)
class Sphere:
    def __init__(self, position, radius):
        self.position = position
        self.radius = radius

    def convert(self) -> numpy.ndarray:
        arr = numpy.zeros((1, 3), numpy.float32)
        arr[0][0] = self.position[0]
        arr[0][1] = self.position[1]
        arr[0][2] = self.radius
        return arr

spec = [
    ('objlist', float32[:,:]),
]
@numba.experimental.jitclass(spec)
class Render:
    def __init__(self) -> None:
        self.objlist = numpy.zeros((0, 3), numpy.float32)

r = Render()
a = Sphere(numpy.array((10., 15.), numpy.float32), float32(20.))
r.objlist = numpy.append(r.objlist, a.convert(), 0)
print(r.objlist)

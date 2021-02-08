import pygame
import numpy
from numpy import array, zeros
import numba
from PIL import Image

class App:
    def __init__(self) -> None:
        self.init()

    def init(self, resolution = (1280, 720), FPS = 30, win_caption = "New project", flags = 0) -> None:
        self._window = pygame.display.set_mode(resolution, flags = flags)
        pygame.display.set_caption(win_caption)
        self._pygameclock = pygame.time.Clock()
        self.resolution = resolution
        self.FPS = FPS
        self._got_event_list = False
        if not hasattr(self, "update"):
            self.update = ...
        self.get_fps = self._pygameclock.get_fps
        self.set_caption = pygame.display.set_caption
        self.tick = 0
        self.shader = ...

        class Mouse:
            def __init__(self) -> None:
                self.get_pos = pygame.mouse.get_pos
                self.set_pos = pygame.mouse.set_pos

        class Camera:
            def __init__(self, app: App, position = array([0, 0, 0], numpy.float64), direction = array([1, 0, 0], numpy.float64), viewing_angle = 90., local_resolution = ...) -> None:
                self.app = app
                self.position = position
                self.direction = direction
                self.viewing_angle = viewing_angle
                if local_resolution == ...:
                    self.local_resolution = app.resolution
                else: self.local_resolution = local_resolution

        spec = [
            ('objlist', numba.float32[:,:]),
        ]
        @numba.experimental.jitclass(spec)
        class Render:
            def __init__(self) -> None:
                self.clear()
            def clear(self):
                self.objlist = numpy.zeros((0, 3), numpy.float32)

        self.camera = Camera(self)
        self.render = Render()
        self.mouse = Mouse()

    def get_event_list(self) -> list:
        self._got_event_list = True
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT: exit(0)
        return event_list

    def run(self) -> None:
        while 1:
            self.tick += 1
            if not self._got_event_list:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT: exit(0)
                    
            if self.update != ...:
                self.update()

            pygame.display.flip()
            self._pygameclock.tick(self.FPS)
            self._got_event_list = False
    
    def calculate(self, size):
        if self.shader != ...:
            return _calculate_pixels(size, self.render.objlist, self.camera.direction, self.camera.position, self.shader)
        else:
            return _calculate_pixels(size, self.render.objlist, self.camera.direction, self.camera.position, default_shader)

@numba.jit
def _calculate_pixels(size, objlist, cam_direction, cam_pos, shader):
    width, height = size
    out_list = zeros((width, height, 3), numpy.uint8)
    for obj in objlist:
        direction = cam_direction
        position = cam_pos
        obj_pos = array((obj[0], obj[1], obj[2]))
        obj_radius = obj[2]
        for x in range(width):
            for y in range(height):
                ray_direction = array([direction[0], direction[1]+x/(width/2)-1, (direction[2]+y/(height/2)-1)*(height/width)], numpy.float64)
                pos, collided = raycast(position, ray_direction, obj_pos, obj_radius)
                # out_list[x][y] = shader(pos, array((x, y), numpy.int64), collided, obj)
                r, g, b = shader(pos, array((x, y), numpy.int64), collided, obj)
                out_list[x][y][0], out_list[x][y][1], out_list[x][y][2] = r, g, b
                # out_list[x][y][0] = pos[0]
                # out_list[x][y][1] = pos[1]
                # out_list[x][y][2] = pos[2]
                # if collided:
                #     out_list[x][y][3] = numpy.float64(1)
                # else: out_list[x][y][3] = numpy.float64(0)
    return out_list

@numba.jit
def get_normal(pos1, pos2) -> numpy.ndarray:
    return normalize(pos2-pos1)

@numba.jit
def default_shader(collide_point, pos, collided, obj):
    if collided:
        obj_pos = array((obj[0], obj[1], obj[2]))
        dot1 = get_normal(obj_pos, collide_point)
        dot2 = normalize(array([1, 1, -1]))
        light = (dot(dot1, dot2)/2+.5)*255
        return array((light, light, light), numpy.uint8)
    else:
        return array((64, 64, 64), numpy.uint8)

@numba.jit
def get_lenght(vector):
    sum = 0
    for scalar in vector:
        sum += scalar**2
    return numpy.sqrt(sum)

@numba.jit
def normalize(vector):
    return vector/get_lenght(vector)

@numba.jit
def raycast(position, direction, obj_position, obj_radius):
    min_distance = 2
    rot = normalize(direction)
    for i in range(10):
        distance = (get_lenght(position-obj_position)-obj_radius)
        if distance <= min_distance:
            return position, True
        end_pos = rot * distance +position
        position = end_pos
    return position, False

spec = [
    ('position', numba.float64[:]),
    ('radius', numba.float32),
]

@numba.experimental.jitclass(spec)
class Sphere:
    def __init__(self, render, position, radius):
        self.position = position
        self.radius = radius

    def get_normal(self, position) -> numpy.ndarray:
        return normalize(position-self.position)

    def draw(self, render):
        render.objlist = numpy.append(render.objlist, self.convert(), 0)

    def convert(self) -> numpy.ndarray:
        arr = numpy.zeros((1, 3), numpy.float32)
        arr[0][0] = self.position[0]
        arr[0][1] = self.position[1]
        arr[0][2] = self.radius
        return arr

# cam_pos = array([10, 720//2, 0], numpy.float64)
# cam_rot = array([1, 0, 0], numpy.float64)
# obj_pos = array([1280//3*2, 720//2, 0], numpy.float64)
# obj_radius = 100
# z = 0

# win = pygame.display.set_mode((1280, 720))
# while 1:
#     ray_list = []
#     z += 1
#     cam_pos[-1] = (numpy.sin(z/400)*1.5)*100
#     pygame.event.get()
#     cam_rot = array([*pygame.mouse.get_pos(), 0])-cam_pos
#     for i in range(200):
#         cam_rot1 = array([cam_rot[0], cam_rot[1]+i*2, 0])
#         ray_list.append(raycast(cam_pos, cam_rot1, obj_pos, obj_radius))
#     win.fill((0, 0, 0))
#     intensity = (numpy.sin(z/1000)/2+.5)*255
#     for ray in ray_list:
#         pygame.draw.line(win, (intensity, 0, 255), cam_pos[:2], ray[:2])
#     pygame.display.update()

@numba.jit
def dot(vec1, vec2):
    out = 0
    for i in range(len(vec1)):
        out += vec1[i]*vec2[i]
    return out

# @numba.jit
# def angle(vec) -> float:
#     vec2 = array((0, -1))
#     # print(vec, vec2)
#     formule = numpy.degrees( numpy.arccos(dot(vec, vec2)/(get_lenght(vec)*get_lenght(vec2))))
#     # formule = numpy.arccos((get_lenght(vec)*get_lenght(vec2)))
#     if vec[0] < 0:
#         return formule * (-1)
#     else:
#         return formule

# @numba.jit
# def vec_from_lenght_degree(lenght, degree):
#     vec = numpy.sin( numpy.radians(degree) ), -numpy.cos( numpy.radians(degree) )
#     return array(vec)*lenght

# @numba.jit
# def calculate_rays(viewing_angle, ray_count, cam_rot, cam_pos, obj_pos, obj_radius):
#     ray_angle = viewing_angle/ray_count
#     ray_list = zeros((1, 2), numpy.float64)

#     for ray_i in range(ray_count):
#         angle_ = (vec_from_lenght_degree(1, angle(cam_rot)+ray_i*ray_angle-viewing_angle/2))
#         tmp = zeros((1, 2), numpy.float64)
#         tmp[0] = raycast(cam_pos, angle_, obj_pos, obj_radius)
#         ray_list = numpy.append(ray_list, tmp, axis = 0)
#     return ray_list[1:]

# win = pygame.display.set_mode((1280, 720))
# cam_pos = array([10, 720//2], numpy.float64)
# cam_rot = array([1, 1], numpy.float64)
# obj_pos = array([1280//3*2, 720//2], numpy.float64)
# obj_radius = 100
# z = 0

# clock = pygame.time.Clock()

# ray_count = 2000
# viewing_angle = 90

# while 1:
#     pygame.event.get()
#     cam_rot = array(pygame.mouse.get_pos())-cam_pos
#     ray_list = calculate_rays(viewing_angle, ray_count, cam_rot, cam_pos, obj_pos, obj_radius)
#     win.fill((0, 0, 0))
#     pygame.draw.circle(win, (255, 0, 0), cam_pos, 10)
#     for ray in ray_list:
#         pygame.draw.line(win, (255, 255, 255), cam_pos, ray)
#     pygame.display.flip()
#     clock.tick(30)

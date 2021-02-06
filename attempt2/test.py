import pygame
import numpy
from numpy import array
import numba

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
def raycast(position, rotation, obj_position, obj_radius):
    min_distance = 2
    rot = normalize(rotation)
    for i in range(10):
        distance = (get_lenght(position-obj_position)-obj_radius)
        if distance <= min_distance:
            return position
        end_pos = rot * distance +position
        position = end_pos
    return position

win = pygame.display.set_mode((1280, 720))
cam_pos = array([10, 720//2], numpy.float64)
cam_rot = array([1, 1], numpy.float64)
obj_pos = array([1280//3*2, 720//2], numpy.float64)
obj_radius = 100

clock = pygame.time.Clock()

while 1:
    pygame.event.get()
    cam_rot = array(pygame.mouse.get_pos())-cam_pos
    # print(normalize(cam_rot-cam_pos), cam_rot)
    out = raycast(cam_pos, cam_rot, obj_pos, obj_radius)
    # win.fill((0, 0, 0))
    pygame.draw.circle(win, (255, 0, 0), cam_pos, 10)
    pygame.draw.line(win, (255, 255, 255), cam_pos, out)
    pygame.display.flip()
    clock.tick(30)

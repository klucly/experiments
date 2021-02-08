import pygame
import numpy
from numpy import array, zeros, full
import numba
# from math import degrees, radians, acos, sin, cos

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

@numba.jit
def dot(vec1, vec2):
    out = 0
    for i in range(len(vec1)):
        out += vec1[i]*vec2[i]
    return out

@numba.jit
def angle(vec) -> float:
    vec2 = array((0, -1))
    # print(vec, vec2)
    formule = numpy.degrees( numpy.arccos(dot(vec, vec2)/(get_lenght(vec)*get_lenght(vec2))))
    # formule = numpy.arccos((get_lenght(vec)*get_lenght(vec2)))
    if vec[0] < 0:
        return formule * (-1)
    else:
        return formule

@numba.jit
def vec_from_lenght_degree(lenght, degree):
    vec = numpy.sin( numpy.radians(degree) ), -numpy.cos( numpy.radians(degree) )
    return array(vec)*lenght

@numba.jit
def calculate_rays(viewing_angle, ray_count, cam_rot, cam_pos, obj_pos, obj_radius):
    ray_angle = viewing_angle/ray_count
    ray_list = zeros((1, 2), numpy.float64)

    for ray_i in range(ray_count):
        angle_ = (vec_from_lenght_degree(1, angle(cam_rot)+ray_i*ray_angle-viewing_angle/2))
        tmp = zeros((1, 2), numpy.float64)
        tmp[0] = raycast(cam_pos, angle_, obj_pos, obj_radius)
        ray_list = numpy.append(ray_list, tmp, axis = 0)
    return ray_list[1:]

win = pygame.display.set_mode((1280, 720))
cam_pos = array([10, 720//2], numpy.float64)
cam_rot = array([1, 1], numpy.float64)
obj_pos = array([1280//3*2, 720//2], numpy.float64)
obj_radius = 100
z = 0

clock = pygame.time.Clock()

ray_count = 2000
viewing_angle = 90

while 1:
    pygame.event.get()
    cam_rot = array(pygame.mouse.get_pos())-cam_pos
    ray_list = calculate_rays(viewing_angle, ray_count, cam_rot, cam_pos, obj_pos, obj_radius)
    win.fill((0, 0, 0))
    pygame.draw.circle(win, (255, 0, 0), cam_pos, 10)
    for ray in ray_list:
        pygame.draw.line(win, (255, 255, 255), cam_pos, ray)
    pygame.display.flip()
    clock.tick(30)

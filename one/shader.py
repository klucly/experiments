from numba import jit
from numpy import full, zeros, array, uint8, sin, cos, sqrt
import libs

@jit(fastmath = True)
def fragment_shader(resolution, tick, matrix, obj_pos, obj_size, texture):
    for x in range(max(obj_pos[0], 0), min(obj_pos[0]+obj_size[0], resolution[0])):
        for y in range(max(obj_pos[1], 0), min(obj_pos[1]+obj_size[1], resolution[1])):
            if texture.shape[-1] == 3:
                matrix[y, x] = texture[y-obj_pos[1], x-obj_pos[0]]
            elif texture.shape[-1] == 4:
                alpha = texture[y-obj_pos[1], x-obj_pos[0]][3]/255
                matrix[y, x] = matrix[y, x] * (1-alpha) + texture[y-obj_pos[1], x-obj_pos[0]][:3] * alpha

@jit(fastmath = True)
def compositor(resolution, tick, matrix, lights_glow_levels, lights_poses, lights_colors):
    for x in range(resolution[0]):
        for y in range(resolution[1]):
            for light in range(lights_glow_levels.shape[0]):
                
                distance = (lights_poses[light, 1]-y)**2+(lights_poses[light, 0]-x)**2
                if distance != 0:
                    if light == 0:
                        itensity = (10-min(distance/(lights_glow_levels[light]*lights_glow_levels[light]), 10))/10*lights_colors[light]
                    else:
                        itensity_ = (10-min(distance/(lights_glow_levels[light]*lights_glow_levels[light]), 10))/10*lights_colors[light]
                        itensity = array([max(itensity[0], itensity_[0]), max(itensity[1], itensity_[1]), max(itensity[2], itensity_[2])])

            r = max( matrix[y, x, 0] + uint8(itensity[0]) - 255, 0)
            g = max( matrix[y, x, 1] + uint8(itensity[1]) - 255, 0)
            b = max( matrix[y, x, 2] + uint8(itensity[2]) - 255, 0)

            matrix[y, x] = array([min(r, 255), min(g, 255), min(b, 255)], uint8)
    


def shader_exec(self):
    matrix = full((self.real_resolution[1], self.real_resolution[0], 3), 64, dtype=uint8)
    light_list = [[], [], []]
    for obj in self.objlist:
        if obj.__class__ == libs.Bullet:
            if (obj.position[0] < -self.real_resolution[0] or obj.position[1] < -self.real_resolution[1] or 
                obj.position[0]+obj.size[0] > self.real_resolution[0]*2 or obj.position[1]+obj.size[1] > self.real_resolution[1]*2):

                obj.delete = True
                if obj in self.objlist:
                    self.objlist.remove(obj)
                if obj.glow in self.objlist:
                    self.objlist.remove(obj.glow)

        if obj._to_draw:
            if obj.__class__ == libs.Light_source or libs.Light_source in obj.__class__.__bases__:
                if obj.position[0]+obj.glow_level > 0 and obj.position[1]+obj.glow_level > 0 and obj.position[0]-obj.glow_level < self.real_resolution[0] and obj.position[1]-obj.glow_level < self.real_resolution[1]:
                    light_list[0].append(obj.glow_level)
                    light_list[1].append(obj.position)
                    light_list[2].append(obj.color)
            else:
                fragment_shader(self.real_resolution, self.tick, matrix, array([round(obj.position[0]), round(obj.position[1])]), obj.size, obj.image_array)

    compositor(self.real_resolution, self.tick, matrix, array(light_list[0]), array(light_list[1]), array(light_list[2]))

    return matrix

import pygame
from numpy import array, zeros
from PIL import Image
import random

from libs import *
from shader import *
from options import *


class Main:
    objlist = [
        Sprite("textures/test_dirt.jpg", array([0, 0]), array([887, 541])),
        Sprite("textures/player.png", array([74, 35]), array([11, 20])),
        Light_source([400//8, 300//8], 30, [255, 255, 230]),
        Light_source([400//8, 300//8], 30, [255, 0, 0]),
        # Sprite("textures/bad.png", array([75, 35]), array([11, 20])),
    ]

    
    time_after_last_shot = 0
    keys = {pygame.K_w: None, pygame.K_a: None, pygame.K_s: None, pygame.K_d: None}
    current_fps = 0
    tick = 0

    def __init__(self) -> None:
        def window_init(self):
            self.display = pygame.display.set_mode(win_size)
            if fullscreen: pygame.display.toggle_fullscreen()
            self.clock = pygame.time.Clock()
        
        def options_init(self):
            self.win_size = win_size
            self.FPS = FPS
            self.real_resolution = real_resolution
            self.bullet_render_distance = bullet_render_distance
            self.fullscreen = fullscreen

        options_init(self)
        window_init(self)

        self.mainloop()

    def mainloop(self):
        while 1:
            self.current_fps = self.clock.get_fps()
            pygame.display.set_caption(str(self.current_fps))
            self.tick += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit(0)
                elif event.type == pygame.KEYDOWN:
                    self.keys[event.key] = True
                elif event.type == pygame.KEYUP:
                    self.keys[event.key] = False

            for key in self.keys:
                if self.keys[key]: self.key_processing(key)

            self.mouse_processing(pygame.mouse.get_pressed())

            self.time_after_last_shot += 1
            
            self.objlist[2].position = self.objlist[1].position+self.objlist[1].size//2
            self.objlist[2].glow_level = sin(self.tick/10)+20
            
            for obj in self.objlist: obj.draw()
            
            self.update()

    def mouse_processing(self, buttons):
        if buttons[0] and self.time_after_last_shot >= (1/(self.current_fps/4)*60):
            mouse_pos = self.get_mouse_pos()
            distance = mouse_pos - (self.objlist[1].position+self.objlist[1].size/2)
            self.objlist.append(Bullet("textures/9wjde.png", self.objlist[1].position+self.objlist[1].size/2, array([5, 5]), normalize(distance+array([random.random()*20-10, random.random()*20-10]))*5))
            self.objlist.append(Bullet_glow(self.objlist[-1]))
            self.time_after_last_shot = 0


    def key_processing(self, key):
        if key == pygame.K_a:
            for i in range(len(self.objlist)):
                if i not in [1, 2]: self.objlist[i].position[0] += 1/self.current_fps*60
        elif key == pygame.K_d:
            for i in range(len(self.objlist)):
                if i not in [1, 2]: self.objlist[i].position[0] -= 1/self.current_fps*60
        elif key == pygame.K_w:
            for i in range(len(self.objlist)):
                if i not in [1, 2]: self.objlist[i].position[1] += 1/self.current_fps*60
        elif key == pygame.K_s:
            for i in range(len(self.objlist)):
                if i not in [1, 2]: self.objlist[i].position[1] -= 1/self.current_fps*60

    def get_mouse_pos(self):
        pos = array(pygame.mouse.get_pos())/array(win_size)*array(real_resolution)
        return array([round(pos[0]), round(pos[1])])

    def update(self):

        def pygame_update(self):
            pygame.display.flip()
            self.clock.tick(FPS)


        pixellist = shader_exec(self)
        image = Image.fromarray(pixellist)
        image = image.resize(win_size, resample=0)
        py_image = pygame.image.fromstring(image.tobytes(), image.size, image.mode)
        self.display.blit(py_image, (0, 0))

        pygame_update(self)

if __name__ == "__main__":
    Main()

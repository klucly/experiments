import pygame
from numpy import array, zeros
from PIL import Image

from options import *
from libs import *
from shader import *


class Main:
    objlist = [
        Sprite("textures/test_dirt.jpg", array([0, 0]), array([1280//8, 720//8])), 
        Sprite("textures/player.jpg", array([7, 10]), array([11, 20])), 
        Light_source([400//8, 300//8], 1000, [255, 255, 230]),
        Light_source([400//8, 300//8], 50, [255, 0, 0]),
        Light_source([900//8, 300//8], 50, [0, 255, 255])]
    real_resolution = real_resolution
    tick = 0

    def __init__(self) -> None:
        def window_init(self):
            self.display = pygame.display.set_mode(win_size)
            if fullscreen: pygame.display.toggle_fullscreen()
            self.clock = pygame.time.Clock()

        window_init(self)

        self.mainloop()

    def mainloop(self):
        while 1:
            self.objlist[-1].position[0] = sin(self.tick/10)*10+10
            self.objlist[-1].position[1] = cos(self.tick/10)*10+10
            self.objlist[-2].position[0] = sin(self.tick/20)*10+10
            self.objlist[-2].position[1] = cos(self.tick/20)*10+10
            pygame.display.set_caption(str(self.clock.get_fps()))
            self.tick += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit(0)
            
            self.objlist[1].position = self.get_mouse_pos()-self.objlist[1].size//2
            self.objlist[-3].position = self.objlist[1].position+self.objlist[1].size//2
            self.objlist[-3].glow_level = sin(self.tick/10)*150+1000
            
            for obj in self.objlist: obj.draw()

            self.update()

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

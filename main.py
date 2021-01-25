from PIL import Image
import numpy as np
import pygame
import numba

@numba.jit(fastmath = True)
def calc(t = 1):
    pos = w//2, h//2
    size = 500
    data = np.zeros((h, w, 3), dtype=np.uint8)
    for x in range(h):
        for y in range(w):

            # if (x-pos[1])**2+(y-pos[0])**2 != 0:
            first_image = min(((x-pos[1])**2+(y-pos[0])**2)/size, 1000)/1000

            x_ = (x)*first_image-h/2
            y_ = (y)*first_image-w/2

            second_image = ((np.sin((x_+t)/10)/2+.5)**5+(np.sin((y_+t)/10)/2+.5)**5)/2*255

            data[x, y] = second_image
    return data


w, h = 1280, 720


t = 1
while 1:
    t += 5
    data = calc(t)
    img = Image.fromarray(data, 'RGB')

    mode = img.mode
    size = img.size
    data = img.tobytes()

    win = pygame.display.set_mode([w, h])

    py_image = pygame.image.fromstring(data, size, mode)
    win.blit(py_image, (0, 0)) 

    pygame.display.flip()

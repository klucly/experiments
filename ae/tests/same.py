from pygame import *
from time import sleep
t = 0
win = display.set_mode((1280, 720))
while 1:
    t += 1
    event.get()
    win.fill((0, 0, 0))
    draw.rect(win, (255, 0, 0), Rect(50, (50+20*t) if (50+20*t) < 700 else 700, 20, 20))
    display.update()
    sleep(.1)
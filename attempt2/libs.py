import pygame
from numpy import array, zeros

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
        self._objlist = []

        class Mouse:
            def __init__(self) -> None:
                self.get_pos = pygame.mouse.get_pos
                self.set_pos = pygame.mouse.set_pos

        class Camera:
            def __init__(self, app: App, position = array([0, 0, 0]), rotation = array([0, 0, 0]), viewing_angle = 90, local_resolution = ...) -> None:
                self.app = app
                self.position = position
                self.rotation = rotation
                self.viewing_angle = viewing_angle
                if local_resolution == ...:
                    self.local_resolution = app.resolution
                else: self.local_resolution = local_resolution

        self.camera = Camera()
        self.mouse = Mouse()

    def get_event_list(self) -> list:
        self._got_event_list = True
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT: exit(0)
        return event_list

    def run(self) -> None:
        while 1:
            if not self._got_event_list:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT: exit(0)
                    
            if self.update != ...:
                self.update()

            pygame.display.flip()
            self._pygameclock.tick(self.FPS)
            self._got_event_list = False

def raycast(app: App, position = array([0, 0, 0]), rotation = array([0, 0, 0])):
    ...

    
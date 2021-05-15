from call import *
from global_funcs import *

class Main:
    def __init__(self) -> None:
        global win
        win = win_init()
        self.clock = pygame.time.Clock()
        self.tick = 0

        self.matrix = zeros((16*4, 9*4, 3))

        # for i in range(self.matrix.shape[0]):
        #     for j in range(self.matrix.shape[1]):
        #         self.matrix[i][j][0] = i*10+j*10
        self.matrix[5][5] = Pixel((255, 0, 255))

        while 1: self.mainloop()

    def mainloop(self) -> None:
        self.tick += 1
        self.update_display()

    def update_display(self) -> None:
        event_handle()
        win.fill(bg_color)

        converted_matrix = handle_matrix(self.matrix, tick = self.tick)
        draw_matrix(converted_matrix)

        pygame.display.update()
        self.clock.tick(30)
        pygame.display.set_caption(f"AE {str(self.clock.get_fps())[:5]}fps")


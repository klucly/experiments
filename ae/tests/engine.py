from call import *
from global_funcs import *

class Main:
    def __init__(self) -> None:
        global win
        win = win_init()
        self.displayClock = pygame.time.Clock()
        self.calcClock = pygame.time.Clock()
        self.tick = 0
        self.killed = False

        self.matrix = full((16*4, 9*4), blank)
        self.displayMatrix = full((16*4, 9*4), blank)

        self.matrix[5][5] = Enemy()

        RunThread(self.calc, "Calculation")
        self.update_display()

    def calc(self) -> None:
        def handle_pixel(matrix, x, y, temp):
            if matrix[y][x] != blank and hasattr(matrix[y][x], "update"):
                matrix[y][x].update(matrix, y, x, temp)

        while 1:
            temp = numpy.full_like(self.matrix, blank)
            if self.killed: break
            self.tick += 1
            self.displayMatrix = handle_matrix(self.matrix, tick = self.tick)
            map2d(self.matrix, lambda matrix, x, y: handle_pixel(matrix, x, y, temp))
            self.matrix = temp
            self.calcClock.tick(10)

    def update_display(self) -> None:
        threading.current_thread().setName("DisplayThread")
        while 1:
            self.killed = event_handle()
            if self.killed: break

            win.fill(bg_color)

            if len(self.displayMatrix.shape) > 2:
                draw_matrix(self.displayMatrix)

            pygame.display.update()
            self.displayClock.tick(30)
            pygame.display.set_caption(f"AE {str(self.displayClock.get_fps())[:5]}fps {str(self.calcClock.get_fps())[:5]}tps")


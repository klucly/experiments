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
        self.displayMatrix = full((16*4, 9*4, 3), 0)

        self.matrix[5][5] = Wall()

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

            mouse_pos = self.get_matrix_mouse_pos()
            if self.matrix[mouse_pos[0]][mouse_pos[1]] == None:
                if max(pygame.mouse.get_pressed()):
                    self.matrix[mouse_pos[0]][mouse_pos[1]] = Sand()
                else:
                    self.matrix[mouse_pos[0]][mouse_pos[1]] = Cursor()

            self.displayMatrix = handle_matrix(self.matrix, tick = self.tick)
            map2d(self.matrix, lambda matrix, x, y: handle_pixel(matrix, x, y, temp))
            self.matrix = temp
            
            self.calcClock.tick(max_tps)

    def update_display(self) -> None:
        threading.current_thread().setName("DisplayThread")
        while 1:
            self.killed = event_handle()
            if self.killed: break

            win.fill(bg_color)

            draw_matrix(self.displayMatrix)

            pygame.display.update()
            self.displayClock.tick(max_fps)
            pygame.display.set_caption(f"AE {str(self.displayClock.get_fps())[:5]}fps {str(self.calcClock.get_fps())[:5]}tps")

    def get_matrix_mouse_pos(self):
        return (int(pygame.mouse.get_pos()[0]/pygame.display.get_surface().get_size()[0]*self.matrix.shape[0]), 
                int(pygame.mouse.get_pos()[1]/pygame.display.get_surface().get_size()[1]*self.matrix.shape[1]))

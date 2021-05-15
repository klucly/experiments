from typing import *

from numpy.core.fromnumeric import ptp
from call import *
from PIL import Image

tick_ = 0

def shader(matrix, x, y) -> Union[Tuple[int, int, int], None]:
    if matrix[y][x] == None:
        return bg_color
    elif hasattr(matrix[y][x], "color"):
        return matrix[y][x].color
    else:
        if warnings: print(f"Pixel {matrix[y][x]} at x={x}, y={y} t={tick_} can't be read")
        matrix[y][x] = bg_color

def draw_matrix(matrix: ndarray, normalize = True) -> None:
    global pixelH, pixelW
    pixelW = resolution[0]/matrix.shape[0]
    pixelH = resolution[1]/matrix.shape[1]

    def draw_cell(matrix: ndarray, x: int, y: int):
        if tuple(matrix[y][x]) != bg_color:
            pygame.draw.rect(win, matrix[y][x], pygame.Rect(y*pixelW, x*pixelH, pixelW+1, pixelH+1))

    map2d(matrix, draw_cell)
    # numpy.
    img = Image.fromarray(numpy.resize(matrix, (16*4, 9*4, 3)), "RGB").rotate(-90, resample=0, expand=1).resize((16*80, 9*80), 0, (0, 0, 1280, 720))
    img = pygame.image.fromstring(img.tobytes(), img.size, img.mode)
    win.blit(img, (0, 400))
    # print(img)


def map2d(matrix, func) -> list:
    return list(map(
        lambda y: list(map(
            lambda x: func(matrix, x, y),
            range(len(matrix[y]))
        )),
        range(len(matrix))
    ))

def win_init() -> None:
    global win
    win = pygame.display.set_mode(resolution)
    pygame.display.set_caption("AE")
    win.fill(bg_color)
    return win

def event_handle() -> None:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
    return False

def handle_matrix(matrix, dtype = numpy.int32, tick: int = 0) -> ndarray:
    global tick_
    tick_ = tick
    return array(map2d(matrix, shader), dtype)

def normalize_matrix(matrix: ndarray) -> ndarray:
    min_ = matrix.min()
    matrix -= min_
    max_ = matrix.max()
    if max_ == 0:
        matrix_ = matrix / .001
    else:
        matrix_ = matrix / max_
    a = array(map2d(matrix_, lambda matrix, x, y: matrix_[y][x]), numpy.float32)
    return a

from typing import *
from call import *

tick_ = 0

def shader(matrix, x, y) -> Union[Tuple[int, int, int], None]:
    if matrix[y][x] == None:
        return blank
    elif hasattr(matrix[y][x], "color"):
        return matrix[y][x].color
    else:
        if warnings: print(f"Pixel {matrix[y][x]} at x={x}, y={y} t={tick_} can't be read")
        return blank

def draw_matrix(matrix: ndarray, normalize = True) -> None:
    global pixelH, pixelW
    pixelW = resolution[0]/matrix.shape[0]
    pixelH = resolution[1]/matrix.shape[1]

    if normalize:
        matrix_ = matrix
        del matrix
        matrix = normalize_matrix(matrix_) * 255

    def draw_cell(matrix: ndarray, x: int, y: int):
        if (matrix[y][x] != blank):
            pygame.draw.rect(win, matrix[y][x], pygame.Rect(y*pixelW, x*pixelH, pixelW+1, pixelH+1))

    map2d(matrix, draw_cell)

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

def handle_matrix(matrix, dtype = object, tick: int = 0) -> ndarray:
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

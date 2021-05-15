import threading
from numpy import ndarray
import random

class RunThread(threading.Thread):
    def __init__(self, func, name, *args):
        super().__init__(*args, name = name)
        self.run = func
        self.start()

class Pixel:
    def __init__(self, color) -> None:
        self.color = color

    def update(self, matrix: ndarray, x: int, y: int, new: ndarray) -> None: new[x][y]=self
            
    def borderCollide(self, matrix, x, y) -> bool:
        return y >= matrix.shape[1]-1 or y <= 0 or x >= matrix.shape[0]-1 or x <= 0

class Enemy(Pixel):
    def __init__(self) -> None:
        super().__init__((255, 0, 0))

    def update(self, matrix: ndarray, x: int, y: int, new: ndarray) -> None:
        if not self.borderCollide(matrix, x, y):
            # new[x][y+1] = self
            # new[x][y-1] = self
            # new[x-1][y] = self
            # new[x+1][y] = self
            # new[x][y] = self
            if x^y > 5: 
                new[x+2][y] = self
                new[x-2][y] = self
            else:
                new[x][y+1] = self

        else: new[x][y] = self

class Wall(Pixel):
    def __init__(self) -> None:
        super().__init__((60, 60, 60))

class Cursor(Pixel):
    def __init__(self) -> None:
        super().__init__((255, 0, 0))
        
    def update(self, matrix: ndarray, x: int, y: int, new: ndarray) -> None: ...

class Sand(Pixel):
    def __init__(self) -> None:
        super().__init__((random.randint(200, 255), random.randint(200, 255), 0))

    def update(self, matrix: ndarray, x: int, y: int, new: ndarray) -> None:
        if not self.borderCollide(matrix, x, y):
            if matrix[x+1][y+1] == None and matrix[x-1][y+1] == None and matrix[x][y+1] != None:
                new[x+(random.randint(0, 1)*2-1)][y+1] = self
            elif matrix[x][y+1] == None:
                new[x][y+1] = self
            elif matrix[x+1][y+1] == None:
                new[x+1][y+1] = self
            elif matrix[x-1][y+1] == None:
                new[x-1][y+1] = self
            else:
                new[x][y] = self
        else:
            new[x][y] = self
   

blank = None

from typing import Union
from numpy import *

class _Vector:
    def __math_func__(self, obj1: object, sign: str):
        out = []
        out = eval(f"self._list {sign} obj1")
        return self.__class__(out)

    def __add__(self, obj: object): return self.__math_func__(obj, "+")
    def __sub__(self, obj: object): return self.__math_func__(obj, "-")
    def __mul__(self, obj: object): return self.__math_func__(obj, "*")
    def __rmul__(self, obj: object): return self.__math_func__(obj, "*")
    def __truediv__(self, obj: object): return self.__math_func__(obj, "/")
    def __pow__(self, obj: object): return self.__math_func__(obj, "**")
    def __floordiv__(self, obj: object): return self.__math_func__(obj, "//")
    def __mod__(self, obj: object): return self.__math_func__(obj, "%")
    
    def __contains__(self, obj: Union[int, float]): return obj in self._list
    def __getitem__(self, index: int): return self._list[index]
    def __setitem__(self, index: int, obj: Union[int, float]): self._list[index] = obj

class Vec2(_Vector):
    def __init__(self, num1 = ..., num2 = ...) -> None:
        if num1.__class__ in [list, tuple]:
            self._list = array(num1)
        elif num1.__class__ in [int, float]:
            if num2.__class__ in [int, float]:
                self._list = array([num1, num2])
            else:
                self._list = array([num1, num1])
        elif num1.__class__ == ndarray or num1.__class__ == Vec2:
            self._list = num1
        else:
            self._list = array([0, 0])

    @property
    def x(self): return self._list[0]
    @property
    def y(self): return self._list[1]

    def __repr__(self) -> str:
        return f"Vec2({self._list[0]} {self._list[1]})"

    def __len__(self): return 3

class Vec3(_Vector):
    def __init__(self, num1 = ..., num2 = ..., num3 = ...) -> None:
        if num1.__class__ in [list, tuple]:
            self._list = array(num1)
        elif num1.__class__ in [int, float]:
            if num2.__class__ in [int, float]:
                self._list = array([num1, num2, num3])
            else:
                self._list = array([num1, num1, num1])
        elif num1.__class__ == ndarray or num1.__class__ == Vec3:
            self._list = num1
        else:
            self._list = array([0, 0, 0])

    @property
    def x(self): return self._list[0]
    @property
    def y(self): return self._list[1]
    @property
    def z(self): return self._list[2]
    @property
    def r(self): return self._list[0]
    @property
    def g(self): return self._list[1]
    @property
    def b(self): return self._list[2]
    @property
    def xy(self): return self._list[:2]
    @property
    def yz(self): return self._list[1:]
    @property
    def rg(self): return self._list[:2]
    @property
    def gb(self): return self._list[1:]
            
    def __repr__(self) -> str:
        return f"Vec2({self._list[0]} {self._list[1]} {self._list[2]})"

    def __len__(self): return 3

def get_lenght(vector):
    sum = 0
    for scalar in vector:
        sum += scalar**2
    return sqrt(sum)

def normalize(vector):
    return vector/get_lenght(vector)

def dot(vector1, vector2):
    sum = 0
    for i in range(len(vector1)):
        sum += vector1[i]*vector2[i]
    return sum

a = normalize(Vec3(1, 5, 1))

print(dot(a, Vec3(1, 0, 0)))


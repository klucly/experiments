from libs import *

class Main(App):
    def __init__(self) -> None:
        self.init()

    def update(self):
        obj_pos = array([10, 3, 0], numpy.float64)
        obj_radius = 1
        # self.width = 16*8
        # self.height = 9*8
        self.width = 1280//8
        self.height = 720//8
        self.sphere = Sphere(self.render, obj_pos, obj_radius)

        self.draw()

        
        self.set_caption(str(self.get_fps()))

    def draw(self):
        self.sphere.position[1] = numpy.sin(self.tick/10)*10
        self.camera.direction = normalize(array((10, numpy.sin(self.tick/10)*10, 0), numpy.float64))
        self.render.clear()
        width = self.width
        height = self.height
        self.sphere.draw(self.render)
        pixels = self.calculate(array([width, height]))
        # for x in range(width):
        #     for y in range(height):
        image = Image.fromarray(pixels)
        image = image.resize([self.resolution[1], self.resolution[0]], resample=0)
        py_image = pygame.image.fromstring(image.tobytes(), image.size, image.mode)
        py_image = pygame.transform.rotate(py_image, -90)
        py_image = pygame.transform.flip(py_image, True, False)
        self._window.blit(py_image, (0, 0))
        # pygame.draw.rect(self._window, pixels[x][y], pygame.Rect(1280/width*x, 720/height*y, 1280/width+1, 720/height+1))


app = Main()
app.run()

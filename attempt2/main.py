from libs import *

class Main(App):
    def __init__(self) -> None:
        self.init()

    def update(self):
        self.mouse.set_pos(array(self.mouse.get_pos())+1)
        self.set_caption(str(self.get_fps()))


app = Main()
app.run()

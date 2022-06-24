import numpy as np
from pygame import *
init()

class Node:
    def __init__(self):
        self.conns=[]

        self.inputs=[]
        self.outputs=[]

class Conn:
    pass



class Game:
    def __init__(self):
        self.WIDTH = 1000
        self.HEIGHT = 500
        self.WINDOW_SIZE = Vector2(self.WIDTH,self.HEIGHT)
        self.FPS = 60
        self.BACKGROUND = (0,0,0)
        self.BORDER = (255,0,0)
        self.BORDER_WIDTH = 1

        self.win = display.set_mode(self.WINDOW_SIZE.xy)
        self.clock = time.Clock()
        self.running = True

    def checkInput(self):
        events=event.get()
        for even in events:
            if even.type == QUIT:
                self.stop()


    def mainUpdate(self):
        pass
    def mainDraw(self):
        pass

    def mainWindowUpdate(self):
        display.update()
        self.clock.tick(self.FPS)
        display.set_caption(str(self.clock.get_fps()))

    def mainLoop(self):
        while self.running:
            self.checkInput()
            if not self.running:
                continue
            self.mainUpdate()
            if not self.running:
                continue
            self.mainDraw()
            if not self.running:
                continue
            self.mainWindowUpdate()

    def stop(self):
        self.running=False

    def destroy(self):
        quit()

    def run(self):
        self.mainLoop()
        self.destroy()

if __name__ == "__main__":
    game=Game()
    game.run()
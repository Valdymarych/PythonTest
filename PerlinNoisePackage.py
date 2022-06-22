import numpy as np
import random as rd
from pygame import *
import math as mt
import time as tm
class SimpleNoise:
    def __init__(self,WIDTH,HEIGHT,side,smoothing=1):
        self.WIDTH=WIDTH
        self.HEIGHT=HEIGHT
        self.side=side
        self.noiseArray,self.vectors=np.array([]),[]
        self.noiseSurface=Surface((side,side))
        self.smoothing=smoothing

        self.smooth=lambda t,i: self.smooth(t*t*(3-2*t),i-1) if i>0 else t
        self.generateNoise()

    def generateNoise(self):
        width = self.WIDTH + self.side - 1 - (self.WIDTH - 1) % self.side
        height = self.HEIGHT + self.side - 1 - (self.HEIGHT - 1) % self.side
        vectors = []
        vectorByAngle = lambda alfa: Vector2(mt.sin(alfa), mt.cos(alfa))
        for y in range(int(height // self.side + 1)):
            vectors.append([])
            for x in range(int(width // self.side + 1)):
                vectors[-1].append(vectorByAngle(rd.random() * mt.pi * 2))
        result = np.zeros((height, width), dtype=np.float32)
        sector = np.linspace(0, self.side - 1, self.side, dtype=np.float32) / self.side
        sectorX, sectorY = np.meshgrid(sector, sector)
        sectorX2 = sectorX - 1
        sectorZ1 = np.zeros((self.side, self.side), dtype=np.float32)
        sectorZ2 = np.zeros((self.side, self.side), dtype=np.float32)
        for y, yVectors in enumerate(vectors[:-1]):
            for x, xVector in enumerate(yVectors[:-1]):
                v1x, v1y = xVector.xy
                v2x, v2y = vectors[y + 1][x].xy
                v3x, v3y = vectors[y][x + 1].xy
                v4x, v4y = vectors[y + 1][x + 1].xy
                sectorZ1[:, :] = v1x * sectorX + v1y * sectorY + self.smooth(sectorY,self.smoothing) * (
                            sectorX * (v2x - v1x) + sectorY * (v2y - v1y) - v2y)
                sectorZ2[:, :] = v3x * sectorX2 + v3y * sectorY + self.smooth(sectorY,self.smoothing) * (
                            sectorX2 * (v4x - v3x) + sectorY * (v4y - v3y) - v4y)

                result[y * self.side:(y + 1) * self.side, x * self.side:(x + 1) * self.side] = sectorZ1 + (sectorZ2 - sectorZ1) * self.smooth(
                    sectorX,self.smoothing)
        result = (result[:self.HEIGHT, :self.WIDTH] - result.min()) / (-result.min() + result.max()) * 255
        result = result.astype(dtype=np.uint8)
        result = np.rot90(result)
        result=np.expand_dims(result,2)
        self.noiseArray=np.concatenate([result, result, result], 2)
        self.vectors=vectors
        self.surface = surfarray.make_surface(self.noiseArray)

    def getSurface(self):
        return self.surface

class View:
    def __init__(self,x,y,width,height):
        self.posts = []
        self.height=height
        self.width=width
        self.y=y
        self.x=x
        self.surface=Surface(width,height)

    def update(self,surface):
        self.updateSelf()
        self.updatePost()


        self.draw(surface)


    def draw(self,surface):
        self.drawSelf()
        self.drawPost()
        surface.blit(self.surface,(self.x,self.y))


    def drawSelf(self):
        pass

    def drawPost(self):
        for post in self.posts:
            post.draw(self.surface)

    def updateSelf(self):
        pass

    def updatePost(self):
        for post in self.posts:
            post.update()

    def addView(self,view):
        self.posts.append(view)

class Button(View):
    def __init__(self,x,y,width,height):
        super(Button, self).__init__(x,y,width,height)

        self.onClick=func

    def drawSelf(self):
        draw.rect(self.surface,(100,100,100),self.surface.get_rect(),3)

class Game:
    def __init__(self):
        self.WIDTH = 256
        self.HEIGHT = 256
        self.WINDOW_SIZE = Vector2(self.WIDTH,self.HEIGHT)
        self.FPS = 60
        self.BACKGROUND = (0,0,0)
        self.BORDER = (255,0,0)
        self.BORDER_WIDTH = 10

        self.win = display.set_mode(self.WINDOW_SIZE.xy)
        self.clock = time.Clock()
        self.running = True

        self.mPosBuf = [0,Vector2(0,0)]

        self.noiseSurface=Surface((700,500))

        self.noise=SimpleNoise(256,256,16)

    def checkInput(self):
        for even in event.get():
            if even.type == QUIT:
                self.stop()
            if even.type == KEYDOWN:
                pass
            if even.type == MOUSEBUTTONDOWN:
                if even.button == BUTTON_LEFT:
                    self.mPosBuf = [True,Vector2(even.pos)]
        pressed=key.get_pressed()
        if pressed[K_s]:
            self.roll[1]+=4
        if pressed[K_w]:
            self.roll[1]-=4

    def mainUpdate(self):
        pass

    def mainDraw(self):
        self.win.fill(self.BACKGROUND)
        self.win.blit(self.noise.getSurface(),(0,0))
        draw.rect(self.win,self.BORDER,[0,0,self.WIDTH,self.HEIGHT],self.BORDER_WIDTH)

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
import numpy as np
import random as rd
from pygame import *
import math as mt
import time as tm
class SimpleNoise:
    def __init__(self,WIDTH,HEIGHT,side,smoothing=1,zoom=[1,1]):
        self.WIDTH=WIDTH
        self.HEIGHT=HEIGHT

        self.side=side
        self.sideX=side*zoom[0]
        self.sideY=side*zoom[1]

        self.vectorsWIDTH=self.WIDTH + self.sideX - 1 - (self.WIDTH - 1) % self.sideX
        self.vectorsHEIGHT=self.HEIGHT + self.sideY - 1 - (self.HEIGHT - 1) % self.sideY

        self.noiseArrayColors=np.array([])  # для малювидла                 (0 - 255)
        self.noiseArrayValues=np.array([])  # для більш складніших структур (self.minValue - self.maxValue)
        self.vectors=[]
        self.smoothing=smoothing

        self.smooth=lambda t,i: self.smooth(t*t*(3-2*t),i-1) if i>0 else t

        self.minValue=-(2**(-1/2))
        self.maxValue=2**(-1/2)
        self.generateNoise()

        self.surface=Surface((self.WIDTH,self.HEIGHT))

        self.filters=[]


    def generateVectors(self):
        vectorByAngle = lambda alfa: Vector2(mt.sin(alfa), mt.cos(alfa))
        for y in range(int(self.vectorsHEIGHT // self.sideY + 1)):
            self.vectors.append([])
            for x in range(int(self.vectorsWIDTH // self.sideX + 1)):
                self.vectors[-1].append(vectorByAngle(rd.random() * mt.pi * 2))

    def generateNoise(self):
        result = np.zeros((self.vectorsHEIGHT, self.vectorsWIDTH), dtype=np.float32)
        sectorXproto = np.linspace(0, (self.sideX - 1), self.sideX, dtype=np.float32) / self.sideX
        sectorYproto = np.linspace(0, (self.sideY - 1), self.sideY, dtype=np.float32) / self.sideY
        sectorX, sectorY = np.meshgrid(sectorXproto, sectorYproto)
        sectorX2 = sectorX - 1
        sectorZ1 = np.zeros((self.sideY, self.sideX), dtype=np.float32)
        sectorZ2 = np.zeros((self.sideY, self.sideX), dtype=np.float32)
        for y, yVectors in enumerate(self.vectors[:-1]):
            for x, xVector in enumerate(yVectors[:-1]):
                v1x, v1y = xVector.xy
                v2x, v2y = self.vectors[y + 1][x].xy
                v3x, v3y = self.vectors[y][x + 1].xy
                v4x, v4y = self.vectors[y + 1][x + 1].xy
                sectorZ1[:, :] = v1x * sectorX + v1y * sectorY + self.smooth(sectorY,self.smoothing) * (sectorX * (v2x - v1x) + sectorY * (v2y - v1y) - v2y)
                sectorZ2[:, :] = v3x * sectorX2 + v3y * sectorY + self.smooth(sectorY,self.smoothing) * (sectorX2 * (v4x - v3x) + sectorY * (v4y - v3y) - v4y)
                result[y * self.sideY:(y + 1) * self.sideY, x * self.sideX:(x + 1) * self.sideX] = sectorZ1 + (sectorZ2 - sectorZ1) * self.smooth(sectorX,self.smoothing)
        result = result[:self.HEIGHT, :self.WIDTH]
        self.noiseArrayValues = result


    def generateSurface(self):  # робить noiseArrayColors з noiseArrayValues і запихає все в surface
        self.noiseArrayColors = (self.noiseArrayValues - self.minValue) / (-self.minValue + self.maxValue) * 255
        self.noiseArrayColors = np.rot90(self.noiseArrayColors)
        self.noiseArrayColors = np.expand_dims(self.noiseArrayColors,2)
        self.noiseArrayColors = np.concatenate([self.noiseArrayColors, self.noiseArrayColors, self.noiseArrayColors], 2)
        self.noiseArrayColors = self.applyFilters(self.noiseArrayColors)
        self.noiseArrayColors = self.noiseArrayColors.astype(dtype=np.uint8)
        self.surface = surfarray.make_surface(self.noiseArrayColors)

    def getSurface(self):
        return self.surface

    def resize(self,newWIDTH,newHEIGHT):
        self.WIDTH=newWIDTH
        self.HEIGHT=newHEIGHT

    def applyFilters(self,noise):
        return noise


class MixNoise:
    def __init__(self,WIDTH,HEIGHT):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT

        self.noises=[]
        self.impacts=[]   # 1  1/2  1/4  1/8 .... (~side)
        self.noisesCount=0

        self.surface=Surface((self.WIDTH,self.HEIGHT))

        self.minValue=0
        self.maxValue=0

        self.noiseArrayColors=np.zeros((self.HEIGHT,self.WIDTH,3))  # для малювидла                 (0 - 255)
        self.noiseArrayValues=np.zeros((self.HEIGHT,self.WIDTH))  # для більш складніших структур (self.minValue - self.maxValue)


    def generateNoise(self):
        for i in range(self.noisesCount):
            self.noises[i].generateNoise()
            self.noises[i].noiseArrayValues=self.noises[i].noiseArrayValues*self.impacts[i]
            self.noiseArrayValues+=self.noises[i].noiseArrayValues
    def generateSurface(self):
        for i in range(self.noisesCount):
            self.noises[i].generateSurface()
            self.noiseArrayColors+=self.noises[i].noiseArrayColors
        self.surface = surfarray.make_surface(self.noiseArrayColors)


    def getSurface(self):
        return self.surface

    def addNoise(self,noise,impact=1):
        noise.resize(self.WIDTH,self.HEIGHT)

        self.noisesCount+=1
        self.noises.append(noise)
        self.impacts.append(impact)
        self.minValue+=noise.minValue*impact
        self.maxValue+=noise.maxValue*impact

        noise.generateNoise()

class Filter:
    def __init__(self,type,filter):
        self.filter=filter
        self.type=type


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


        self.noise1=SimpleNoise(256,256,16)
        self.noise1.generateVectors()
        self.noise1.generateNoise()
        self.noise1.generateSurface()

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
        self.win.blit(self.noise1.getSurface(),(0,0))
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
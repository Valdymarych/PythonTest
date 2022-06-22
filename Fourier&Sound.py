from pygame import *
import math as mt
import struct
from pyaudio import PyAudio
import numpy as np
from time import time as tm
import matplotlib.pyplot as plt
import numpy.fft as fft
print(fft.helper.integer_types)
init()

import pyaudio
p = pyaudio.PyAudio()
for i in range(p.get_device_count()):
    print(i, p.get_device_info_by_index(i)["name"])


"""
CHUNK = 1024*4
FORMAT = pyaudio.paInt16
CHANNELS = 1
RECORD_SECONDS = 5
DEVICE_INDEX=0
WAVE_OUTPUT_FILENAME = "output.wav"
RATE=int(p.get_device_info_by_index(DEVICE_INDEX)['defaultSampleRate'])
p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                input=True,
                input_device_index=DEVICE_INDEX,
                rate=RATE,
                frames_per_buffer=CHUNK)

print("* recording")


fig, ax = plt.subplots(1, figsize=(15, 7))
x = np.arange(0, 2 * CHUNK, 2)


line, = ax.plot(x, np.random.rand(CHUNK), '-', lw=2)
ax.set_title('AUDIO WAVEFORM')
ax.set_xlabel('samples')
ax.set_ylabel('volume')
ax.set_ylim(0, 255)
ax.set_xlim(0, 2 * CHUNK)
plt.setp(ax, xticks=[0, CHUNK, 2 * CHUNK], yticks=[0, 128, 255])
plt.show(block=False)

print('stream started')

frame_count = 0
while True:
    bef=tm()
    data = stream.read(CHUNK)
    print(tm()-bef)
    data_int = struct.unpack(str(2 * CHUNK) + 'B', data)
    data_np = np.array(data_int, dtype='b')[::2] + 128
    line.set_ydata(data_np)
   # try:
    fig.canvas.draw()
    fig.canvas.flush_events()
    frame_count += 1

    #except TclError:
     #   frame_rate = frame_count / (time.time() - start_time)

      #  print('stream stopped')
       # print('average frame rate = {:.0f} FPS'.format(frame_rate))
        #break

print("* done recording")
stream.stop_stream()
stream.close()
p.terminate()
"""


"""
wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()
"""


class Game:
    def __init__(self):

        self.WIDTH=800
        self.HEIGHT=500
        self.winSize=Vector2(self.WIDTH,self.HEIGHT)
        self.winSizeHalf=self.winSize/2
        self.win=display.set_mode(self.winSize)
        self.clock=time.Clock()
        self.FPS=60
        self.BACKGROUND=(0,0,0)

        self.freqs = [10,20,30,40,50]


        self.soundSurfaceOffset=Vector2(10,10)
        self.soundSurfaceSize=Vector2(self.WIDTH-self.soundSurfaceOffset.x*2,self.HEIGHT/2-self.soundSurfaceOffset.y*2)
        self.soundSurface=Surface(self.soundSurfaceSize)


        self.complexSurfaceOffset=Vector2(10,10+self.soundSurfaceOffset.y+self.soundSurfaceSize.y)
        self.complexSurfaceSize=Vector2(self.WIDTH/2-self.complexSurfaceOffset.x,self.HEIGHT/2-10)
        self.complexSurface=Surface(self.complexSurfaceSize)



        self.resultSurfaceOffset=Vector2(10+self.complexSurfaceOffset.x+self.complexSurfaceSize.x,10+self.soundSurfaceOffset.y+self.soundSurfaceSize.y)
        self.resultSurfaceSize=Vector2(self.WIDTH/2-10*2,self.HEIGHT/2-10)
        self.resultSurface=Surface(self.resultSurfaceSize)
        self.scale=[1,101]
        self.axisOffset=Vector2(15,15)
        self.amplitudes=[]


        self.now_t=0
        self.way=[]
        self.now_freq=0


        self.pyaudio = PyAudio()
        self.CHUNK = 1024 * 2
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.DEVICE_INDEX = 0
        self.RATE = int(self.pyaudio.get_device_info_by_index(self.DEVICE_INDEX)['defaultSampleRate'])

        self.stream = p.open(format=self.FORMAT,
                        channels=self.CHANNELS,
                        input=True,
                        input_device_index=self.DEVICE_INDEX,
                        rate=self.RATE,
                        frames_per_buffer=self.CHUNK)
        self.data_np=np.array([0 for i in range(self.CHUNK)], dtype='b')


    def UpdateStuff(self):

        bef=tm()
        self.getSound()
        print(tm()-bef)
        bef = tm()
        self.now_t+=1
        if self.now_t>self.soundSurfaceSize.x:
            self.now_t=0
            self.now_freq+=1
            cnt_mass=Vector2()
            for i in self.way:
                cnt_mass+=i-self.complexSurfaceSize/2
            cnt_mass/=len(self.way)
            self.amplitudes.append(cnt_mass.magnitude())
            self.way=[]
        print(tm() - bef)
    def DrawStuff(self):
        mash = 16
        self.win.fill(self.BACKGROUND)

        self.complexSurface.fill((20,20,20))
        self.resultSurface.fill((20, 20, 20))


        draw.line(self.complexSurface,(255,0,0),[0,self.complexSurfaceSize.y/2],[self.complexSurfaceSize.x,self.complexSurfaceSize.y/2])
        draw.line(self.complexSurface, (255, 0, 0), [self.complexSurfaceSize.x / 2,0],[self.complexSurfaceSize.x/2, self.complexSurfaceSize.y])

        draw.line(self.resultSurface,(255,0,0),[0,self.resultSurfaceSize.y-self.axisOffset.y],[self.resultSurfaceSize.x,self.resultSurfaceSize.y-self.axisOffset.y])
        draw.line(self.resultSurface,(255,0,0),[self.axisOffset.x,0],[self.axisOffset.x,self.resultSurfaceSize.y])




        draw.line(self.soundSurface,(255,0,0),[0,self.soundSurfaceSize.y/2],[self.soundSurfaceSize.x,self.soundSurfaceSize.y/2])
        self.soundSurface.fill((20, 20, 20))
        bef=[0,self.soundSurfaceSize.y/2]
        for t in range(0,int(self.soundSurfaceSize.x)):

            x=t/self.soundSurfaceSize.x*2*mt.pi
            y=self.get_y_by_t(t/self.soundSurfaceSize.x)
            draw.line(self.soundSurface,(255,255,255),[bef[0],bef[1]],[t,y+self.soundSurfaceSize.y/2])
            bef=[t,y+self.soundSurfaceSize.y/2]





        x=self.now_t/self.soundSurfaceSize.x*2*mt.pi
        y = self.get_y_by_t(self.now_t / self.soundSurfaceSize.x)
        draw.line(self.soundSurface,(0,255,0),[self.now_t,y+self.soundSurfaceSize.y/2],[self.now_t,self.soundSurfaceSize.y/2])
        draw.circle(self.soundSurface, (255,0,0), [self.now_t,y+self.soundSurfaceSize.y/2],7)



        if len(self.way)>1:
            draw.lines(self.complexSurface,(255,255,0),False,self.way,2)
        ang=self.now_t/self.soundSurfaceSize.x*2*mt.pi*self.now_freq
        rot_vec=Vector2(1,0).rotate_rad(ang)
        draw.line(self.complexSurface,(255,255,255),self.complexSurfaceSize/2,self.complexSurfaceSize/2+rot_vec*-300)
        draw.line(self.complexSurface, (0, 255, 120), self.complexSurfaceSize / 2,self.complexSurfaceSize / 2 + rot_vec * y,2)
        draw.circle(self.complexSurface,(255,0,0),self.complexSurfaceSize/2+rot_vec*y,7)
        self.way.append(self.complexSurfaceSize/2+rot_vec*y)


        for i,amp in enumerate(self.amplitudes):
            width=int((self.resultSurfaceSize.x-self.axisOffset.x)/(self.scale[1]-self.scale[0]+1))
            draw.rect(self.resultSurface,(255,255,255),[self.axisOffset.x+i*width,self.resultSurfaceSize.y-self.axisOffset.y-amp*mash,width,amp*mash])


        self.win.blit(self.soundSurface,self.soundSurfaceOffset)
        self.win.blit(self.complexSurface, self.complexSurfaceOffset)
        self.win.blit(self.resultSurface, self.resultSurfaceOffset)
    def CheckStuff(self):
        for even in event.get():
            if even.type == QUIT:
                self.terminate()
    def WindowStuff(self):
        display.update()
        self.clock.tick(self.FPS)
        display.set_caption(str(round(self.clock.get_fps())))

    def terminate(self):
        self.stream.stop_stream()
        self.stream.close()
        self.pyaudio.terminate()
        quit()
        exit()
    def mainLoop(self):
        self.UpdateStuff()
        self.DrawStuff()
        self.CheckStuff()
        self.WindowStuff()
    def getSound(self):

        data = self.stream.read(self.CHUNK)
        data_int = struct.unpack(str(2 * self.CHUNK) + 'B', data)
        for i,val in enumerate(data_int[::2]):
            self.data_np[i]=val
        self.data_np = self.data_np
        return self.data_np
    def get_y_by_t(self,t):
        return self.data_np[int(t*(len(self.data_np)-1))]
    def run(self):
        while True:
            self.mainLoop()


if __name__=="__main__":
    game=Game()
    game.run()
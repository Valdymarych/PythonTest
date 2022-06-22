from pygame import *

FPS=60
win_size=[1000,500]
win=display.set_mode(win_size)
clock=time.Clock()

mPos=[0,0]
class Object:
    def __init__(self,size,centerPos):
        self.rect=Rect(centerPos,size)
        self.center=centerPos
        self.rect.center=self.center
        self.angle=0
        self.points=[
            Vector2(-size[0], -size[1]) / 2,
            Vector2( size[0], -size[1]) / 2,
            Vector2( size[0],  size[1]) / 2,
            Vector2(-size[0],  size[1]) / 2
        ]
    def rotate(self,angle):
        self.angle+=angle
    def get_points(self):
        return [point.rotate(self.angle)+self.center for point in self.points]
class Resistor(Object):
    resistors=[]
    def __init__(self,size,centerPos,name):
        super().__init__(size,centerPos)
        self.name=name
        Resistor.resistors.append(self)
    def draw(self,win):
        draw.polygon(win,(0,0,0),self.get_points(),1)
def eventUpdate():
    for even in event.get():
        if even.type==QUIT:
            quit()
            exit()
        if even.type==MOUSEWHEEL:
            mn=9000
            if len(Resistor.resistors)<1:
                continue
            resist=Resistor.resistors[0]
            for res in Resistor.resistors:
                l=(res.center-mPos).magnitude()
                if mn>l:
                    mn=l
                    resist=res
            resist.rotate(even.y*15)
        if even.type==MOUSEBUTTONDOWN:
            if even.button==1:
                Resistor([100,30],even.pos,"1")

def fullDraw(win):
    for resistor in Resistor.resistors:
        resistor.draw(win)

while True:
    mPos=Vector2(mouse.get_pos())
    win.fill((255,255,255))
    fullDraw(win)

    eventUpdate()
    clock.tick(FPS)
    display.update()

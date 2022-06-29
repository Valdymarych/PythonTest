import numpy as np
from pygame import *
import random as rd
init()
class View:
    def __init__(self,rect,magnetic=[],alfa=False):
        #  magnetic:     top  down  left  right

        if "top" in magnetic:
            rect.y=0
        if "left" in magnetic:
            rect.x=0

        self.magnetic=magnetic
        self.posts = []

        if alfa:
            self.surface=Surface(rect.size,flags=SRCALPHA)
        else:
            self.surface=Surface(rect.size)

        self.rect=rect                          # координати відносно контейнера
        self.rectDraw=self.surface.get_rect()   # рект свого сурвейса    (!!! МІНЯЄТЬСЯ ТІЛЬКИ ПРИ RESIZE !!!)
        self.absoluteRect=rect                  # абсолютні координати
        self.figures=[]

    def update(self,events):
        self.updateSelf(events)
        self.updatePost(events)

    def draw(self,surface):
        self.drawSelf()
        self.drawFigures()
        self.drawPost(surface)
        surface.blit(self.surface,self.rect.topleft)

    def drawFigures(self):
        for figure in self.figures:
            figure.draw(self.surface)

    def drawSelf(self):
        pass

    def drawPost(self,surface):   # surface  --- surface від контейнера
        for post in self.posts:   #  self.surface ---  своя surface
            post.draw(self.surface)

    def updateSelf(self,events):
        pass

    def updatePost(self,events):
        for post in self.posts:
            post.update(events)

    def addView(self,view):
        self.posts.append(view)
        view.added(self)

    def addFigure(self,figure):
        self.figures.append(figure)

    def removeFigure(self,figure):
        self.figures.remove(figure)

    def added(self,view):
        if "right" in self.magnetic:
            self.rect.x=view.rect.width-self.rect.width
        if "down" in self.magnetic:
            self.rect.y=view.rect.height-self.rect.height
        if "center" in self.magnetic:
            self.rect.center=view.rectDraw.center
        self.absoluteRect=Rect(self.rect.x+view.absoluteRect.x,self.rect.y+view.absoluteRect.y,*self.rect.size)
        for post in self.posts:
            post.added(self)

    def move(self,topleft):
        self.absoluteRect=Rect(self.absoluteRect.x+topleft[0]-self.rect.x,self.absoluteRect.y+topleft[1]-self.rect.y,self.absoluteRect.width,self.absoluteRect.height)
        self.rect=Rect(topleft,self.rect.size)
        for post in self.posts:
            post.added(self)

    def resize(self,width,height):
        oldsurf=self.surface
        self.surface=Surface((width,height))
        self.surface.blit(oldsurf,(0,0))
        self.rectDraw=self.surface.get_rect()
        self.rect.size=self.rectDraw.size
        self.absoluteRect.size=self.rectDraw.size

class Figure:
    def __init__(self,painter,*args):
        self.painter=painter
        self.args=args

    def draw(self,surface):
        self.painter(surface,*self.args)

    def setArgs(self,*args):
        self.args=args


class Button(View):
    def __init__(self,rect,func,magnetic=[]):
        super(Button, self).__init__(rect,magnetic)

        self.onClick=func
        self.backgroundStd=(40,40,40)
        self.backgroundHint=(50,50,50)
        self.backgroundClick=(0,0,0)
        self.background=self.backgroundStd


    def drawSelf(self):
        draw.rect(self.surface,self.background,self.rectDraw)
        draw.rect(self.surface,(100,100,100),self.rectDraw,3)


    def updateSelf(self,events):
        if self.absoluteRect.collidepoint(events["mousePos"]):
            if True in events["pressedMouse"]:
                self.background=self.backgroundClick
            elif "clickMouse" in events.keys() and events["clickMouse"].button==1:
                self.background=self.backgroundClick
                self.onClick()
            else:
                self.background=self.backgroundHint
        else:
            self.background=self.backgroundStd

    def addText(self,text,textColor,fontSize,background):
        self.addView(Text(0,0,text,textColor,fontSize,background,["center"]))

class Text(View):
    def __init__(self,x,y,text,textColor,fontSize,background,magnetic=[]):
        # якщо background == (0,0,0,0) от прозоре
        self.text=text
        self.font=font.Font(None,fontSize)
        self.color = textColor
        self.background=background
        self.invisible=False if len(background)<4 else True
        self.background=self.background[:4]
        super(Text, self).__init__(Rect(x, y, 1, 1),magnetic,True)
        self.setText(text)

    def draw(self,surface):
        if self.invisible:
            self.surface.fill(self.background)
            self.surface.set_colorkey(self.background)
        super(Text, self).draw(surface)


    def drawSelf(self):
        self.surface.fill(self.background)
        self.surface.blit(self.renderedText,self.renderedTextRect)

    def updateSelf(self,events):
        pass

    def setText(self,text):
        self.text=text
        self.renderedText = self.font.render(self.text, False, self.color)
        self.renderedTextRect=self.renderedText.get_rect()
        self.surface=Surface(self.renderedTextRect.size)
        self.rectDraw=self.surface.get_rect()
        self.absoluteRect.size=self.rectDraw.size
        self.rect.size=self.absoluteRect.size

class Image(View):
    def __init__(self,rect,magnetic=[]):
        super(Image, self).__init__(rect,magnetic)
        self.imageSurface=Surface(self.surface.get_rect())

    def drawSelf(self):
        self.surface.blit(self.imageSurface,(0,0))

    def setSurface(self,surface):
        self.imageSurface=surface

class Container(View):
    def __init__(self,rect,magnetic,background,border,alfa=False):
        # border - ширина і колір   [1, (255,0,0)]
        # якщо alfa == True тo прозорий фон
        super(Container, self).__init__(rect,magnetic,alfa)
        self.background=background
        self.borderWidth=border[0]
        self.borderColor=border[1]

    def draw(self,surface):
        super(Container, self).draw(surface)


    def drawSelf(self):
        draw.rect(self.surface,self.background,self.rectDraw)
        draw.rect(self.surface,self.borderColor,self.rectDraw,self.borderWidth)

class Map(Container):
    def __init__(self,rect,magnetic,background,border):
        super(Map, self).__init__(rect,magnetic,background,border)
        self.follow=False
        self.followPos=[0,0]

    def updateSelf(self,events):
        mPos=events["mousePos"]
        mPos=[mPos[0]-self.absoluteRect.x,mPos[1]-self.absoluteRect.y]

        if "clickMouse" in events.keys() and events["clickMouse"].button==1:
            for post in self.posts:
                post.follow=False
            self.follow=False

        #----------------------------------------------------------------------- якщо совгаю post
        for post in self.posts:
            if post.follow:
                post.move([mPos[0]-post.followPos[0],mPos[1]-post.followPos[1]])
            if post.rect.collidepoint(mPos):
                if "downMouse" in events.keys() and events["downMouse"].button==1:
                    post.follow=True
                    post.followPos=[mPos[0]-post.rect.x,mPos[1]-post.rect.y]
        #------------------------------------------------------------------------ якщо совгаю offset
        if "downMouse" in events.keys() and events["downMouse"].button==1 and self.rectDraw.collidepoint(mPos):
            if any([post.rect.collidepoint(mPos) for post in self.posts]):
                self.follow=False
            else:
                self.follow=True
                self.followPos=mPos
                for post in self.posts:
                    post.followPos=post.rect.topleft
        if self.follow:
            for post in self.posts:
                post.move([post.followPos[0]+mPos[0]-self.followPos[0],post.followPos[1]+mPos[1]-self.followPos[1]])

    def addView(self,view):
        super(Map, self).addView(view)
        view.follow=False
        view.followPos=[0,0]

class List(Container):
    def __init__(self,rect,magnetic,background,border,adapter):
        # adapter - функція яка вертає View
        super(List, self).__init__(rect,magnetic,background,border)
        self.adapter=adapter
        self.realHeight=0

    def addElement(self,*args):
        newpost=self.adapter(*args)
        newwidth=self.rectDraw.width
        realHeight=self.realHeight
        self.realHeight+=newpost.rect.height+newpost.rect.y
        newheight=max(self.realHeight,self.rectDraw.height)
        if newpost.rect.width>self.rect.width:
            newwidth=newpost.rect.width

        newpost.move([0,realHeight])
        print(newwidth,newheight,self.rectDraw.height)
        self.resize(newwidth,newheight)

        self.addView(newpost)



def adapter(text):
    cont=Container(Rect(0,0,100,100),[],(0,0,0),[1,(255,0,0)])
    cont.addFigure(fig)
    fig.setArgs((0,0,250),[0,0],[100,100])
    return cont

def drawwer(surface,color,start,end):
    draw.line(surface,color,start,end,3)
fig=Figure(drawwer,(0,250,0),[0,0],[100,100])
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

        self.mPosBuf = [0,Vector2(0,0)]

        listView=List(Rect(0,0,70,70),[],(0,0,0,0),[5,(255,0,0)],adapter)
        listView.addElement("Хелоу")
        listView.addElement("Альо")
        self.mainView=Container(self.win.get_rect(),[],self.BACKGROUND,[self.BORDER_WIDTH,self.BORDER])
        self.map=Map(Rect(0,0,self.WIDTH//2,self.HEIGHT),["right"],[0,0,0],[self.BORDER_WIDTH,self.BORDER])
        self.mainView.addView(self.map)
        btn=Button(Rect(100, 100, 100, 100), lambda :print(1),["right"])
        btn.addText("print(1)",(255,255,255),30,(0,0,0,0))
        self.map.addView(btn)
        self.map.addView(listView)

        self.map.addView(Text(150,150,"qwerty",(255,0,0),30,[*self.BACKGROUND,0]))

    def checkInput(self):
        events=event.get()
        eventsDone={}
        for i,even in enumerate(events):
            if even.type == QUIT:
                self.stop()
            if even.type == MOUSEBUTTONDOWN:
                eventsDone["downMouse"]=even
            if even.type == MOUSEBUTTONUP:
                eventsDone["clickMouse"]=even
            if even.type == KEYDOWN:
                eventsDone["clickKey"]=even
            if even.type == MOUSEWHEEL:
                eventsDone["wheel"]=even
        eventsDone["mousePos"]=mouse.get_pos()
        eventsDone["pressedKey"]=key.get_pressed()
        eventsDone["pressedMouse"]=mouse.get_pressed()
        return eventsDone

    def mainUpdate(self,events):
        self.mainView.update(events)

    def mainDraw(self):
        self.mainView.draw(self.win)

    def mainWindowUpdate(self):
        display.update()
        self.clock.tick(self.FPS)
        display.set_caption(str(self.clock.get_fps()))

    def mainLoop(self):
        while self.running:
            events=self.checkInput()
            if not self.running:
                continue
            self.mainUpdate(events)
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
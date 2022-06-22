import numpy as np
from pygame import *
init()
class View:
    def __init__(self,rect):
        self.posts = []

        self.surface=Surface(rect.size)
        self.rect=rect
        self.rectDraw=self.surface.get_rect()
        self.absoluteRect=rect

    def update(self,events):
        self.updateSelf(events)
        self.updatePost(events)

    def draw(self,surface):
        self.surface.fill((0,0,0))
        self.surface.set_colorkey((0,0,0))
        self.drawSelf()
        self.drawPost()
        surface.blit(self.surface,self.rect.topleft)


    def drawSelf(self):
        pass

    def drawPost(self):
        for post in self.posts:
            post.draw(self.surface)

    def updateSelf(self,events):
        pass

    def updatePost(self,events):
        for post in self.posts:
            post.update(events)

    def addView(self,view):
        self.posts.append(view)
        view.added(self)

    def added(self,view):
        self.absoluteRect=Rect(self.rect.x+view.absoluteRect.x,self.rect.y+view.absoluteRect.y,*self.rect.size)
        for post in self.posts:
            post.added(self)

class Button(View):
    def __init__(self,rect,func):
        super(Button, self).__init__(rect)

        self.onClick=func
        self.backgroundStd=(25,25,25)
        self.backgroundHint=(50,50,50)
        self.backgroundClick=(0,0,0)
        self.background=self.backgroundStd


    def drawSelf(self):
        draw.rect(self.surface,self.background,self.rectDraw)
        draw.rect(self.surface,(100,100,100),self.rectDraw,3)


    def updateSelf(self,events):
        if self.absoluteRect.collidepoint(events["mousePos"]):
            self.background=self.backgroundHint
            if "clickMouse" in events.keys() and events["clickMouse"].button==1:
                self.background=self.backgroundClick
                self.onClick()
        else:
            self.background=self.backgroundStd
class Text(View):
    def __init__(self,x,y,text,textColor,fontSize,background):
        self.text=text
        self.font=font.Font(None,fontSize)
        self.color = textColor
        self.background=background
        super(Text, self).__init__(Rect(x, y, 1, 1))
        self.setText(text)


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

class Game:
    def __init__(self):
        self.WIDTH = 1000
        self.HEIGHT = 500
        self.WINDOW_SIZE = Vector2(self.WIDTH,self.HEIGHT)
        self.FPS = 60
        self.BACKGROUND = (0,0,0)
        self.BORDER = (255,0,0)
        self.BORDER_WIDTH = 10

        self.win = display.set_mode(self.WINDOW_SIZE.xy)
        self.clock = time.Clock()
        self.running = True

        self.mPosBuf = [0,Vector2(0,0)]

        self.mainView=View(Rect(self.BORDER_WIDTH,self.BORDER_WIDTH,*(self.WINDOW_SIZE-2*Vector2(self.BORDER_WIDTH,self.BORDER_WIDTH)).xy))
        self.mainView.addView(Button(Rect(100, 100, 100, 100), lambda :print(1)))
        self.mainView.addView(Text(150,150,"qwerty",(255,0,0),30,self.BACKGROUND))

    def checkInput(self):
        events=event.get()
        eventsDone={}
        for i,even in enumerate(events):
            if even.type == QUIT:
                self.stop()
            if even.type == MOUSEBUTTONDOWN:
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
        self.win.fill(self.BACKGROUND)
        self.mainView.draw(self.win)
        draw.rect(self.win,self.BORDER,[0,0,self.WIDTH,self.HEIGHT],self.BORDER_WIDTH)

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
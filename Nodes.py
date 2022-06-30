from NewPygame import *

class Node(View):
    def __init__(self,rect,magnetic):
        super(Node, self).__init__(rect,magnetic,True)
        self.connectorWidth=15
        self.connectorHeight=10
        self.impactWidth=30

    def updateSelf(self,events):
        pass


    def drawSelf(self):
        self.surface.fill((0,0,0,0))
        draw.rect(self.surface,(0,0,0),self.rectDraw)
        draw.rect(self.surface,(0,255,0),self.rectDraw,1)


class NodeSpace(Map):
    def __init__(self,rect,magnetic,background,border):
        super(NodeSpace, self).__init__(rect,magnetic,background,border)



    def updateSelf(self,events):
        update=True
        if update:
            super(NodeSpace, self).updateSelf(events)


def nodeAdapter():
    return Container(Rect(0,0,100,100),[],[155,155,0],[3,[0,0,255]])



class Game:
    def __init__(self):
        self.WIDTH = 1000
        self.HEIGHT = 500
        self.WINDOW_SIZE = Vector2(self.WIDTH,self.HEIGHT)
        self.FPS = 60
        self.BACKGROUND = (0,0,0)
        self.BORDER = (255,0,0)
        self.BORDER_WIDTH = 3

        self.win = display.set_mode(self.WINDOW_SIZE.xy)
        self.clock = time.Clock()
        self.running = True

        self.mainView=Container(self.win.get_rect(),[],self.BACKGROUND,[self.BORDER_WIDTH,self.BORDER])


        self.map=NodeSpace(Rect(0,0,3/4*self.WIDTH,self.HEIGHT),["left"],self.BACKGROUND,[self.BORDER_WIDTH,self.BORDER])
        self.list=List(Rect(0,0,1/4*self.WIDTH,self.HEIGHT),["right"],self.BACKGROUND,[self.BORDER_WIDTH,[0,255,0]],nodeAdapter)

        self.map.addView(Node(Rect([100,100,150,100]),[]))
        self.map.addView(Node(Rect([500,100,150,100]),[]))

        self.mainView.addView(self.map)
        self.mainView.addView(self.list)

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
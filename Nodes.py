from NewPygame import *

class Node(View):
    def __init__(self,rect,magnetic):
        super(Node, self).__init__(rect,magnetic,True)
        self.connectorWidth=15
        self.connectorHeight=10
        self.impactWidth=30

        self.connectorRect=Rect(0,0,self.connectorWidth,self.connectorHeight)

        self.inputConnectorsCount=3
        self.outputConnectorsCount=1

        self.inputConnectorsSplit=self.rectDraw.height/self.inputConnectorsCount-self.connectorHeight
        self.outputConnectorsSplit=self.rectDraw.height/self.outputConnectorsCount-self.connectorHeight

        self.inputConnectors=[]
        self.outputConnectors=[]
        self.allConnectors=[]

        for i in range(self.inputConnectorsCount):
            connectorRect=Rect(0,(i+0.5)*self.inputConnectorsSplit+i*self.connectorHeight,self.connectorWidth,self.connectorHeight)
            self.inputConnectors.append(Connector(connectorRect,[],"in"))
            self.addView(self.inputConnectors[-1])
        for i in range(self.outputConnectorsCount):
            connectorRect=Rect(self.rectDraw.width+self.connectorWidth,(i+0.5)*self.outputConnectorsSplit+i*self.connectorHeight,self.connectorWidth,self.connectorHeight)
            self.outputConnectors.append(Connector(connectorRect,[],"out"))
            self.addView(self.outputConnectors[-1])

        self.allConnectors=self.inputConnectors+self.outputConnectors
    def updateSelf(self,events):
        pass

    def drawPost(self,surface):
        for post in self.posts:
            if post in self.allConnectors:
                post.draw(surface)
            else:
                post.draw(self.surface)

    def drawSelf(self):
        self.surface.fill((0,0,0,0))
        draw.rect(self.surface,(0,0,0),self.rectDraw)
        draw.rect(self.surface,(0,255,0),self.rectDraw,1)

class NodeSpace(Map):
    def __init__(self,rect,magnetic,background,border):
        super(NodeSpace, self).__init__(rect,magnetic,background,border)
        def painterConnectionNoReady(surface,connOut,end):
            draw.line(surface,(255,255,255),connOut.rect.center,end)
        def painterConnectionReady(surface,connOut,connIn):
            draw.line(surface,(255,255,255),connOut.rect.center,connIn.rect.center)
        self.painterConnectionReady=painterConnectionReady
        self.createConn=False
        self.createConnConnector=None
        self.createConnConnection=Connection(painterConnectionNoReady)


    def updateSelf(self,events):
        update=True
        mPos=events["mousePos"]
        mPos=[mPos[0]-self.absoluteRect.x,mPos[1]-self.absoluteRect.y]
        if "downMouse" in events.keys() and events["downMouse"].button==1:
            if not any([post.rect.collidepoint(mPos) for post in self.posts]):
                for post in self.posts:
                    for conn in post.outputConnectors:
                        if conn.impactZone.collidepoint(events["mousePos"]):
                            update=False
                            self.createConn=True
                            self.createConnConnector=conn
                            self.createConnConnection.setArgs(self.createConnConnector,mPos)
                            self.addFigure(self.createConnConnection)
        if "clickMouse" in events.keys() and events["clickMouse"].button==1:
            if self.createConn:

                if not any([post.rect.collidepoint(mPos) for post in self.posts]):
                    for post in self.posts:
                        for conn in post.inputConnectors:
                            if conn.impactZone.collidepoint(events["mousePos"]):
                                self.addFigure(Connection(self.painterConnectionReady,self.createConnConnector,conn))

                self.createConn=False
                self.createConnConnector=None
                self.removeFigure(self.createConnConnection)
        print(len(self.figures))
        if self.createConn:
            self.createConnConnection.setArgs(self.createConnConnector,mPos)
        if update:
            super(NodeSpace, self).updateSelf(events)




    def drawSelf(self):
        super(NodeSpace, self).drawSelf()
        for post in self.posts:
            for conn in post.allConnectors:
                draw.rect(self.surface,(255,255,255),conn.impactZone)

class Connector(View):
    def __init__(self,rect,magnetic,type):
        super(Connector, self).__init__(rect,magnetic)
        self.type=type
        self.node=None
        self.startRect=self.rect
        self.impactZone=self.rect
    def drawSelf(self):
        if self.node!=None:
            if self.type=="in":
                draw.rect(self.surface,(255,0,0),self.rectDraw)
            if self.type=="out":
                draw.rect(self.surface,(0,255,0),self.rectDraw)
            draw.rect(self.surface,(0,0,255),self.rectDraw,1)


    def updateSelf(self,events):
        if self.node!=None:
            self.move([self.startRect[0]+self.node.rect[0]-self.rect.width,self.startRect[1]+self.node.rect[1]])
            self.impactZone=self.rect.inflate(self.node.impactWidth-self.rect.width,self.node.inputConnectorsSplit if self.type=="in" else self.node.outputConnectorsSplit)

    def move(self,topleft):
        super(Connector, self).move(topleft)

    def added(self,view):
        super(Connector, self).added(view)
        self.node=view

class Connection(Figure):
    def __init__(self,painter,*args):
        super(Connection, self).__init__(painter,*args)

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
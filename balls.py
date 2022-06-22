from pygame import *
import math as mt
def jut(a,b):
    return a.dot(b)/b.magnitude()
class Ball:
    def __init__(self,pos,V):
        self.next_pos = Vector2(0,0)
        self.next_V = Vector2(V)
        self.pos = pos
        self.r = 15
        self.V = Vector2(V)

class BallFactory:

    def __init__(self,game):
        self.game = game
        self.balls = []
        self.lines = []

        self.lines.append([Vector2(game.WIDTH,game.HEIGHT),Vector2(0,game.HEIGHT)])
        self.lines.append([Vector2(0,game.HEIGHT),Vector2(0, 0)])
        self.lines.append([Vector2(0, 0), Vector2(game.WIDTH, 0)])
        self.lines.append([Vector2(game.WIDTH, 0), Vector2(game.WIDTH, game.HEIGHT)])

    def addBall(self,pos,V):
        self.balls.append(Ball(pos,V))

    def tick(self,dt):
        k=0.5

        for ball_id in range(len(self.balls)):
            ball=self.balls[ball_id]
            ball.next_V+=self.game.g*dt
            ball.next_pos=ball.pos+Vector2(0,0)
            for wall_id in range(len(self.balls)):
                if ball_id==wall_id:
                    continue
                wall=self.balls[wall_id]
                x=ball.pos-wall.pos
                r=x.magnitude()
                if r<ball.r+wall.r:

                    ball.next_pos+=x.normalize()*(ball.r+wall.r-r)/2
                    projection = jut(wall.V-ball.next_V,x)
                    if projection>0.1:
                        ball.next_V=ball.next_V+projection*x.normalize()*(k+1)/2

            for line in self.lines:
                p1=line[0]-ball.pos
                projection=jut(p1,(line[0]-line[1]))
                h=mt.sqrt(p1.magnitude_squared()-projection**2)

                if h<ball.r:
                    p3=line[1]-line[0]
                    y=Vector2(-p3.y,p3.x)
                    projection=jut(ball.next_V,y)
                    if projection<0:
                        ball.next_pos+=y.normalize()*(ball.r-h)
                        ball.next_V=ball.next_V-2*projection*y.normalize()*(k+1)/2
            ball.next_pos+=(ball.next_V+ball.V)/2*dt
            ball.next_V-=self.game.alfa*ball.V
        for ball in self.balls:
            ball.pos = ball.next_pos+Vector2(0,0)
            ball.V=ball.next_V+Vector2(0,0)

    def drawAll(self):
        q=0
        for ball in self.balls:
            q+=-ball.pos[1]+ball.V.magnitude()**2/2
            draw.circle(self.game.win,(0,255,0),ball.pos.xy,ball.r)
        for line in self.lines:
            draw.line(self.game.win,(0,0,255),line[0].xy,line[1].xy,3)
        #print(q)
class Game:
    def __init__(self):
        self.WIDTH = 1400
        self.HEIGHT = 800
        self.WINDOW_SIZE = Vector2(self.WIDTH,self.HEIGHT)
        self.FPS = 60
        self.BACKGROUND = (0,0,0)
        self.BORDER = (255,0,0)
        self.BORDER_WIDTH = 10

        self.win = display.set_mode(self.WINDOW_SIZE.xy)
        self.clock = time.Clock()
        self.running = True

        self.factory=BallFactory(self)
        self.g=Vector2(0,1)
        self.dt=0.2
        self.alfa=0.01

        self.mPosBuf = [0,Vector2(0,0)]
        for y in range(15):
            for i in range(10):
                self.factory.addBall(Vector2(100+y*70+17*i,100+40*i),[0,0])
        #self.factory.addBall(Vector2(200, 200),[5,0])
        #self.factory.addBall(Vector2(400, 200), [-5, 0])


    def checkInput(self):
        for even in event.get():
            if even.type == QUIT:
                self.stop()
            if even.type == KEYDOWN:
                pass
            if even.type == MOUSEBUTTONDOWN:
                if even.button == BUTTON_LEFT:
                    self.mPosBuf = [True,Vector2(even.pos)]
            if even.type == MOUSEBUTTONUP:
                if even.button == BUTTON_LEFT:
                    self.mPosBuf[0] = False
                    self.g=-(self.mPosBuf[1]-Vector2(even.pos))/30
    def mainUpdate(self):
        self.factory.tick(self.dt)

    def mainDraw(self):
        self.win.fill(self.BACKGROUND)
        draw.rect(self.win,self.BORDER,[0,0,self.WIDTH,self.HEIGHT],self.BORDER_WIDTH)
        self.factory.drawAll()
        draw.circle(self.win,(100,100,100),[self.WIDTH-65,65],50)
        draw.circle(self.win, (0, 0, 100), [self.WIDTH - 65, 65], 50,10)

        try:
            g=self.g.normalize()
        except:
            g=Vector2(0,0)
        draw.line(self.win, (255,255,255), [self.WIDTH-65,65], [self.WIDTH-65+g.x*30,65+g.y*30],3)

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
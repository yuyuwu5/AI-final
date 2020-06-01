import random,pygame
#定義顏色
Purple=(255,123,188)
White=(255,255,255)
Black=(0,0,0)
Yellow=(255,255,0)

#定義視窗長寬
screen_height=300
screen_width=300
screen=pygame.display.set_mode((screen_width,screen_height))

#定義球拍
#player_height=10
#player_width=60
player_initial_radium=16
player_initial_y=screen_height-50
player_initial_x=200
player_initial_dx=0
player_initial_dy=0
player_initial_speed=2
#player_buffer=10

#定義球
ball_initial_x=200
ball_initial_y=150
ball_initial_speed=2
ball_smash=10
ball_initial_radium=10
ball_initial_dx=0
ball_initial_dy=0
ball_initial_color=Purple

def Ball(x,y):
    pygame.draw.circle(screen,Purple,(x,y),ball_initial_radium,0)
    #pygame.draw.circle(screen,White,(x,y),ball_initial_radium,0)

def Player(x,y):
    pygame.draw.circle(screen,White,(x,y),player_initial_radium,0)

def Enemy(x,y):
    pygame.draw.circle(screen,White,(x,y),player_initial_radium,0)

def Playground():
    pygame.draw.circle(screen,Yellow,(int(screen_width/2),int(screen_height/2)),50,3)
    #pygame.draw.circle(screen,White,(int(screen_width/2),int(screen_height/2)),50,3)
    middle=pygame.Rect(5,int(screen_height/2),screen_width-5,3)
    pygame.draw.rect(screen,Yellow,middle,0)
    #pygame.draw.rect(screen,White,middle,0)
    left=pygame.Rect(0,0,3,screen_height-3)
    pygame.draw.rect(screen,Yellow,left,0)
    #pygame.draw.rect(screen,White,left,0)
    right=pygame.Rect(screen_width-3,0,3,screen_height-3)
    pygame.draw.rect(screen,Yellow,right,0)
    #pygame.draw.rect(screen,White,right,0)
    up=pygame.Rect(3,0,screen_width-3,3)
    pygame.draw.rect(screen,Yellow,up,0)
    #pygame.draw.rect(screen,White,up,0)
    down=pygame.Rect(3,screen_height-3,screen_width-3,3)
    pygame.draw.rect(screen,Yellow,down,0)
    #pygame.draw.rect(screen,White,down,0)

def updateBall(px,py,ex,ey,x,y,dx,dy,ac,sb):
    x+=dx*sb
    y+=dy*sb
    reward=0
    if (abs(y-py)**2+abs(x-px)**2)<=(player_initial_radium+ball_initial_radium)**2: 
        if ac[3]==1 or ac[4]==1:
            #print("yes")
            sb=ball_smash
        dy=-dy
        x+=sb*dx
        y+=sb*dy
    elif (abs(y-ey)**2+abs(x-ex)**2)<=(player_initial_radium+ball_initial_radium)**2: 
        #dx=-dx
        sb=ball_initial_speed
        dy=-dy
        x+=sb*dx
        y+=sb*dy
    elif y>=screen_height-ball_initial_radium:
        reward=-1
        sb=ball_initial_speed
        dy=-dy
        y=screen_height-ball_initial_radium
    elif y<=ball_initial_radium:
        reward=1
        sb=ball_initial_speed
        dy=-dy
        y=10
    elif x<=ball_initial_radium:
        x=10
        dx=-dx
        x+=dx
    elif x>=screen_width-ball_initial_radium:
        #sb=ball_initial_speed
        x=screen_width-ball_initial_radium
        dx=-dx
        x+=dx
    return [reward,px,py,ex,ey,x,y,dx,dy,sb]
def updatePlayer(ac,x,y):
    if ac[1]==1: #向右
        x+=player_initial_speed
    if ac[2]==1: #向左
        x-=player_initial_speed
    if ac[3]==1: #向下
        y+=player_initial_speed
    if ac[4]==1: #向上
        y-=player_initial_speed
    if x<player_initial_radium:
        x=player_initial_radium
    if x>screen_width-player_initial_radium:
        x=screen_width-player_initial_radium
    if y<int(screen_height/2)+player_initial_radium:
        y=int(screen_height/2)+player_initial_radium
    if y>screen_height-player_initial_radium:
        y=screen_height-player_initial_radium
    return [x,y]
def updateEnemy(bx,by,x,y):
    if x+player_initial_radium<=bx+ball_initial_radium:
        x+=player_initial_speed
    elif x+player_initial_radium>=bx+ball_initial_radium:
        x-=player_initial_speed
    if x<player_initial_radium:
        x=player_initial_radium
    if x>screen_width-player_initial_radium:
        x=screen_width-player_initial_radium
    return [x,y]
class Game:
    def __init__(self):
        #num=random.randint(0,9)
        self.Pscore=0
        self.Escore=0
        self.Px=int(screen_width/2)
        self.Py=screen_height-player_initial_radium
        self.Ex=int(screen_width/2)
        self.Ey=player_initial_radium
        self.Bx=int(screen_width/2)
        self.By=int(screen_height/2)
        self.Bs=ball_initial_speed
        direction=[1,-1]
        self.Bdx=random.choice(direction)
        self.Bdy=random.choice(direction)
    def NowFrame(self):
        pygame.event.pump()
        screen.fill(Black)
        #pygame.Surface((screen_width,1)).fill(White)
        Playground()
        Player(self.Px,self.Py)
        Enemy(self.Ex,self.Ey)
        Ball(self.Bx,self.By)
        screen_shot=pygame.surfarray.array3d(pygame.display.get_surface())
        pygame.display.flip()
        return screen_shot
    def NextFrame(self,ac):
        pygame.event.pump()
        reward=0  #定義reward
        screen.fill(Black)
        Playground()
        #更新player的位置
        self.Px,self.Py=updatePlayer(ac,self.Px,self.Py) 
        Player(self.Px,self.Py)
        self.Ex,self.Ey=updateEnemy(self.Bx,self.By,self.Ex,self.Ey)
        Enemy(self.Ex,self.Ey)
        [reward,self.Px,self.Py,self.Ex,self.Ey,self.Bx,self.By,self.Bdx,self.Bdy,self.Bs]=updateBall(self.Px,self.Py,self.Ex,self.Ey,self.Bx,self.By,self.Bdx,self.Bdy,ac,self.Bs)
        Ball(self.Bx,self.By)
        screen_shot=pygame.surfarray.array3d(pygame.display.get_surface())
        pygame.display.flip()
        if reward==1:
            self.Pscore+=1
        elif reward==-1:
            self.Escore+=1
        #print('%s %d %s %d'%("my score: ",self.Pscore,"enemy score: ",self.Escore))
        return [reward,screen_shot]

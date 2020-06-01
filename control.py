import pygame,game
from pygame.locals import *
import numpy as np
Hocky=game.Game()
frame=Hocky.NowFrame()
#while(1):Hocky.NowFrame()

enemy_score=0
player_score=0
#player
clock=pygame.time.Clock()
while(1):
    ac=np.zeros([5])
    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[K_LEFT]==1:
        ac[2]=1
    elif pressed_keys[K_RIGHT]==1:
        ac[1]=1
    elif pressed_keys[K_UP]==1:
        ac[4]=1
    elif pressed_keys[K_DOWN]==1:
        ac[3]=1
    reward,frame=Hocky.NextFrame(ac)
    if reward==1:player_score+=1
    elif reward==-1:enemy_score+=1
    if reward!=0:
        print('%s %d %s %d'%("my score: ",player_score,"enemy score: ",enemy_score))
    clock.tick(50)


### auto
'''
while(1):
    ac=np.zeros([5])
    num=np.random.randint(0,5,1)
    #num=4
    ac[num]=1
    reward,frame=Hocky.NextFrame(ac)
    if reward==1:player_score+=1
    elif reward==-1:enemy_score+=1
    if reward!=0:
        print('%s %d %s %d'%("my score: ",player_score,"enemy score: ",enemy_score))
'''

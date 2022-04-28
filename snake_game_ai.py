from math import gamma
from tarfile import BLOCKSIZE
import pygame 
import random
from enum import Enum
import numpy as np
from collections import namedtuple
pygame.init()
font=pygame.font.Font('arial.ttf',25)
class Direction(Enum):
    RIGHT = 1
    LEFT=2
    UP=3
    DOWN=4
    
Point = namedtuple('Point','x,y')
BLOCK_SIZE=20
SPEED=200
BLACK=(0,0,0)
WHITE=(255,255,255)
RED=(200,0,0)
BLUE1=(0,0,255)
BLUE2=(0,100,255)

class SnakeGameAI:
    def __init__(self,w=640,h=480):
        self.w=w
        self.h=h
        
        #init the display
        self.display=pygame.display.set_mode((self.w,self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.reset();
        
        
    def reset(self):
       
        #init the initial state and food
        self.direction=Direction.RIGHT

        self.head=Point(self.w/2,self.h/2) #starting at the middle
        self.snake=[self.head,Point(self.head.x-BLOCK_SIZE,self.head.y),Point(self.head.x-(2*BLOCK_SIZE),self.head.y)]
        self.score=0
        self.food=None
        self._place_food()  
        self.frame_iteration=0
         
    def _place_food(self):
        x=random.randint(0,(self.w-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        y=random.randint(0,(self.h-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        self.food=Point(x,y)
        if self.food in self.snake:
            self._place_food()
            

        
    def play_step(self,action):
        #collect the user input 
        self.frame_iteration+=1
        for event in pygame.event.get():
            if event.type== pygame.QUIT:
                pygame.quit()
                quit()
           
        #move our snake 
        
        self._move(action)
        self.snake.insert(0,self.head)
        #reward
        reward = 0
        #check if game over ---> quit if it is the case 
        
        game_over=False

        if self.is_collision() or self.frame_iteration >100*len(self.snake): 
            game_over=True
            reward=-10
            return reward,game_over,self.score
        #place new food or just move 
        if self.head==self.food:
            self.score+=1
            reward=10
            self._place_food()
        else:
            self.snake.pop() # remove the last element from the snake
            
            
        #update the ui pygame and the clock 
        # return if game over and return the score
        
        self._update_ui()
        self.clock.tick(SPEED)
        return reward,game_over, self.score
    
    
    def is_collision(self,pt=None):
        #check if it hit s the boundary or iteslt
     
        if pt is None:
            pt=self.head
        if pt.x>self.w-BLOCK_SIZE or pt.x <0 or pt.y >self.h-BLOCK_SIZE or pt.y <0:
            return True  
        
        
        # if self.head.x>=self.w:
        #     self.head=Point(0,self.head.y)
        # elif self.head.x<=0:
        #     self.head=Point(self.w-BLOCK_SIZE,self.head.y)
        # elif self.head.y>=self.h-BLOCK_SIZE:
        #     self.head=Point(self.head.x,0)
        # elif self.head.y<=0:
        #     self.head=Point(self.head.x,self.h-BLOCK_SIZE)
            
        if self.head in self.snake[1:]:
            return True
        return False
        
        
    def _move(self,action):
        # [straigh,right,left]
        clock_wise=[Direction.RIGHT,Direction.DOWN,Direction.LEFT,Direction.UP]
        idx=clock_wise.index(self.direction)
        if np.array_equal(action, [1,0,0,]):
            new_dir=clock_wise[idx] 
        elif np.array_equal(action, [0,1,0,]):
            next_idx=(idx+1)%4
            new_dir=clock_wise[next_idx]  #turn right
        else:  #[0,0,1]
            next_idx=(idx-1)%4
            new_dir=clock_wise[next_idx]    #left turn
            
        self.direction=new_dir
        
        #update the head of the snake
        x=self.head.x
        y=self.head.y

        if self.direction==Direction.RIGHT:
            x+=BLOCK_SIZE
        elif self.direction==Direction.LEFT:
            x-=BLOCK_SIZE
        elif self.direction==Direction.UP:
            y-=BLOCK_SIZE
        elif self.direction==Direction.DOWN:
            y+=BLOCK_SIZE
        self.head=Point(x,y)
            
    def _update_ui(self):
        self.display.fill(BLACK)
        for point in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(point.x,point.y,BLOCK_SIZE,BLOCK_SIZE))
            #draw the snake
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(point.x+4,point.y+4,12,12))
            #draw the food
        pygame.draw.rect(self.display,RED,pygame.Rect(self.food.x,self.food.y,BLOCK_SIZE,BLOCK_SIZE))
        #draw the score
        text=font.render("Score: "+str(self.score),True,WHITE)
        self.display.blit(text,[0,0])
        pygame.display.flip()  # without this command we will not see changes 
            

        
    #we want to control this class from agent
    
    #for changing the game to let agent play it we must add : 
        #reset funtion
        #implement the reward
        #play(action ) -> return direction
        #game iteration
        #change is_collision fucntion
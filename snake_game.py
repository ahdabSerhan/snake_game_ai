from math import gamma
from tarfile import BLOCKSIZE
import pygame 
import random
from enum import Enum
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
SPEED=5
BLACK=(0,0,0)
WHITE=(255,255,255)
RED=(200,0,0)
BLUE1=(0,0,255)
BLUE2=(0,100,255)

class SnakeGame:
    def __init__(self,w=640,h=480):
        self.w=w
        self.h=h
        
        #init the display
        self.display=pygame.display.set_mode((self.w,self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        
        #init the initial state and food
        self.direction=Direction.RIGHT

        self.head=Point(self.w/2,self.h/2) #starting at the middle
        self.snake=[self.head,Point(self.head.x-BLOCK_SIZE,self.head.y),Point(self.head.x-(2*BLOCK_SIZE),self.head.y)]
        self.score=0
        self.food=None
        self._place_food()
        
        
        
    def _place_food(self):
        x=random.randint(0,(self.w-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        y=random.randint(0,(self.h-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        self.food=Point(x,y)
        if self.food in self.snake:
            self._place_food()
            

        
    def play_step(self):
        #collect the user input 
        for event in pygame.event.get():
            if event.type== pygame.QUIT:
                pygame.quit()
                quit()
            if event.type==pygame.KEYDOWN:
                if event.key ==pygame.K_LEFT:
                    self.direction=Direction.LEFT
                elif event.key ==pygame.K_RIGHT:
                    self.direction=Direction.RIGHT
                elif event.key ==pygame.K_UP:
                    self.direction=Direction.UP
                elif event.key ==pygame.K_DOWN:
                    self.direction=Direction.DOWN
        #move our snake 
        
        self._move(self.direction)
        self.snake.insert(0,self.head)
        #check if game over ---> quit if it is the case 
        game_over=False

        if self._is_collision(): 
            game_over=True
            return game_over,self.score
        #place new food or just move 
        if self.head==self.food:
            self.score+=1
            self._place_food()
        else:
            self.snake.pop() # remove the last element from the snake
            
            
        #update the ui pygame and the clock 
        # return if game over and return the score
        
        self._update_ui()
        self.clock.tick(SPEED)
        return game_over, self.score
    
    
    def _is_collision(self):
        #check if it hit s the boundary or iteslt
        # if self.head.x>self.w-BLOCK_SIZE or self.head.x <0 or self.head.y >self.h-BLOCK_SIZE or self.head.y <0:
        #     return True
        
        
        if self.head.x>=self.w:
            self.head=Point(0,self.head.y)
        elif self.head.x<=0:
            self.head=Point(self.w-BLOCK_SIZE,self.head.y)
        elif self.head.y>=self.h-BLOCK_SIZE:
            self.head=Point(self.head.x,0)
        elif self.head.y<=0:
            self.head=Point(self.head.x,self.h-BLOCK_SIZE)
            
        if self.head in self.snake[1:]:
            return True
        return False
        
        
    def _move(self,direction):
        #update the head of the snake
        x=self.head.x
        y=self.head.y
        print("self.head,y ",y)


        if direction==Direction.RIGHT:
            x+=BLOCK_SIZE
        elif direction==Direction.LEFT:
            x-=BLOCK_SIZE
        elif direction==Direction.UP:
            y-=BLOCK_SIZE
        elif direction==Direction.DOWN:
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
            

        
if __name__=='__main__':
    game= SnakeGame()
    
    
    while True:
        game_over,score=game.play_step()
        
        if game_over==True: break
    
    print('Final Score',score)
    pygame.quit()
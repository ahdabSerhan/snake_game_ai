import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
from random import randint
curses.initscr()
win=curses.newwin(20,60,0,0)
win.keypad(1)
curses.noecho()
curses.curs_set(0)
win.border(0)
win.nodelay(1)


snake=snake = [[4,10], [4,9], [4,8]]  
food = [10,20]                                                    
win.addch(food[0], food[1], '*')

ESC=27
key=KEY_RIGHT
# game logic
score=0

while key!=ESC:
    win.border(0)
    win.addstr(0,2,'Score'+ str(score)+ ' ')
    win.timeout(150-(len(snake))//5 + len(snake)//10 %120)
    prev_key=key
    event=win.getch()
    key = event if event!=-1 else prev_key 
    if key not in [curses.KEY_LEFT, curses.KEY_RIGHT,curses.KEY_UP,curses.KEY_DOWN,ESC]:
        key=prev_key
    snake.insert(0, [snake[0][0] + (key == KEY_DOWN and 1) + (key == KEY_UP and -1), snake[0][1] + (key == KEY_LEFT and -1) + (key == KEY_RIGHT and 1)])

    if snake[0][0] == 0: snake[0][0] = 18
    if snake[0][1] == 0: snake[0][1] = 58
    if snake[0][0] == 19: snake[0][0] = 1
    if snake[0][1] == 59: snake[0][1] = 1
        
    

    
    if snake[0] in snake[1:]: break #check if the snake collied with itself
    if snake[0] == food :
        score+1
        food=[]
        while food ==[]:
            food= [randint(1,18),randint(1,58)]
            if food in snake:
                food=[]
        win.addch(food[0],food[1],'#')
    else:
        last= snake.pop() #move the snake
        win.addch(last[0],last[1],' ')
        
    win.addch(snake[0][0],snake[0][1],'#')
    
curses.endwin()
print("\nScore - " + str(score))
print("http://bitemelater.in\n")

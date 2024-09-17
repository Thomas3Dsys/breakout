
import random
from turtle import Screen
import time
import keyboard
from paddlesize import PaddleSize
from scoreboard import Scoreboard
from paddle import Paddle
from ball import Ball
from field import BrickField
from powerup import PowerUp
from gamemodifier import GameModifier



screen = Screen()
screensize =(720,800)
screen.setup(width=screensize[0], height=screensize[1])
screen.bgcolor("black")
screen.title("BREAKOUT")
screen.mode("world")
screen.setworldcoordinates(0,0,screensize[0], screensize[1])
default_wait_time = .025
wait_time = .025
wait_increment = .025
center = (screensize[0]/2, screensize[1]/2)
left= (20, screensize[1]/2)
top= (screensize[0]/2, screensize[1]-20)

screen.tracer(0) # only draw when asked to on refresh of screen

xcount= 9
ycount= 5
x_plain_coord = 40
default_paddle_size = (100,20)

paddle = Paddle(screensize = screensize, x_plain_coord=x_plain_coord, size= default_paddle_size)

# screen.update()
# paddle = paddle
# paddle.recenter()
# screen.update()

field = BrickField(screen=screen, screensize = screensize,field_padding =(20,100),xcount= xcount, ycount=ycount, brick_size=(60,25), brick_padding=(15,15) )
scoreboard = Scoreboard(screensize, xcount * ycount )
ball = Ball(screensize, center)
is_paused = True

active_modifiers = {}
offpower = {
            "start_time":time.time(),
            "active_length":0,
            "is_active":False,
            "activated":False
                             }


def restart():
    global paddle, field, scoreboard, ball,  is_paused, screen
    paddle.reset()
    field.reset()
    scoreboard.reset()
    ball.reset()
    screen.update()
    is_paused = True

scoreboard.write_menu()
screen.update()

is_game_on = True

def exit_app():
    global is_game_on 
    is_game_on = False
    exit()

def toggle_menu():
    scoreboard.toggle_menu()

def start():
    global is_paused
    is_paused = False
    scoreboard.do_start()


##CHEATS / TESTING
def small():
    if keyboard.is_pressed("alt"): 
         power = {
                                 "start_time":time.time(),
                                 "active_length":20,
                                 "is_active":True,
                                 "activated":False
                             }
         active_modifiers[GameModifier.SMALLPADDLE] = power
     
def large():
    if keyboard.is_pressed("alt"): 
         power = {
                                 "start_time":time.time(),
                                 "active_length":20,
                                 "is_active":True,
                                 "activated":False
                             }
                    
         active_modifiers[GameModifier.BIGPADDLE] = power
     
def default():
    if keyboard.is_pressed("alt"):
       
        active_modifiers[GameModifier.BIGPADDLE] = offpower
        active_modifiers[GameModifier.SMALLPADDLE] = offpower
    
def increase_speed():
    global default_wait_time
    if keyboard.is_pressed("alt"):
        default_wait_time = .0125
        print("FAST")

def regular_speed():
    global default_wait_time
    if keyboard.is_pressed("alt"):
        default_wait_time = .025
        print("REGULAR")

def decrease_speed():#increase wait time
    global default_wait_time
    if keyboard.is_pressed("alt"):
        default_wait_time = .1
        print("SLOW")

## END CHEATS / TESTING

def pause():
    global is_paused
    is_paused = not is_paused   
    scoreboard.pause(is_paused)

screen.listen()
screen.onkey(key="Left", fun=paddle.left)
screen.onkey(key="Right", fun=paddle.right)
screen.onkey(key="p", fun=pause)
screen.onkey(key="space", fun=start)
screen.onkey(key="r", fun=restart)
screen.onkey(key="x", fun=exit_app)

screen.onkey(key="1", fun=decrease_speed)
screen.onkey(key="2", fun=regular_speed)
screen.onkey(key="3", fun=increase_speed)

screen.onkey(key="Tab", fun=toggle_menu)

screen.onkey(key="s", fun=small)
screen.onkey(key="l", fun=large)
screen.onkey(key="d", fun=default)


screen.bgcolor("black")
is_round_on = True
ball.reset()
field.draw_field()

powerups = []
powerup_active_time_multipliers = (.8, 1.3) 

def handle_powerups():
    remove_powerup_indexes = []
    #for all active power ups
    for p in range(0,len(powerups)):
        powerup = powerups[p]
        
        #randomize active length within range for each powerup type
        # slow  = 10 * (random .8 to 1.3)
        # fast  =  7 * (random .8 to 1.3)
        # Large = 30 * (random .8 to 1.3)
        # Small = 10 * (random .8 to 1.3)

        if paddle.is_powerup_hit(powerup):
            active_time = 0
            random_multiplier = random.uniform(powerup_active_time_multipliers [0], powerup_active_time_multipliers [1])
            score_add = 2
            match powerup.power:
                case GameModifier.BIGPADDLE:
                    active_time = 30 * random_multiplier
                case GameModifier.SMALLPADDLE:
                    active_time = 10 * random_multiplier
                    score_add = 4 # more points for hard powerUps (downs)
                case GameModifier.FAST:
                    active_time = 7 * random_multiplier
                    score_add = 4 
                case GameModifier.SLOW:
                    active_time = 10 * random_multiplier
                case _:
                    pass

            scoreboard.increase_score(score_add)
            power = {
                             "start_time":time.time(),
                             "active_length":active_time,
                             "is_active":True,
                             "activated":False
                         }
                    
            active_modifiers[powerup.engage()] = power

        # is power up dead? remove
        if powerup.get_position()[1] <= 0:
            powerup.alive = 0
            remove_powerup_indexes.append(p)

    for q in range(0,len(remove_powerup_indexes)):
        powerups.pop(q)

    for powerup in powerups:
        powerup.move()
            
def handle_fast_powerup():
    global wait_time
    if(GameModifier.FAST in active_modifiers):
        fast = active_modifiers[GameModifier.FAST]
    else:
        fast = None
        
    if fast:
        if fast['is_active']:
            elapsed = time.time() - fast['start_time']
            if elapsed > fast['active_length']:
                fast['is_active'] = False
                scoreboard.modify_active_powerups(GameModifier.FAST, False)
                wait_time = default_wait_time
            if fast['is_active']:
                print(f"Fast Time Left :{fast['active_length'] - elapsed}")  
                if not fast['activated']:
                    fast['activated'] = True
                    wait_time = .0125
                    fast['start_time'] = time.time()
                    scoreboard.modify_active_powerups(GameModifier.SLOW, False)
                    scoreboard.modify_active_powerups(GameModifier.FAST, True)
        else:
            wait_time = default_wait_time
            scoreboard.modify_active_powerups(GameModifier.FAST, False)
    return fast

def handle_slow_powerup():
    global wait_time
    if(GameModifier.SLOW in active_modifiers):
        slow = active_modifiers[GameModifier.SLOW]
    else:
        slow = None
        
    if slow:
        if slow['is_active']:
            elapsed = time.time() - slow['start_time']
            if elapsed > slow['active_length']:
                 slow['is_active'] = False
                 scoreboard.modify_active_powerups(GameModifier.SLOW, False)
                 wait_time = default_wait_time
            if slow['is_active']:
                  print(f"Slow Time Left :{slow['active_length'] - elapsed}")  
                  if not slow['activated']:
                    slow['activated'] = True
                    wait_time = .05   
                    slow['start_time'] = time.time()
                    scoreboard.modify_active_powerups(GameModifier.FAST, False)
                    scoreboard.modify_active_powerups(GameModifier.SLOW, True)
        #else:
         #   wait_time = default_wait_time
            #scoreboard.modify_active_powerups(GameModifier.SLOW, False)
                
    return slow
        
def handle_bigpaddle_powerup():
    global paddle
    if(GameModifier.BIGPADDLE in active_modifiers):
        paddle_power = active_modifiers[GameModifier.BIGPADDLE]
    else:
        paddle_power = None
        
    if paddle_power:
        if paddle_power['is_active']:
            elapsed = time.time() - paddle_power['start_time']
            if elapsed > paddle_power['active_length']:
                paddle_power['is_active'] = False
                scoreboard.modify_active_powerups(GameModifier.BIGPADDLE, False)
                paddle.set_paddle_shape(PaddleSize.DEFAULT)
            if paddle_power['is_active']:
                print(f"Big Paddle Time Left :{paddle_power['active_length'] - elapsed}")
                if not paddle_power['activated']:
                    paddle_power['start_time'] = time.time()
                    paddle.set_paddle_shape(PaddleSize.LARGE)
                    paddle_power['activated'] = True
                    scoreboard.modify_active_powerups(GameModifier.SMALLPADDLE, False)
                    scoreboard.modify_active_powerups(GameModifier.BIGPADDLE, True)
     
def handle_smallpaddle_powerup():
    global paddle
    if(GameModifier.SMALLPADDLE in active_modifiers):
        paddle_power = active_modifiers[GameModifier.SMALLPADDLE]
    else:
        paddle_power = None
        
    if paddle_power:
        if paddle_power['is_active']:
            elapsed = time.time() - paddle_power['start_time']
            if elapsed > paddle_power['active_length']:
                paddle_power['is_active'] = False
                scoreboard.modify_active_powerups(GameModifier.SMALLPADDLE, False)
                paddle.set_paddle_shape(PaddleSize.DEFAULT)
            if paddle_power['is_active']:
                print(f"Small Paddle Time Left :{paddle_power['active_length'] - elapsed}")  
                if not paddle_power['activated']:
                    paddle_power['start_time'] = time.time()
                    paddle.set_paddle_shape(PaddleSize.SMALL)
                    paddle_power['activated'] = True
                    scoreboard.modify_active_powerups(GameModifier.BIGPADDLE, False)
                    scoreboard.modify_active_powerups(GameModifier.SMALLPADDLE, True)
    return paddle_power



# def handle_default_paddle():
#     global paddle
#     is_big = False
#     is_small = False
    
#     if GameModifier.BIGPADDLE in active_modifiers:
#         lg_paddle = active_modifiers[GameModifier.BIGPADDLE]
#         if lg_paddle['is_active']:
#             is_big = True
#         else:
#             is_big = False
#             scoreboard.modify_active_powerups(GameModifier.BIGPADDLE, False)

#     if GameModifier.SMALLPADDLE  in active_modifiers:
#         sm_paddle = active_modifiers[GameModifier.SMALLPADDLE]
#         if sm_paddle['is_active']:
#             is_small = True
#         else:
#             is_small = False
#             scoreboard.modify_active_powerups(GameModifier.SMALLPADDLE, False)
            
    
        
#     if not(is_big or is_small):
#             scoreboard.modify_active_powerups(GameModifier.BIGPADDLE, False)    
#             scoreboard.modify_active_powerups(GameModifier.SMALLPADDLE, False)    
#             paddle.set_paddle_shape(PaddleSize.DEFAULT)

            
def handle_gamemodifiers():
    global wait_time

    if not any([active_modifiers[m]['is_active'] for m in active_modifiers]):
        return

    fast = handle_fast_powerup()
    slow = handle_slow_powerup()
    handle_bigpaddle_powerup()
    handle_smallpaddle_powerup()
    #handle_default_paddle()
    
    if not fast and not slow:
        wait_time = default_wait_time


for i in range(0,20):
    speed  = random.randint(3,7)
    field.add_random_powerup(PowerUp(power=random.choice(list(GameModifier)), step=speed))
    

active_powerups = []
while is_game_on:
    if not is_paused:

        handle_gamemodifiers()

        #game speed
        time.sleep(wait_time)
        
        #check game over
        if ball.has_fallen():
            scoreboard.do_game_over()
            is_game_on = False
    
        #return a hit ball
        if paddle.is_ball_hit(ball.get_position()) :
            distance = paddle.get_hit_distance(ball.get_position())
            ball.hit_paddle(distance)
        
        #what brick did the ball hit?
        b_id = field.handle_hit(ball.get_position(), ball.size)
        if b_id  > 0:
            ball.hit_brick() #redirect ball
            if field.has_powerup(b_id):#handle if brick has a power up to drop
                power_up = field.get_powerup(b_id)
                new_power_up = power_up.drop_powerup()
                powerups.append(new_power_up)
                    
            if scoreboard.increase_score():
                is_game_on = False # game is won
                pass
            else:
                scoreboard.display()
                
        #move and catch power ups, do game modification when caught
        handle_powerups()      
        
        #move the ball each iteration
        ball.move()
        
    screen.update()
    




screen.update()
screen.exitonclick()
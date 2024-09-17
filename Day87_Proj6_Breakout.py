
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
from level import Level
screensize =(720,800)
xcount= 9
ycount= 5

brick_size=(60,25)
powerup_active_time_multipliers = (.8, 1.3) 

#defaults
level1 = Level()

#change whas is needed
level2 = Level(
    num_powerups = 10,
    slow_wait_time = .1,
    default_wait_time = .05,
    fast_wait_time = .0325,
    ball_size = 20,
    powerup_step_variation = (3,7),
    powerup_size = (50,15),
    bigpaddle_active_time = 30,
    smallpaddle_active_time=7,
    slow_active_time = 10,
    fast_active_time = 7,
    good_powerup_score_add = 2,
    bad_powerup_score_add = 4,
    x_plain_coord = 40,
    default_paddle_size = (100,20),
    paddle_fast_step = 55,
    paddle_step = 35,
    paddle_slow_step = 10)

cur_level = level1


#World Setup
screen = Screen()
screen.setup(width=screensize[0], height=screensize[1])
screen.title("BRICK BRAKE")
screen.mode("world")
screen.setworldcoordinates(0,0,screensize[0], screensize[1])
center = (screensize[0]/2, screensize[1]/2)
screen.tracer(0) # only draw when asked to on refresh of screen
screen.bgcolor("black")
wait_time = cur_level.default_wait_time


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

def exit_app():
    global is_game_on 
    is_game_on = False
    exit()

def start():
    global is_paused
    is_paused = False
    scoreboard.do_start()
    
def pause():
    global is_paused
    is_paused = not is_paused   
    scoreboard.pause(is_paused)

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
    
def go_fast():
    global wait_time
    if keyboard.is_pressed("alt"):
        wait_time = cur_level.fast_wait_time
        print("FAST")

def regular_speed():
    global wait_time
    if keyboard.is_pressed("alt"):
        wait_time = cur_level.default_wait_time
        print("REGULAR")

def go_slow():#increase wait time
    global wait_time
    if keyboard.is_pressed("alt"):
        wait_time = cur_level.slow_wait_time
        print("SLOW")
## END CHEATS / TESTING


def populate_powerups():
    for i in range(0,cur_level.num_powerups):
        speed  = random.randint(cur_level.powerup_step_variation[0],cur_level.powerup_step_variation[1])
        field.add_random_powerup(PowerUp(power=random.choice(list(GameModifier)), step=speed, size=cur_level.powerup_size))

def toggle_menu():
    scoreboard.toggle_menu()

def handle_powerups():
    remove_powerup_indexes = []
    #for all active power ups
    for p in range(0,len(powerups)):
        powerup = powerups[p]
        
        if paddle.is_powerup_hit(powerup):
            active_time = 0
            random_multiplier = random.uniform(powerup_active_time_multipliers[0], powerup_active_time_multipliers[1])
            score_add = cur_level.good_powerup_score_add
            match powerup.power:
                case GameModifier.BIGPADDLE:
                    active_time = cur_level.bigpaddle_active_time * random_multiplier
                case GameModifier.SMALLPADDLE:
                    active_time = cur_level.smallpaddle_active_time * random_multiplier
                    score_add = cur_level.bad_powerup_score_add
                case GameModifier.FAST:
                    active_time =  cur_level.fast_active_time * random_multiplier
                    score_add = cur_level.bad_powerup_score_add 
                case GameModifier.SLOW:
                    active_time = cur_level.slow_active_time* random_multiplier
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
                wait_time = cur_level.default_wait_time
            if fast['is_active']:
                print(f"Fast Time Left :{fast['active_length'] - elapsed}")  
                if not fast['activated']:
                    fast['activated'] = True
                    wait_time = cur_level.fast_wait_time
                    fast['start_time'] = time.time()
                    scoreboard.modify_active_powerups(GameModifier.SLOW, False)
                    scoreboard.modify_active_powerups(GameModifier.FAST, True)
        else:
            wait_time = cur_level.default_wait_time
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
                 wait_time = cur_level.default_wait_time
            if slow['is_active']:
                  print(f"Slow Time Left :{slow['active_length'] - elapsed}")  
                  if not slow['activated']:
                    slow['activated'] = True
                    wait_time = cur_level.slow_wait_time   
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

def handle_gamemodifiers():
    global wait_time

    if not any([active_modifiers[m]['is_active'] for m in active_modifiers]):
        return

    fast = handle_fast_powerup()
    slow = handle_slow_powerup()
    handle_bigpaddle_powerup()
    handle_smallpaddle_powerup()
    
    if not fast and not slow:
        wait_time = cur_level.default_wait_time


#Game Objects        

      

paddle = Paddle(screensize = screensize, 
                x_plain_coord=cur_level.x_plain_coord, 
                size= cur_level.default_paddle_size,
                fast_step = cur_level.paddle_fast_step,
                step = cur_level.paddle_step,
                slow_step= cur_level.paddle_slow_step
                )
field = BrickField(screen=screen, screensize = screensize,field_padding =(20,100),xcount= xcount, ycount=ycount, brick_size=brick_size, brick_padding=(15,15) )
scoreboard = Scoreboard(screensize, xcount * ycount )
ball = Ball(screensize, center, cur_level.ball_size)
is_paused = True
scoreboard.write_menu()
screen.update()
is_game_on = True
is_round_on = True
ball.reset()
field.draw_field()
powerups = []
populate_powerups()
active_powerups = []


#Handle Inputs
screen.listen()
screen.onkey(key="Left", fun=paddle.left)
screen.onkey(key="Right", fun=paddle.right)
screen.onkey(key="p", fun=pause)
screen.onkey(key="space", fun=start)
screen.onkey(key="r", fun=restart)
screen.onkey(key="x", fun=exit_app)

screen.onkey(key="1", fun=go_slow)
screen.onkey(key="2", fun=regular_speed)
screen.onkey(key="3", fun=go_fast)

screen.onkey(key="Tab", fun=toggle_menu)

screen.onkey(key="s", fun=small)
screen.onkey(key="l", fun=large)
screen.onkey(key="d", fun=default)


#Main Game Loop
while is_game_on:
    if not is_paused:

        handle_gamemodifiers()

        #game speed
        print(f"w:{wait_time}")
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
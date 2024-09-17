
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
from gamelogic import GameLogic

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

screen = Screen()
game = GameLogic(cur_level, screen)
screen.title("BRICK BRAKE")
screen.tracer(0) # only draw when asked to on refresh of screen
wait_time = cur_level.default_wait_time

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
    game.scoreboard.do_start()
    
def pause():
    global is_paused
    is_paused = not is_paused   
    game.scoreboard.pause(is_paused)

##CHEATS / TESTING
def small():
    if keyboard.is_pressed("alt"): 
         power = {
                                 "start_time":time.time(),
                                 "active_length":20,
                                 "is_active":True,
                                 "activated":False
                             }
         game.active_modifiers[GameModifier.SMALLPADDLE] = power
     
def large():
    if keyboard.is_pressed("alt"): 
         power = {
                                 "start_time":time.time(),
                                 "active_length":20,
                                 "is_active":True,
                                 "activated":False
                             }
                    
         game.active_modifiers[GameModifier.BIGPADDLE] = power
     
def default():
    if keyboard.is_pressed("alt"):
       
        game.active_modifiers[GameModifier.BIGPADDLE] = offpower
        game.active_modifiers[GameModifier.SMALLPADDLE] = offpower
    
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


is_paused = True
is_game_on = True
is_round_on = True

game.scoreboard.write_menu()
game.ball.reset()
game.field.draw_field()
game.populate_powerups()
game.screen.update()


#Handle Inputs
screen.listen()
screen.onkey(key="Left", fun=game.paddle.left)
screen.onkey(key="Right", fun=game.paddle.right)
screen.onkey(key="p", fun=pause)
screen.onkey(key="space", fun=start)
screen.onkey(key="r", fun=restart)
screen.onkey(key="x", fun=exit_app)

screen.onkey(key="1", fun=go_slow)
screen.onkey(key="2", fun=regular_speed)
screen.onkey(key="3", fun=go_fast)

screen.onkey(key="Tab", fun=game.toggle_menu)

screen.onkey(key="s", fun=small)
screen.onkey(key="l", fun=large)
screen.onkey(key="d", fun=default)


#Main Game Loop
while is_game_on:
    if not is_paused:

        game.handle_gamemodifiers()

        #game speed
        print(f"w:{wait_time}")
        time.sleep(wait_time)
        
        #check game over
        if game.ball.has_fallen():
            game.scoreboard.do_game_over()
            is_game_on = False
    
        #return a hit ball
        if game.paddle.is_ball_hit(game.ball.get_position()) :
            distance = game.paddle.get_hit_distance(game.ball.get_position())
            game.ball.hit_paddle(distance)
        
        #what brick did the ball hit?
        b_id = game.field.handle_hit(game.ball.get_position(), game.ball.size)
        if b_id  > 0:
            game.ball.hit_brick() #redirect ball
            if game.field.has_powerup(b_id):#handle if brick has a power up to drop
                power_up = game.field.get_powerup(b_id)
                new_power_up = power_up.drop_powerup()
                game.powerups.append(new_power_up)
                    
            if game.scoreboard.increase_score():
                is_game_on = False # game is won
                pass
            else:
                game.scoreboard.display()
                
        #move and catch power ups, do game modification when caught
        game.handle_powerups()      
        
        #move the ball each iteration
        game.ball.move()
        
    game.screen.update()

game.screen.update()
screen.exitonclick()
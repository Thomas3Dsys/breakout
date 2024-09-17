
# import random
from turtle import Screen
import time
import keyboard

from gamemodifier import GameModifier
from level import Level
from gamelogic import GameLogic

#move to levels file?
levels = [ Level(1,
              brick_array_size = (4,1), # (9,2)
              default_paddle_size = (120,22),
              default_wait_time =.06,
              num_powerups = 8,
              bigpaddle_active_time = 30
                ),
          Level(2, 
              brick_array_size = (9,4),
              num_powerups = 6
              ),
          Level(3, 
              screensize = (1000,800),
              brick_array_size = (12,6),
              ball_size = 18,
              default_paddle_size = (90,18),
              default_wait_time =.04,
              num_powerups = 2,
              bigpaddle_active_time = 10
              )    
          ]




screen = Screen()

def setup_screen(screensize):
    global screen    
    screen = Screen()
    screen.mode("world")
    screen.setup(width=screensize[0], height=screensize[1])
    screen.setworldcoordinates(0,0,screensize[0], screensize[1])
    screen.bgcolor("black")
    screen.title("BRICK BRAKE")
    screen.tracer(0) # only draw when asked to on refresh of screen


def reset_screen(screensize):
    global screen    
    screen = Screen()
    screen.setup(width=screensize[0], height=screensize[1])


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

restart_flag = False
def set_restart_flag():
    global restart_flag
    restart_flag = True    

def restart():
    global level_itr, restart_flag, is_paused
    restart_flag = False  
    is_paused = True
    level_itr -= 1
    next_level(True)


def brake():##### CHEAT / DEBUG #####
    game.field.remove_brick_by_id(game.field.bricks[0].id)
    game.field.remove_dead_bricks()
    screen.update()

def go_fast():##### CHEAT / DEBUG #####
     global wait_time
     wait_time = 0



def setup_listen():
    global screen    
    #Handle Inputs
    screen.listen()
    screen.onkey(key="Left", fun=game.paddle.left)#do_left)
    screen.onkey(key="Right", fun=game.paddle.right)#do_right
    screen.onkey(key="p", fun=pause)
    screen.onkey(key="space", fun=start)
    
    screen.onkey(key="f", fun=go_fast)##### CHEAT / DEBUG #####
    screen.onkey(key="b", fun=brake)##### CHEAT / DEBUG #####
   
    screen.onkey(key="r", fun=set_restart_flag)
    screen.onkey(key="x", fun=exit_app)


    screen.onkey(key="Tab", fun=game.scoreboard.toggle_menu)


level_itr = 0
setup_screen(levels[level_itr].screensize)
game = GameLogic(levels[level_itr])
setup_listen()
start_display_y = game.field.get_brick_min_y()
game.scoreboard.display_start_info(f"Level {game.level.iteration}",start_display_y)

wait_time = game.level.default_wait_time

is_paused = True
is_game_on = True


def next_level(restart = False):
    global level_itr, game,is_game_on
    level_itr += 1
    
    if level_itr >= len(levels):
       game.scoreboard.win()
       is_game_on = False
       return
    
    reset_screen(levels[level_itr].screensize)
    game.new_level(levels[level_itr])
    
    start_display_y = game.field.get_brick_min_y() 
    if restart:
        game.scoreboard.display_start_info(f"Level {game.level.iteration}",start_display_y)
    else:
        game.scoreboard.level_complete(f"Level {game.level.iteration}",start_display_y)
    

    

print(f"wait:{wait_time}")

#Main Game Loop
while is_game_on:
    if not is_paused:

        game.handle_gamemodifiers()

        #game speed
        time.sleep(wait_time)
        
        #check game over
        if game.ball.has_fallen():
            game.scoreboard.do_game_over()
            is_game_on = False
    
        #return a hit ball
        if game.paddle.is_ball_hit(game.ball.get_position(), game.ball.size) :
            distance = game.paddle.get_hit_distance(game.ball.get_position())
            game.ball.hit_paddle(distance)
        
        #what brick did the ball hit?
        b_id = game.field.get_hit_id(game.ball.get_position(), game.ball.size)
        if b_id  > -1:
            game.ball.hit_brick() #redirect ball
            if game.field.has_powerup(b_id):#handle if brick has a power up to drop
                power_up = game.field.get_powerup(b_id)
                new_power_up = power_up.drop_powerup()
                game.powerups.append(new_power_up)
            game.field.remove_brick_by_id(b_id)#remove hit brick
            game.scoreboard.increase_score()
        
        if game.is_level_complete():
            next_level()
            is_paused = True # game is won
            #pass
        else:
            game.scoreboard.display()
                
        #move and catch power ups, do game modification when caught
        game.handle_powerups()      
        
        #move the ball each iteration
        game.ball.move()
     
    if restart_flag:
        restart()


    screen.update()
   

screen.update()
screen.exitonclick()
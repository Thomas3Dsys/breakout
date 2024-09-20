from turtle import Screen, Turtle
import time
from level import Level
from gamelogic import GameLogic
from paddlesize import PaddleSize




def test():
    wait_time = "0"
    screen = Screen()
    is_game_on = True
    game:GameLogic = None
    is_paused = False
    screen = Screen()
    
    def setup_screen(screensize):
        global screen    
        screen = Screen()
        screen.mode("world")
        screen.setup(width=screensize[0]+10, height=screensize[1]+10)
        screen.setworldcoordinates(0,0,screensize[0], screensize[1])
        screen.bgcolor("black")
        screen.title("BRICK BRAKE")
        screen.tracer(0) # only draw when asked to on refresh of screen



    level = Level(1)
    setup_screen(level.screensize)

    
    #Debug ball and paddle hits
    center = (level.screensize[0]/2, level.screensize[1]/2)
    half_paddle = level.default_paddle_size[0]  /2
    start  =(center[0]-half_paddle-10, center[1])
    level.ball_start_position = start


    #debug ball edge
    #start  =(10, level.screensize[1]/2)
    #level.ball_start_position = start
    #level.paddle_start_x = level.default_paddle_size[0] /2
    #level.ball_size = .25


    game = GameLogic(level)
    game.paddle.set_paddle_shape(PaddleSize.LARGE)
    
    def pause():
        global is_paused
        is_paused = not is_paused   
        game.scoreboard.pause(is_paused)

    
    def setup_listen():
        global screen    
        #Handle Inputs
        screen.listen()
        screen.onkey(key="Left", fun=game.paddle.left)
        screen.onkey(key="Right", fun=game.paddle.right)
        screen.onkey(key="p", fun=pause)
        screen.onkey(key="space", fun=start)
   
        #screen.onkey(key="r", fun=set_restart_flag)
        #screen.onkey(key="x", fun=exit_app)

        screen.onkey(key="Tab", fun=game.scoreboard.toggle_menu)


    
    wait_time = game.level.default_wait_time

    # screen.listen()
    # screen.onkey(key="Left", fun=game.paddle.left)
    # screen.onkey(key="Right", fun=game.paddle.right)
    setup_listen()

    #game.ball.ball_heading = 225
    

    #straight down
    game.ball.ball_heading = 270
    

    start = time.time()
    screen.update()
    while True:
         if not is_paused: 
            time.sleep(wait_time)
         
            #debug speed
            # if(time.time() - start > 15):
            #    wait_time = game.level.default_wait_time
            #    print("default")
            # elif(time.time() - start > 10):
            #    wait_time = game.level.fast_wait_time
            #    print("fast")
            # elif(time.time() - start > 5):
            #    wait_time = game.level.slow_wait_time
            #    print("slow")


            if game.paddle.is_ball_hit(game.ball.get_position(), game.ball.size) :
                distance = game.paddle.get_hit_distance(game.ball.get_position())
                game.ball.do_hit_paddle(distance)
            game.ball.move()
            screen.update()
         
    screen.update()
    screen.exitonclick()
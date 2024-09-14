
from turtle import Screen
from scoreboard import Scoreboard
from paddle import Paddle
from ball import Ball
from field import BrickField

#import time


screen = Screen()
screensize =(1400,800)
screen.setup(width=screensize[0], height=screensize[1])
screen.bgcolor("black")
screen.title("BREAKOUT")
speed = .075

#center = (screensize[0]/2, screensize[1]/2)
center = (20, screensize[1]/2)

screen.tracer(0) # only draw when asked to on refresh of screen
scoreboard = Scoreboard(screensize)
paddle = Paddle(screensize = screensize, x_plain_coord = 35, size= (200,40), speed= 5)
ball = Ball(screensize, center)
field = BrickField(screen=screen, screensize = screensize,field_padding =(90,80),xcount= 18, ycount=8, brick_size=(60,25), brick_padding=(15,15) )

screen.update()

is_game_on = True

def exit_app():
    global is_game_on 
    is_game_on = False


screen.listen()
screen.onkey(key="Left", fun=paddle.left)
screen.onkey(key="Right", fun=paddle.right)
screen.onkey(key="x", fun=exit_app)



screen.bgcolor("black")
is_round_on = True
ball.reset()
paddle.reset()
field.draw_field() 

while is_game_on:
    #time.sleep(speed)
    #ball.move()
    if ball.has_fallen():
        scoreboard.do_game_over()
        is_game_on = False
    
    if paddle.is_ball_hit(ball.get_position()) :
        ball.hit_paddle()
        
    if field.handle_hit(ball.get_position()):
        ball.hit_brick()
        scoreboard.increase_score()


    screen.update()

screen.exitonclick()
from turtle import Turtle, Screen


class Paddle(Turtle):
    
    def __init__(self,  screensize, x_plain_coord, size, speed):
        super().__init__()
        self.screensize = screensize
        self.color("white")
        self.penup()
        self.x_plain_coord = x_plain_coord
        self.reset()
        self.is_going_left = False
        self.is_going_right = False
        screen = Screen()
        self.speed = speed
        
        self.xbounds = screensize[0]
        #self.y_position = -int(screen[1]/2)
        
        self.b_width = size[0]
        self.b_height = size[1]
        
        sX = int(size[0]/2)
        sY = int(size[1]/2)

        screen.register_shape(
            "paddle",
           (
                (sY/ 2, 0),
                (-sY / 2, 0),
                (-sY/ 2, sX),
                (sY / 2, sX)
           )
                                  )
        self.shape("paddle")
        self.setheading(180)
        self.step = 10
 
        
    def left(self):
        if self.xcor() > self.b_width/2:
            self.forward(self.step * self.speed)
    
    def right(self):
        if self.xcor() < self.screensize[0]:# - self.b_width/2:
            self.backward(self.step * self.speed)
        else:
            pass


    def is_ball_hit(self, ball_pos):
        if  abs(self.xcor() - ball_pos[0]) <= self.b_width/2 and abs(self.ycor() - ball_pos[1]) <= self.b_height/2:
            return True
        return False
    
    def reset(self):
        #self.goto(self.screensize[0]/2,self.x_plain_coord)
        self.goto(20,self.x_plain_coord)
        self.is_going_left = False
        self.is_going_right = False
        

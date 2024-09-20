from turtle import Turtle, Screen
import random

class Ball(Turtle):
    
    def __init__(self, screensize, starting_pos, step = 10, shape_size = 1):
        super().__init__()
        self.clear()
        self.speed("fastest")
        self.starting_pos = starting_pos
        self.color("white")
        self.penup()
        self.goto(starting_pos)
        
        #visual representation
        self.shape("circle")
        self.shape_size = shape_size
        self.shapesize(self.shape_size)
        
        #physics size calcualtions
        self.size = 10 * shape_size
        self.hsize = self.size / 2
        
        self.step = step
        self.screensize = screensize
        self.recenter()
        
    def recenter(self):
        self.ball_heading = random.randint(250,290)
        self.goto(self.starting_pos)

    def get_position(self):
        return self.position()#(self.xcor, self.ycor)
        
    def do_hit_paddle(self, distance):
        if distance <= -30:
            self.ball_heading  = 360  - self.ball_heading + 30
            print("hit left")
        elif distance >= 30:
            self.ball_heading  = 360  - self.ball_heading - 30
            print("hit right")
        else:
            self.ball_heading  = 360  - self.ball_heading + random.randint(-10,10)
        self.move()

    def hit_brick(self):
        self.ball_heading  = 360  - self.ball_heading #+ random.randint(-10,10) # update to have angle depend on how far from center it hit
        self.move()
        
    def move(self):
        
        self.handle_edge_ricochet()
        if self.ball_heading > 360:
            self.ball_heading = self.ball_heading - 360
          
        #self correcting heading, so there is not too much side to side
        if self.ball_heading > 135 and self.ball_heading < 180:
            self.ball_heading = 135
        elif self.ball_heading > 315 and self.ball_heading < 360:
            self.ball_heading = 315
        elif self.ball_heading >180 and self.ball_heading < 225:
            self.ball_heading = 225
        elif self.ball_heading > 0 and self.ball_heading < 45:
            self.ball_heading = 45

        self.setheading(self.ball_heading)
        
        self.forward(self.step)

    
    def handle_edge_ricochet(self):
        #left and right
        if self.xcor() <= 0 or self.xcor() >= self.screensize[0]:
             self.ball_heading  = 360 - ( self.ball_heading-180)
            
        #top collision
        if self.ycor() + self.hsize >= self.screensize[1]:
             self.ball_heading  = 360  - self.ball_heading

    def has_fallen(self):
        if self.ycor() <= 2 :
            return True
            #CHEAT/DEBUG
            #self.ball_heading  = 360  - self.ball_heading
        return False

    

        
    

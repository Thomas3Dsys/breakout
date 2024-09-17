from turtle import Turtle, Screen
import random

class Ball(Turtle):
    
    def __init__(self, screensize, starting_pos, step = 10, size = 20):
        super().__init__()
        self.starting_pos = starting_pos
        self.color("white")
        self.penup()
        self.goto(starting_pos)
        self.size = size
        self.pensize(self.size)
        self.hsize = self.size / 2
        self.shape("circle")
        self.step = step
        self.screensize = screensize
        
        
    def reset(self):
        self.ball_heading = random.randint(210,330)
        self.goto(self.starting_pos)

    def get_position(self):
        return self.position()#(self.xcor, self.ycor)
        
    def hit_paddle(self, distance):
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
        #if not self.has_fallen():
         #   self.forward(self.step)
        self.forward(self.step)
        self.handle_edge_ricochet()

    
    def handle_edge_ricochet(self):
        #left and right
        if self.xcor()+self.hsize >= self.screensize[0] or self.xcor() <= self.hsize :
            self.ball_heading  = 180  - self.ball_heading
            
        #top collision
        if self.ycor() + self.hsize >= self.screensize[1]:
             self.ball_heading  = 360  - self.ball_heading

    def has_fallen(self):
        if self.ycor() <= 2 :
            return True
            #temporary ricochet for testing
            #self.ball_heading  = 360  - self.ball_heading
        return False

    

        
    

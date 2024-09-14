from turtle import Turtle, Screen
import random

class Ball(Turtle):
    
    def __init__(self, screensize, starting_pos, step = 10):
        super().__init__()
        self.starting_pos = starting_pos
        self.screen.mode("world")
        self.screen.setworldcoordinates(0,0,screensize[0], screensize[1])
        self.color("white")
        self.penup()
        self.goto(starting_pos)
        self.size = 20
        self.pensize(self.size)
        self.hsize = self.size / 2
        self.shape("circle")
        self.step = step
        self.screensize = screensize
        #self.screen_half_height = int(screen_size[1]/2)
        #self.screen_half_width = int(screen_size[0]/2)
        self.reset()



        
    def reset(self):
        self.ball_heading = 270#random.randint(210,330)
        self.goto(self.starting_pos)

    def get_position(self):
        return self.position()#(self.xcor, self.ycor)
        
    def hit_paddle(self):
        self.ball_heading  = 360  - self.ball_heading + random.randint(-20,20)# update to have angle depend on how far from center it hit
        self.move()

    def hit_brick(self):
        self.ball_heading  = 360  - self.ball_heading + random.randint(-10,10) # update to have angle depend on how far from center it hit
        self.move()
        
    def move(self):
        self.setheading(self.ball_heading)
        if not self.has_fallen():
            self.forward(self.step)
        self.handle_edge_ricochet()

        # if self.ball_heading > 85 and self.ball_heading < 95:
        #     self.ball_heading += self.step
        
    # def paddle_return(self):
    #     self.ball_heading += 180 + random.randint(-20,20)
    #     self.ball_heading = self.ball_heading % 360
        
    # def is_off_screen(self):
    #     if self.xcor() >= self.screen_half_width or  self.xcor() <= -self.screen_half_width:
    #         return True
    #     return False
    
    def handle_edge_ricochet(self):
        #size collision
        # if self.xcor() >= self.screen_half_width - 10 or self.xcor() <= -self.screen_half_width - 10:
        #     self.ball_heading  = 180  - self.ball_heading
        #     self.move()
        
        # #top collision
        # if self.ycor() >= self.screen_half_height - 10 or self.ycor() <= -self.screen_half_height - 10:
        #     self.ball_heading  = 360  - self.ball_heading
        #     self.move()

        #left and right
        if self.xcor()+self.hsize >= self.screensize[0] or self.xcor() <= self.hsize :
            self.ball_heading  = 180  - self.ball_heading
            self.move()
            
        #top collision
        if self.ycor() + self.hsize >= self.screensize[1]:
             self.ball_heading  = 360  - self.ball_heading
             self.move()


    def has_fallen(self):
        if self.ycor() <= self.hsize:
            return True
        return False




    

        
    

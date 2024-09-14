from turtle import Turtle, Screen
from brick import Brick

class BrickField(Turtle):
    
    def __init__(self, screen, screensize, field_padding, xcount, ycount, brick_size, brick_padding):
        super().__init__()
        #Field Padding
        self.x_padding = field_padding[0]
        self.y_padding = field_padding[1]
        self.screensize = screensize
        self.screen = screen
        self.xcount = xcount
        self.ycount = ycount
        self.brick_size = brick_size
        self.brick_x_padding = brick_padding[0]
        self.brick_y_padding = brick_padding[1]
        self.bricks = []
        self.colors=["red","orange", "yellow", "blue", "purple"]

    def draw_field(self):
        id = 0
        y_position = int(self.screensize[1]) - self.y_padding 
        for j in range(0,self.ycount):
            x_position = self.x_padding 
            for i in range(0, self.xcount):
                self.bricks.append(Brick((x_position,y_position), self.brick_size, self.colors[j % (len(self.colors))],id))
                id = id + 1
                x_position = x_position + self.brick_size[0] + self.brick_x_padding
            y_position = y_position -  (self.brick_size[1]+ self.brick_y_padding)
        
        self.screen.update()   
        
    def handle_hit(self, ball_pos):
        #dont bother to check if not to min of the y positions
        bricks_minY = min([b.get_min_ycor() for b in self.bricks])
        if ball_pos[1] < bricks_minY:
            return False
        
        for brick in self.bricks:
            if brick.is_ball_hit(ball_pos):
                return True

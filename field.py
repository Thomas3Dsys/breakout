from turtle import Turtle, Screen
from brick import Brick
from gamemodifier import GameModifier
from powerup import PowerUp
import random
from typing import List

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
        self.bricks: List[Brick]= []
        self.colors=["red","orange", "yellow", "blue", "purple"]
        #self.brick_ids = []

    def draw_field(self):
        id = 0
        y_position = int(self.screensize[1]) - self.y_padding 
        for j in range(0,self.ycount):
            x_position = self.x_padding + self.brick_size[0]/2 
            for i in range(0, self.xcount):
                self.bricks.append(Brick((x_position,y_position), self.brick_size, self.colors[j % (len(self.colors))],id))
                #self.brick_ids.append(id)
                id = id + 1
                x_position = x_position + self.brick_size[0] + self.brick_x_padding
            y_position = y_position -  (self.brick_size[1]+ self.brick_y_padding)
        
        self.screen.update()   
        

    def add_powerup(self, b_id, powerup:PowerUp):
        brick:Brick = [b for b in self.bricks if b.id == b_id][0]
        brick.add_power(powerup)
        
    def add_random_powerup(self, powerup:PowerUp):
        randomid= self.get_random_non_power_up_id()
        print(f"random power up: brick id:{randomid}")
        self.add_powerup(randomid, powerup)

    def get_powerup(self, b_id) -> PowerUp:
        brick:Brick = [b for b in self.bricks if b.id == b_id][0]
        return brick.get_power()

    def get_random_non_power_up_id(self):
        return random.choice([x.id for x in self.bricks if not x.has_power()])


    def handle_hit(self, ball_pos, ball_size):
        #dont bother to check if not to min of the y positions
        if len(self.bricks) > 0:
            bricks_minY = min([b.get_min_ycor() for b in self.bricks])
            if ball_pos[1] < bricks_minY:
                return -1
        
        for brick in self.bricks:
            if brick.is_ball_hit(ball_pos,ball_size):
                return brick.id

        return -1
    

    def has_powerup(self, b_id):
        brick:Brick = [b for b in self.bricks if b.id == b_id][0]
        return brick.has_power()

    def reset(self):
         self.bricks = []
         self.draw_field()
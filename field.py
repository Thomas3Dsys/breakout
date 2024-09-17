from turtle import Turtle, Screen
from brick import Brick
from gamemodifier import GameModifier
from powerup import PowerUp
import random
from typing import List

class BrickField():
    
    def __init__(self, screensize, field_padding, xcount, ycount, brick_size, brick_padding):
        #super().__init__()
        #self.clear()
        #self.speed("fastest")
        #Field Padding
        self.x_padding = field_padding[0]
        self.y_padding = field_padding[1]
        self.screensize = screensize
        self.xcount = xcount
        self.ycount = ycount
        self.field_size = xcount * ycount
        self.brick_size = brick_size
        self.brick_x_padding = brick_padding[0]
        self.brick_y_padding = brick_padding[1]
        self.bricks: List[Brick]= []
        self.colors=["red","orange", "yellow", "blue", "purple"]
        #self.brick_ids = []
        #self.reset()

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
        
        #self.screen.update()   
        

    def remove_dead_bricks(self):
        dead_bricks = [index for index, brick in enumerate(self.bricks) if brick.alive == 0]
        for index in dead_bricks:
            self.bricks.pop(index)

    def no_more_bricks(self):
        self.remove_dead_bricks()
        return len(self.bricks) == 0

    def add_powerup(self, b_id, powerup:PowerUp):
        brick:Brick = [b for b in self.bricks if b.id == b_id][0]
        brick.add_power(powerup)
        
    def add_random_powerup(self, powerup:PowerUp):
        randomid= self.get_random_non_power_up_id()
        print(f"random power up: brick id:{randomid}, powerup:{powerup.power}")
        self.add_powerup(randomid, powerup)

    def get_powerup(self, b_id) -> PowerUp:
        brick:Brick = [b for b in self.bricks if b.id == b_id][0]
        return brick.get_power()

    def get_random_non_power_up_id(self):
        return random.choice([x.id for x in self.bricks if not x.has_power()])

    def get_brick_min_y(self):
        return min([b.get_min_ycor() for b in self.bricks])

    def get_hit_id(self, ball_pos, ball_size):
        #dont bother to check if not to min of the y positions
        if len(self.bricks) > 0:
            
            if ball_pos[1] < self.get_brick_min_y():
                return -1
        for brick in self.bricks:
            if brick.is_ball_hit(ball_pos,ball_size):
                return brick.id

        return -1
    
    def remove_brick_by_id(self, b_id):
        b_index = [index for index, brick in enumerate(self.bricks) if brick.id == b_id][0]
        self.remove_brick_by_index(b_index)
    
    def remove_brick_by_index(self, index):
         self.bricks[index].alive = 0
         self.bricks[index].remove()
         self.bricks.pop(index)

    def has_brick(self, b_id):
         found_bricks = [index for index, brick in enumerate(self.bricks) if brick.id == b_id]
         return len(found_bricks) > 0

    def has_powerup(self, b_id):
        if not self.has_brick(b_id):
            return False
        brick:Brick = [b for b in self.bricks if b.id == b_id][0]
        return brick.has_power()

    def reset(self):
        #for brick in self.bricks:
        for index in range(len(self.bricks)-1,-1,-1):
           self.remove_brick_by_index(index)
        self.bricks = []
         
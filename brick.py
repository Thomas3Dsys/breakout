from turtle import Turtle, Screen

from gamemodifier import GameModifier
from powerup import PowerUp


class Brick(Turtle):
    
    def __init__(self, position, size, color, id):
        super().__init__()
        
        #self.penup()
        self.size = size
        self.id = id
        self.alive = 1
        self.brick_width = self.size[0]
        self.brick_height = self.size[1]
        self.penup()
        self.anchor_position  = (position[0], position[1])
        
        screen = Screen()
        # screen.register_shape(
        #     "brick",
        #    (
               
        #     (0,0),
        #     (self.brick_width, 0),
        #     (self.brick_width, self.brick_height),
        #     (0, self.brick_height)
        #    )
        #                           )


        hX = self.brick_width /2
        hY = self.brick_height /2
        screen.register_shape(
            "brick",
                (
                    (-hX,hY),
                    (hX,hY),
                    (hX,-hY),
                    (-hX,-hY)
                )
            )

        self.shape("brick")
        self.color(color)
        self.goto(position)
        
        self.write(self.id,False, "right", ('Arial', 10))
        #print(f"created brick: {self.id}")
        self.setheading(90)
        self.stamp_id = self.stamp()
        self.powerup = GameModifier.NONE

        
    def get_min_ycor(self):
        return self.anchor_position[1] - self.brick_height

    def add_power(self, powerup: PowerUp):
        self.powerup = powerup
        self.powerup.set_position(self.anchor_position)
    
    def _between(self,cur, start, end):
        return cur > start and cur < end

    def has_power(self):
        if self.powerup != GameModifier.NONE:
            return True
        return False
    
    def get_power(self):
        return self.powerup  

    def is_ball_hit(self, ball_pos, ball_size):
        #bricks position is its top left
        #ball is centered around position and has ball_size
        if self.alive == 0:
            return False
        
        ball_right_in_x_area= self._between(ball_pos[0] + ball_size / 2, self.anchor_position[0] - self.brick_width/2,self.anchor_position[0] + self.brick_width/2)
        ball_left_in_x_area = self._between(ball_pos[0] - ball_size / 2, self.anchor_position[0]- self.brick_width/2,self.anchor_position[0] + self.brick_width/2)

        x_hit = ball_right_in_x_area or  ball_left_in_x_area
        
        if not x_hit:
            return False
        #top of bottom?
        #anchor is bottom left
        brick_bottom = self.anchor_position[1] 
        brick_top = self.anchor_position[1] + self.brick_height

        ball_bottom_in_y_area =   self._between(ball_pos[1]  -  ball_size / 2, brick_bottom, brick_top)
        ball_top_in_y_area =   self._between(ball_pos[1]  +  ball_size / 2, brick_bottom, brick_top)
       
        y_hit = ball_bottom_in_y_area or ball_top_in_y_area
        
        if y_hit:
            self.remove()
            return True
    

    def hit_color(self):
        self.color("black")
        print(f"clear brick id: {self.id}")

    def remove(self):
        self.hit_color()
        self.clear()
        self.goto(-100,-100)
        self.alive = 0
        
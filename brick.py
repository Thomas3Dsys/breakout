from turtle import Turtle, Screen


class Brick(Turtle):
    
    def __init__(self, position, size, color, id):
        super().__init__()
        self.color(color)
        self.penup()
        self.size = size
        self.id = id
        self.alive = 1
        self.brick_width = self.size[1]
        self.brick_height = self.size[0]
        
        self.anchor_position  = position
        self.goto(position)
        #print(f"brick({position[0]},{position[1]}> cords: {position[0]},{position[1]} >  {position[0]+brick_width},{position[1]-brick_height} )")
        
        # self.shape_coords = (
        #     (position[0],position[1]),
        #     (position[0]+ xS, position[0]),
        #     (position[0]+ xS, position[1]-yS),
        #     (position[1], position[1]-yS)
        #    )

        screen = Screen()
        screen.register_shape(
            "brick",
           (
               
            (0,0),
            (self.brick_width, 0),
            (self.brick_width, -self.brick_height),
            (0, -self.brick_height)
           )
                                  )
        self.shape("brick")
        self.write(id)
        self.stamp()
        
    def get_min_ycor(self):
        return self.anchor_position[1] - self.brick_height

    def is_ball_hit(self, ball_pos):
        #bricks position is its top left
        #ball is centered around position and has ball_size
        if self.alive == 0:
            return False
        
        
        #20 is ball size
        x_hit = ball_pos[0] + 10  >= self.anchor_position[0] - self.size[0] and ball_pos[0] -10  <= self.anchor_position[0]
        
        if not x_hit:
            return False
        #top of bottom?
        y_hit = ball_pos[1]  + 10 >= self.anchor_position[1] - self.size[1] and ball_pos[1]  - 10 <= self.anchor_position[1] + self.size[1]
        
        if y_hit:
            self.remove()
            return True
    

    def hit_color(self):
        self.goto(self.anchor_position)    
        self.color("white")
        self.stamp()
        self.goto(self.anchor_position)    
        self.color("black")
        self.stamp()

    def remove(self):
        self.hit_color()
        self.alive = 0
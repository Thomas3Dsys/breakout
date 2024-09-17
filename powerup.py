from turtle import Turtle, Screen
from gamemodifier import GameModifier

class PowerUp(Turtle):
    
    #PowerUp(power=GameModifier.BIGPADDLE, step=5)
    def __init__(self,  power : GameModifier, step, size):
        super().__init__()
        self.penup()
        self.size = size
        self.power = power
        self.alive = 0
        self.shape_width = self.size[0]
        self.shape_height = self.size[1]
        self.penup()
        self.step = step
        self.setheading(270)
        self.goto(-600,-600)
        screen = Screen()
       
        hX = self.shape_width /2
        hY = self.shape_height /2
        screen.register_shape(
            "powerup",
                (
                    (-hX,hY),
                    (hX,hY),
                    (hX,-hY),
                    (-hX,-hY)
                )
            )

        self.shape("powerup")

        if power == GameModifier.BIGPADDLE or power == GameModifier.SLOW: 
            self.color("#44ee44")
            
        elif power == GameModifier.SMALLPADDLE or power == GameModifier.FAST: 
            self.color("#ee4444")

    def set_position(self, newpos):
        self.anchor_position = newpos

    def drop_powerup(self):
        self.alive = 1
        self.goto(self.anchor_position)
        return self

    def get_size(self):
        return self.size    

    def get_position(self):
        return self.position()  
    
    def engage(self) -> GameModifier:
        print(f"Engage Power: {self.power}")
        self.clear()
        self.goto(-500,-500)
        self.alive = 0
        return self.power


    def move(self):  
        if not self.alive:
            self.goto(-500,-500)
            return 
        
        if self.ycor() > -100 :
            self.setheading(270)          
            self.forward(self.step)
        else:
            self.clear() 
                
from turtle import Turtle, Screen
from gamemodifier import GameModifier

class PowerUp(Turtle):
    
    def __init__(self,  power : GameModifier, step, size):
        super().__init__()
        self.speed("fastest")
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


        self.shapesize(stretch_wid=None, stretch_len=None, outline=4)
        self.shape("powerup")
        self.pensize(8)
        match power:
            case GameModifier.BIGPADDLE:
                 self.color("#ccffff","#6EC207")
            case GameModifier.SLOW: 
                self.color("#6EC207","#009900")  
            case GameModifier.SMALLPADDLE:  
                  self.color("#ccffff","#ee4444")
            case GameModifier.FAST:
                self.color("#6EC207","#C7253E") 
                
            case _:
                
                self.color("#FFEB00","#C7253E")


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
    
    def kill(self):
        self.clear()
        self.goto(-500,-500)
        self.alive = 0
        
    def engage(self) -> GameModifier:
        print(f"Engage Power: {self.power}")
        self.kill()
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
                
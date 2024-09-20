from turtle import Turtle, Screen
import keyboard
from paddlesize import PaddleSize
from powerup import PowerUp

class Paddle(Turtle):
    
    def __init__(self,  screensize, **kwargs):
        super().__init__()
        
        self.speed("fastest")
        self.x_plain_coord = kwargs.get('x_plain_coord',"default value")
        self.size = kwargs.get('size',(100,20))
        self.speed = kwargs.get('speed', 5)
        self.fast_step = kwargs.get('fast_step', 10)
        self.slow_step= kwargs.get('slow_step',2)
        self.step = kwargs.get('step', '10')
        
        self.paddle_start_x = kwargs.get('paddle_start_x',screensize[0]/2)
        self.paddle_start = ( self.paddle_start_x, self.x_plain_coord)

        screen = Screen() 
        sX = int(self.size[0]/2)
        sY = int(self.size[1]/2)
        
        sXL = int(self.size[0]/2)+20
        sYL = int(self.size[1]/2)+2
        
        sXS = int(self.size[0]/2)-20
        sYS = int(self.size[1]/2)-2
        screen.register_shape(
            "lpaddle",
                (
                    (-sXL,sYL),
                    (sXL,sYL),
                    (sXL,-sYL),
                    (-sXL,-sYL)
                )
            )
        
            
        screen.register_shape(
            "spaddle",
                (
                    (-sXS,sYS),
                    (sXS,sYS),
                    (sXS,-sYS),
                    (-sXS,-sYS)
                )
            )
        
            
        screen.register_shape(
            "paddle",
                (
                    (-sX,sY),
                    (sX,sY),
                    (sX,-sY),
                    (-sX,-sY)
                )
            )
        
        self.width = self.size[0]
        self.default_width = self.size[0]
        self.height = self.size[1]
        self.screensize = screensize
        self.color("white")
        self.penup()
        self.paddlesize = PaddleSize.DEFAULT
        self.setheading(90)
        self.reset()

    def set_paddle_shape(self, paddle_size:PaddleSize):
        self.paddle_size = paddle_size
        if self.paddle_size == PaddleSize.DEFAULT:
            self.shape("paddle")
            self.width = self.default_width
        if self.paddle_size == PaddleSize.LARGE:
            self.shape("lpaddle")
            self.width = self.default_width + 20
        if self.paddle_size == PaddleSize.SMALL:
            self.shape("spaddle")
            self.width = self.default_width - 20
   
        
    def left(self):
        self.goto((self.xcor()),self.x_plain_coord)
        if self.xcor() > self.width/2:
            self.setheading(180)
            if keyboard.is_pressed("shift"):
                self.forward(self.fast_step)
            elif keyboard.is_pressed("control"):
                self.forward(self.slow_step)
            else:
                self.forward(self.step)
            self.setheading(90)
    

    def right(self):
        self.goto((self.xcor()),self.x_plain_coord)
        if self.xcor() < self.screensize[0] - self.width/2:
            self.setheading(180)
            if keyboard.is_pressed("shift"):
                self.backward(self.fast_step)
            elif keyboard.is_pressed("control"):
                self.backward(self.slow_step)
            else:
                self.backward(self.step)
            self.setheading(90)
        else:
            pass


#use size of object
    def is_ball_hit(self, ball_pos, ball_size):

        #first quick check: is ball at paddle Y level
        hit_y= ball_pos[1] - ball_size/2 <= self.ycor() + self.height/2
        if not hit_y:
            return False
        
        return self.is_item_hit(ball_pos, (ball_size, ball_size))

    def _between(self,cur, start, end):
        return cur >= start and cur <= end    

    def is_item_hit(self, item_pos, item_size):
        top_paddel_y = self.ycor() + self.height/2
        bottom_paddel_y = self.ycor() - self.height/2
        top_item_y =  item_pos[1] + item_size[1] /2
        bottom_item_y = item_pos[1] - item_size[1] /2

        if bottom_item_y <= top_paddel_y: #Hit on Y coordinate
            paddle_left = self.xcor() - self.width / 2
            paddle_right =self.xcor() + self.width / 2
            item_left = item_pos[0] - item_size[0] /2
            item_right = item_pos[0] + item_size[0] /2
            if self._between(item_left, paddle_left, paddle_right) or self._between(item_right , paddle_left, paddle_right): 
               return True
        return False


    def is_powerup_hit(self, powerup:PowerUp):
        if not powerup.alive:
            return False
        else:
            item_pos = powerup.get_position()
            item_size = powerup.get_size()
            return self.is_item_hit(item_pos,item_size )

    
    #-50 to 50
    def get_hit_distance(self, ball_pos):
        offset = ball_pos[0] -self.xcor()
        #print(f"ball hit paddle {offset} from the center of the paddle")
        return offset
    
    
    def reset(self):
        self.set_paddle_shape(PaddleSize.DEFAULT)
        self.goto(self.paddle_start)
        
    def recenter(self):
        self.goto(self.paddle_start)

    def clear(self):
        self.screen.clear()

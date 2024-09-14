
from turtle import Turtle, Screen
import os

class Scoreboard(Turtle):
    
    def __init__(self,  screensize):
        super().__init__()
        
        self.penup()
        self.hideturtle()
        self.color("white")
        self.score = 0
        self.screensize = screensize
        self.display()
        
    def win(self, player):
        self.goto(0,0)
        self.color("yellow")
        self.write(f"Round Complete!", False, "center", ('MLB Padres', 40, 'bold'))
    
    def display(self):
        self.clear()
        self.goto(int(self.screensize[0]/2)-40,int(self.screensize[1]/2)-60)
        self.write(f"{self.score}", False, "right", ('MLB Padres', 40, 'bold'))
   
    def increase_score(self):
        self.score += 1

    def do_game_over(self):
        self.goto(0,int(self.screensize[1]/2)-60)
        self.write(f"GAME OVER", False, "center", ('courier', 40, 'bold'))

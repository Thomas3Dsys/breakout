
from turtle import Turtle, Screen
import os

from gamemodifier import GameModifier

class Scoreboard(Turtle):
    
    def __init__(self,  screensize, maxscore):
        super().__init__()
        self.penup()
        self.hideturtle()
        self.color("white")
        self.score = 0
        self.screensize = screensize
        self.maxscore = maxscore
        self.menus_is_diaplayed = True
        self.game_started = False
        self.toggle_menu()
        self.mod_display = ""
        self.display()
        self.start()
        self.modifiers = {
           GameModifier.FAST: False,
           GameModifier.SLOW: False,
           GameModifier.SMALLPADDLE: False,
           GameModifier.BIGPADDLE: False
           }
        
       
    
    def start(self):
        self.goto(self.screensize[0]/2,self.screensize[1]/2)
        self.write("Press Space Bar to Start", False, "center", ('MLB Padres', 40, 'bold'))

    def do_start(self):
        self.menus_is_diaplayed = False
        self.game_started = True
        self.display()
       
        
    def win(self):
        self.color("yellow")
        self.goto(self.screensize[0]/2,self.screensize[1]/2)
        self.write(f"YOU WIN!", False, "center", ('courier', 100, 'bold'))

    def display(self):
        self.clear()
        self.color("white")
        self.penup()
        self.goto(self.screensize[0]-40,self.screensize[1]-60)
        self.write(f"{self.score}", False, "right", ('MLB Padres', 40, 'bold'))
        if not self.menus_is_diaplayed:
            self.draw_tab_text()

        self.goto(10,5)
        self.color("white")
        self.write(self.mod_display, False, "left", ('courier', 12, 'bold'))
   
    def increase_score(self, amount = 1):
        self.score += amount
        if self.score == self.maxscore:
           self.win()
           return True
        return False
            
    def write_menu(self):
        self.color("gray")
        self.goto(self.screensize[0]-400,100)
        menu = """Left and Right Arrows Moves the Paddle
        Shift - Speed up paddle
        Control - Slow down paddle
        
        r - restart game
        p - pause
        x - exit game 

        Cheats!
        1, 2, 3,  change the speed
        s,l,d paddle size
        
        
Press Tab to toggle this menu"""
        
        self.write(menu, False, "left", ('courier', 10, 'bold'))


    def toggle_menu(self):
        if not self.game_started :
            return
        self.menus_is_diaplayed = not self.menus_is_diaplayed
        if not self.menus_is_diaplayed:
            self.clear()
            self.display()
            self.write_menu()
        else:
            self.clear()
            self.display()
            self.draw_tab_text()

    def draw_tab_text(self):
            self.color("gray")
            self.goto(self.screensize[0]-100,5)
            self.write("Tab : menu", False, "left", ('courier', 10, 'bold'))
            
    def do_game_over(self):
        self.color("white")
        self.goto(self.screensize[0]/2,self.screensize[1]/2)
        self.write(f"GAME OVER", False, "center", ('courier', 40, 'bold'))
    
    def pause(self,is_paused):
        if is_paused:
            self.goto(self.screensize[0]/2,self.screensize[1]/2)
            self.color("white")
            self.write("PAUSED", False, "center", ('MLB Padres', 60, 'bold'))
        else:
            self.display()
            
    def modify_active_powerups(self, powerup:GameModifier, status):
        self.modifiers[powerup] = status

        poweruplist = []
        
        #([i in self.modifiers for i == True])
        aset = [i for i in self.modifiers if self.modifiers[i] == True]
        if any(aset):
            poweruplist.append("Power Ups:")

            if self.modifiers[GameModifier.FAST]:
                poweruplist.append("[FAST MODE: ON]")
            elif self.modifiers[GameModifier.SLOW]:
                poweruplist.append("[SLOW MODE: ON]")

            if self.modifiers[GameModifier.SMALLPADDLE]:
                poweruplist.append("[SMALL PADDLE]")
            elif self.modifiers[GameModifier.BIGPADDLE]:
                poweruplist.append("[BIG PADDLE]")

        self.mod_display = " ".join(poweruplist)
        self.display()       
        

    def reset(self):
        self.score = 0
        self.display()
        self.start()
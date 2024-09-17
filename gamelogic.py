
from pickle import NONE
import random
from turtle import Screen
import time
from typing import Self
import keyboard
from paddlesize import PaddleSize
from scoreboard import Scoreboard
from paddle import Paddle
from ball import Ball
from field import BrickField
from powerup import PowerUp
from gamemodifier import GameModifier
from level import Level


class GameLogic():
    
    def __init__(self, cur_level):
        self.level = cur_level

        self.active_modifiers = {}
        ball_start_position = (self.level.screensize[0]/2, cur_level.screensize[1]/2-40)
        
        self.paddle = Paddle(
                screensize = self.level.screensize, 
                x_plain_coord=self.level.x_plain_coord, 
                size= self.level.default_paddle_size,
                fast_step = self.level.paddle_fast_step,
                step = self.level.paddle_step,
                slow_step= self.level.paddle_slow_step
                )

        self.field = BrickField(
                screensize = self.level.screensize,field_padding =(20,100),
                xcount= self.level.brick_array_size[0],
                ycount=self.level.brick_array_size[1],
                brick_size=self.level.brick_size,
                brick_padding=(15,15) 
                )
        self.field.draw_field()
        
        self.scoreboard = Scoreboard(
                self.level.screensize,
                self.level.brick_array_size[0] * self.level.brick_array_size[1] 
                )
        self.scoreboard.display()
        
        self.ball = Ball(    
                self.level.screensize, 
                ball_start_position,
                self.level.ball_size
                )

        self.powerups = []
        
        self.scoreboard.write_menu()
        self.ball.reset()
        self.populate_powerups()
        self.paddle.reset()
        self.last_print = 0

    def new_level(self, cur_level):
        self.level = cur_level
        self.active_modifiers = {}
        #ball_start_position = (self.level.screensize[0]/2, cur_level.screensize[1]/2-40)
        
        self.ball.reset()
        score = self.scoreboard.score 
        self.scoreboard.reset()
        self.scoreboard.score = score 
        self.paddle.reset()
        self.field.reset()


        
        self.scoreboard.screensize = self.level.screensize
        self.paddle.screensize = self.level.screensize
        self.ball.screensize = self.level.screensize
        self.field.screensize = self.level.screensize
        
        self.field.xcount= self.level.brick_array_size[0]
        self.field.ycount=self.level.brick_array_size[1]
        self.field.brick_size=self.level.brick_size
        
        self.field.draw_field()
        self.powerups = []
        self.scoreboard.write_menu()
        self.populate_powerups()
        self.last_print = 0


    def populate_powerups(self):
        num_to_populate = min(self.field.field_size,self.level.num_powerups)

        for i in range(0,num_to_populate):
            speed  = random.randint(self.level.powerup_step_variation[0],self.level.powerup_step_variation[1])
            
            randomPowerUp = GameModifier.NONE
            while randomPowerUp == GameModifier.NONE:
                randomPowerUp = random.choice(list(GameModifier))
            self.field.add_random_powerup(PowerUp(power=randomPowerUp, step=speed, size=self.level.powerup_size))
        

    def toggle_menu(self):
         self.scoreboard.toggle_menu()

    def handle_powerups(self, ):
        remove_powerup_indexes = []
        

        #for all active power ups
        for p in range(0,len(self.powerups)):
            powerup = self.powerups[p]
        
            if self.paddle.is_powerup_hit(powerup):
                active_time = 0
                random_multiplier = random.uniform(self.level.powerup_active_time_multipliers[0], self.level.powerup_active_time_multipliers[1])
                score_add = self.level.good_powerup_score_add
                match powerup.power:
                    case GameModifier.BIGPADDLE:
                        active_time = self.level.bigpaddle_active_time * random_multiplier
                    case GameModifier.SMALLPADDLE:
                        active_time = self.level.smallpaddle_active_time * random_multiplier
                        score_add = self.level.bad_powerup_score_add
                    case GameModifier.FAST:
                        active_time =  self.level.fast_active_time * random_multiplier
                        score_add = self.level.bad_powerup_score_add 
                    case GameModifier.SLOW:
                        active_time = self.level.slow_active_time* random_multiplier
                    case _:
                        pass

                self.scoreboard.increase_score(score_add)
                power = {
                                 "start_time":time.time(),
                                 "active_length":active_time,
                                 "is_active":True,
                                 "activated":False
                             }
                    
                self.active_modifiers[powerup.engage()] = power

            # is power up dead? remove
            if powerup.get_position()[1] <= -powerup.shape_height/2:
                powerup.alive = 0
                remove_powerup_indexes.append(p)

        
        for powerup in self.powerups:
            powerup.move()

        for q in range(0,len(remove_powerup_indexes)):
            self.powerups.pop(q)

      
    def handle_gamemodifiers(self):
        global wait_time

        if not any([self.active_modifiers[m]['is_active'] for m in self.active_modifiers]):
            return

        for modifier in list(GameModifier):
            self.manage_gamemodifier(modifier)

    def is_level_complete(self):
        if self.field.no_more_bricks():
            
            return True
        return False

    def do_modifier_affect(self,cur_modifier, affect_state):
         match cur_modifier:                
            case GameModifier.BIGPADDLE:
                if affect_state == True:
                    self.paddle.set_paddle_shape(PaddleSize.LARGE)
                else:
                    self.paddle.set_paddle_shape(PaddleSize.DEFAULT)
                print(f"Large Paddle:{affect_state}")

            case GameModifier.SMALLPADDLE:
                if affect_state == True:
                    self.paddle.set_paddle_shape(PaddleSize.SMALL)
                else:
                    self.paddle.set_paddle_shape(PaddleSize.DEFAULT)
                print(f"Small Paddle:{affect_state}")

            case GameModifier.FAST:
                if affect_state == True: 
                    wait_time = self.level.fast_wait_time 
                else:
                    wait_time = self.level.default_wait_time
                print(f"wait:{wait_time}") # print to console

            case GameModifier.SLOW:
                if affect_state == True: 
                    wait_time = self.level.slow_wait_time 
                else:
                    wait_time = self.level.default_wait_time
                print(f"wait:{wait_time}") # print to console
                
            case _:
                return 
        


    def get_opposite_modifier(self, cur_modifier:GameModifier):
        match cur_modifier:                
            case GameModifier.BIGPADDLE:
                return GameModifier.SMALLPADDLE
            case GameModifier.SMALLPADDLE:
                return GameModifier.BIGPADDLE
            case GameModifier.FAST:
                return GameModifier.SLOW
            case GameModifier.SLOW:
                return GameModifier.FAST
            case _:
                return GameModifier.NONE

    def manage_gamemodifier(self, cur_modifier:GameModifier):
        global wait_time
        if cur_modifier == GameModifier.NONE:
            return 
        if cur_modifier in self.active_modifiers:
            power_obj = self.active_modifiers[cur_modifier]
        else:
            power_obj = None
        
        opposite_modifier = self.get_opposite_modifier(cur_modifier)

        if power_obj:
            if power_obj['is_active']:
                elapsed = time.time() - power_obj['start_time']
                if elapsed > power_obj['active_length']: # Time has elapsed
                     power_obj['is_active'] = False # deactivate
                     self.scoreboard.modify_active_powerups(cur_modifier, False) # remove from scoreboard
                     self.do_modifier_affect(cur_modifier, False)
                     self.last_print = 1000 # reset printing restrictor
                     
                if power_obj['is_active']:
                     if not power_obj['activated']:# is active but not activated yet
                        self.last_print = 1000 #reset this for useage
                        self.do_modifier_affect(cur_modifier, True)
                        power_obj['start_time'] = time.time() # set the timer
                        self.scoreboard.modify_active_powerups(cur_modifier, True) # reset the scoreboard
                        self.scoreboard.modify_active_powerups(opposite_modifier, False) # will not longer be fast
                        power_obj['activated'] = True # will not be activated
                        
                     time_left = power_obj['active_length'] - elapsed # calcualte time left
                     
                     if int(time_left) < self.last_print: # only print for ever new second
                        print(f"{cur_modifier} Time Left :{int(time_left)}")  #print
                        self.last_print = int(time_left) # update print restritor counter
                      
            #else:
             #   wait_time = default_wait_time
                #scoreboard.modify_active_powerups(GameModifier.SLOW, False)
                
        return power_obj
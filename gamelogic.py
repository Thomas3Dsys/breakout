
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

        
            
    def handle_fast_powerup(self):
        global wait_time
        if(GameModifier.FAST in self.active_modifiers):
            fast = self.active_modifiers[GameModifier.FAST]
        else:
            fast = None
        
        if fast:
            if fast['is_active']:
                elapsed = time.time() - fast['start_time']
                if elapsed > fast['active_length']:
                    fast['is_active'] = False
                    self.scoreboard.modify_active_powerups(GameModifier.FAST, False)
                    wait_time = self.level.default_wait_time
                    print(f"wait:{wait_time}")
                if fast['is_active']:
                    print(f"Fast Time Left :{fast['active_length'] - elapsed}")  
                    if not fast['activated']:
                        fast['activated'] = True
                        wait_time = self.level.fast_wait_time
                        print(f"wait:{wait_time}")
                        fast['start_time'] = time.time()
                        self.scoreboard.modify_active_powerups(GameModifier.SLOW, False)
                        self.scoreboard.modify_active_powerups(GameModifier.FAST, True)
            else:
                wait_time = self.level.default_wait_time
                self.scoreboard.modify_active_powerups(GameModifier.FAST, False)
        return fast

    def handle_slow_powerup(self):
        global wait_time
        if(GameModifier.SLOW in self.active_modifiers):
            slow = self.active_modifiers[GameModifier.SLOW]
        else:
            slow = None
        
        if slow:
            if slow['is_active']:
                elapsed = time.time() - slow['start_time']
                if elapsed > slow['active_length']: # Time has elapsed
                     slow['is_active'] = False # deactivate
                     self.scoreboard.modify_active_powerups(GameModifier.SLOW, False) # remove from scoreboard
                     wait_time = self.level.default_wait_time # reset affects
                     print(f"wait:{wait_time}") # print to console
                     self.last_print = 0 # reset printing restrictor
                if slow['is_active']:
                     if not slow['activated']:# is active but not activated yet
                        self.last_print = 0 #reset this for useage
                        wait_time = self.level.slow_wait_time # enable effect
                        print(f"wait:{wait_time}") # print to console
                        slow['start_time'] = time.time() # set the timer
                        self.scoreboard.modify_active_powerups(GameModifier.SLOW, True) # reset the scoreboard
                        self.scoreboard.modify_active_powerups(GameModifier.FAST, False) # will not longer be fast
                        slow['activated'] = True # will not be activated
                        
                     time_left = slow['active_length'] - elapsed # calcualte time left
                     
                     if int(time_left) > self.last_print: # only print for ever new second
                        print(f"Slow Time Left :{time_left}")  #print
                        self.last_print = int(time_left) # update print restritor counter
                      
            #else:
             #   wait_time = default_wait_time
                #scoreboard.modify_active_powerups(GameModifier.SLOW, False)
                
        return slow
        
    def handle_bigpaddle_powerup(self):
        global paddle
        if(GameModifier.BIGPADDLE in self.active_modifiers):
            paddle_power = self.active_modifiers[GameModifier.BIGPADDLE]
        else:
            paddle_power = None
        
        if paddle_power:
            if paddle_power['is_active']:
                elapsed = time.time() - paddle_power['start_time']
                if elapsed > paddle_power['active_length']:
                    paddle_power['is_active'] = False
                    self.scoreboard.modify_active_powerups(GameModifier.BIGPADDLE, False)
                    self.paddle.set_paddle_shape(PaddleSize.DEFAULT)
                if paddle_power['is_active']:
                    print(f"Big Paddle Time Left :{paddle_power['active_length'] - elapsed}")
                    if not paddle_power['activated']:
                        paddle_power['start_time'] = time.time()
                        self.paddle.set_paddle_shape(PaddleSize.LARGE)
                        paddle_power['activated'] = True
                        self.scoreboard.modify_active_powerups(GameModifier.SMALLPADDLE, False)
                        self.scoreboard.modify_active_powerups(GameModifier.BIGPADDLE, True)
     
    def handle_smallpaddle_powerup(self):
        global paddle
        if(GameModifier.SMALLPADDLE in self.active_modifiers):
            paddle_power = self.active_modifiers[GameModifier.SMALLPADDLE]
        else:
            paddle_power = None
        
        if paddle_power:
            if paddle_power['is_active']:
                elapsed = time.time() - paddle_power['start_time']
                if elapsed > paddle_power['active_length']:
                    paddle_power['is_active'] = False
                    self.scoreboard.modify_active_powerups(GameModifier.SMALLPADDLE, False)
                    self.paddle.set_paddle_shape(PaddleSize.DEFAULT)
                if paddle_power['is_active']:
                    print(f"Small Paddle Time Left :{paddle_power['active_length'] - elapsed}")  
                    if not paddle_power['activated']:
                        paddle_power['start_time'] = time.time()
                        self.paddle.set_paddle_shape(PaddleSize.SMALL)
                        paddle_power['activated'] = True
                        self.scoreboard.modify_active_powerups(GameModifier.BIGPADDLE, False)
                        self.scoreboard.modify_active_powerups(GameModifier.SMALLPADDLE, True)
        return paddle_power

    def handle_gamemodifiers(self):
        global wait_time

        if not any([self.active_modifiers[m]['is_active'] for m in self.active_modifiers]):
            return

        fast = self.handle_fast_powerup()
        slow = self.handle_slow_powerup()
        self.handle_bigpaddle_powerup()
        self.handle_smallpaddle_powerup()
    
        if not fast and not slow:
            wait_time = self.level.default_wait_time
            print(f"wait:{wait_time}")

    def is_level_complete(self):
        if self.field.no_more_bricks():
            
            return True
        return False


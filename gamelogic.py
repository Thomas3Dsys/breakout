
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
    
    def __init__(self, cur_level, screen):
        self.level = cur_level
        self.screen = screen
        self.screen.mode("world")
        self.screen.setup(width=self.level.screensize[0], height=self.level.screensize[1])
        self.screen.setworldcoordinates(0,0,self.level.screensize[0], self.level.screensize[1])
        screen.bgcolor("black")
        

        self.active_modifiers = {}
        center = (self.level.screensize[0]/2, cur_level.screensize[1]/2)
        
        self.paddle = Paddle(
                screensize = self.level.screensize, 
                x_plain_coord=self.level.x_plain_coord, 
                size= self.level.default_paddle_size,
                fast_step = self.level.paddle_fast_step,
                step = self.level.paddle_step,
                slow_step= self.level.paddle_slow_step
                )

        self.field = BrickField(
                screen = self.screen, 
                screensize = self.level.screensize,field_padding =(20,100),
                xcount= self.level.brick_array_size[0],
                ycount=self.level.brick_array_size[1],
                brick_size=self.level.brick_size,
                brick_padding=(15,15) 
                )

        self.scoreboard = Scoreboard(
                self.level.screensize,
                self.level.brick_array_size[0] * self.level.brick_array_size[1] 
                )
        
        self.ball = Ball(    
                self.level.screensize, 
                center,
                self.level.ball_size
                )

        self.powerups = []


    def populate_powerups(self):
        for i in range(0,self.level.num_powerups):
            speed  = random.randint(self.level.powerup_step_variation[0],self.level.powerup_step_variation[1])
            self.field.add_random_powerup(PowerUp(power=random.choice(list(GameModifier)), step=speed, size=self.level.powerup_size))
        

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
            if powerup.get_position()[1] <= 0:
                powerup.alive = 0
                remove_powerup_indexes.append(p)

        for q in range(0,len(remove_powerup_indexes)):
            self.powerups.pop(q)

        for powerup in self.powerups:
            powerup.move()
            
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
                if fast['is_active']:
                    print(f"Fast Time Left :{fast['active_length'] - elapsed}")  
                    if not fast['activated']:
                        fast['activated'] = True
                        wait_time = self.level.fast_wait_time
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
                if elapsed > slow['active_length']:
                     slow['is_active'] = False
                     self.scoreboard.modify_active_powerups(GameModifier.SLOW, False)
                     wait_time = self.level.default_wait_time
                if slow['is_active']:
                      print(f"Slow Time Left :{slow['active_length'] - elapsed}")  
                      if not slow['activated']:
                        slow['activated'] = True
                        wait_time = self.level.slow_wait_time   
                        slow['start_time'] = time.time()
                        self.scoreboard.modify_active_powerups(GameModifier.FAST, False)
                        self.scoreboard.modify_active_powerups(GameModifier.SLOW, True)
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

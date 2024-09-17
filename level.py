class Level():
    
    def __init__(self, iteration, **kwargs):
        self.iteration = iteration
        #Size of the game window
        self.screensize = kwargs.get('screensize', (720,800))
        
        #size of the brick field
        self.brick_size= kwargs.get('brick_size',(60,25))
        self.brick_array_size = kwargs.get('brick_array_size',(9,5))
        self.brick_field_colors = kwargs.get('brick_field_colors',None)

        #Ball size
        self.ball_size =  kwargs.get('ball_size',20)

        #Paddle details
        self.x_plain_coord = kwargs.get('x_plain_coord', 40)
        self.default_paddle_size =  kwargs.get('default_paddle_size',(100,20))
        self.paddle_fast_step =  kwargs.get('paddle_fast_step',70)
        self.paddle_step =  kwargs.get('paddle_step',35)
        self.paddle_slow_step =  kwargs.get('paddle_slow_step',10)
        
        #Game Speed
        self.default_wait_time =  kwargs.get('default_wait_time',.05)
        self.slow_wait_time =  kwargs.get('slow_wait_time',.1)
        self.fast_wait_time =  kwargs.get('fast_wait_time',.035)
        
        #Power Ups
        self.num_powerups =  kwargs.get('num_powerups',10)
        self.powerup_size =  kwargs.get('power_up_size',(50,15))
        self.powerup_active_time_multipliers =  kwargs.get('powerup_active_time_multipliers',(.8, 1.3) )
        self.powerup_step_variation =  kwargs.get('powerup_step_variation',(3,7))
        self.bigpaddle_active_time =  kwargs.get('bigpaddle_active_time',20)
        self.smallpaddle_active_time= kwargs.get('smallpaddle_active_time',7)
        self.slow_active_time = kwargs.get('slow_active_time', 10)
        self.fast_active_time = kwargs.get('fast_active_time', 7)
        self.good_powerup_score_add =  kwargs.get('good_powerup_score_add',2)
        self.bad_powerup_score_add = kwargs.get('bad_powerup_score_add',4)
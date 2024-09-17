# from paddlesize import PaddleSize
# from scoreboard import Scoreboard
# from paddle import Paddle
# from ball import Ball
# from field import BrickField
# from powerup import PowerUp


#change whas is needed
# levelx = Level(
#     num_powerups = 10,
#     slow_wait_time = .1,
#     default_wait_time = .05,
#     fast_wait_time = .0325,
#     ball_size = 20,
#     powerup_step_variation = (3,7),
#     powerup_size = (50,15),
#     bigpaddle_active_time = 30,
#     smallpaddle_active_time=7,
#     slow_active_time = 10,
#     fast_active_time = 7,
#     good_powerup_score_add = 2,
#     bad_powerup_score_add = 4,
#     x_plain_coord = 40,
#     default_paddle_size = (100,20),
#     paddle_fast_step = 55,
#     paddle_step = 35,
#     paddle_slow_step = 10)



# restart_flag = False
# def set_restart_flag():
#     global restart_flag
#     restart_flag = True    

# def restart():
#     global game ,is_paused, restart_flag, screen
#     #screen.resetscreen()
#     #game.field.clear()
   
#     #game.ball.clear()
#     #game.scoreboard.reset()
#     #game.paddle.clear()
   
#     #setup_screen()
#     #setup_listen()
#     game = GameLogic(cur_level)
#     is_paused = True
#     restart_flag = False



# def do_left():
#     game.paddle.left

# def do_right():
#     game.paddle.right

# def toggle():
#     global game
#     game.scoreboard.toggle_menu()


# ##CHEATS / TESTING
# def small():
#     if keyboard.is_pressed("alt"): 
#          power = {
#                                  "start_time":time.time(),
#                                  "active_length":20,
#                                  "is_active":True,
#                                  "activated":False
#                              }
#          game.active_modifiers[GameModifier.SMALLPADDLE] = power
     
# def large():
#     if keyboard.is_pressed("alt"): 
#          power = {
#                                  "start_time":time.time(),
#                                  "active_length":20,
#                                  "is_active":True,
#                                  "activated":False
#                              }
                    
#          game.active_modifiers[GameModifier.BIGPADDLE] = power
     
# def default():
#     if keyboard.is_pressed("alt"):
       
#         game.active_modifiers[GameModifier.BIGPADDLE] = offpower
#         game.active_modifiers[GameModifier.SMALLPADDLE] = offpower
    
# def go_fast():
#     global wait_time
#     if keyboard.is_pressed("alt"):
#         wait_time = cur_level.fast_wait_time
#         print("FAST")

# def regular_speed():
#     global wait_time
#     if keyboard.is_pressed("alt"):
#         wait_time = cur_level.default_wait_time
#         print("REGULAR")

# def go_slow():#increase wait time
#     global wait_time
#     if keyboard.is_pressed("alt"):
#         wait_time = cur_level.slow_wait_time
#         print("SLOW")
## END CHEATS / TESTING



    # screen.onkey(key="1", fun=go_slow)
    # screen.onkey(key="2", fun=regular_speed)
    # screen.onkey(key="3", fun=go_fast)


    # screen.onkey(key="s", fun=small)
    # screen.onkey(key="l", fun=large)
    # screen.onkey(key="d", fun=default)


   # if restart_flag:
        #     restart()




offpower = {
            "start_time":time.time(),
            "active_length":0,
            "is_active":False,
            "activated":False
                             }







def brake():##### CHEAT / DEBUG #####
    game.field.remove_brick_by_id(game.field.bricks[0].id)
    game.field.remove_dead_bricks()
    screen.update()

def go_fast():##### CHEAT / DEBUG #####
     global wait_time
     wait_time = 0
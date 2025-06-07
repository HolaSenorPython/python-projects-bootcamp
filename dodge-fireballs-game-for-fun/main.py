# I'm making a game on my own, to test my knowledge of Classes and Objects! Angela didn't teach me this.
from turtle import Screen
from player import Player
from scoreboard import Scoreboard
from fireball_manager import FireballManager
import time
# screen stuff
screen = Screen()
screen.setup(width=600,height=600)
screen.colormode(255)
screen.bgcolor("dark turquoise")
screen.register_shape('turtle.gif')
screen.register_shape('turtle_left.gif')
screen.register_shape('fireball.gif')
screen.tracer(0)
# PLAYER/TURTLE GIF IS 86 by 66 PIXELS, code accordingly, FIREBALL GIF is 32 by 53 PIXELS
player = Player()
fball_manager = FireballManager()
score = Scoreboard()

start_time = time.time()

screen.listen()
screen.onkeypress(player.go_left, "Left")
screen.onkeypress(player.go_right, "Right")

game_on = True
last_checked_score = 0
while game_on:
    time.sleep(0.05)
    screen.update()

    # Fireball logistics! spawn in up top, and move downnnn
    fball_manager.make_fireball()
    fball_manager.move_fireball()

    #CHECK FOR FIREBALL OFF-SCREEN
    fball_manager.hide()

    # CHECK IF SECOND HAS PASSED, IF SO INCREASE SCORE
    elapsed_time = time.time() - start_time
    if elapsed_time >= 1:
        score.increase_score()
        start_time = time.time()

    # CHECK IF SCORE IS DIVISIBLE BY 10, IF SO MAKE THE GAME FASTER/HARDER!
    if score.score % 10 == 0 and score.score != last_checked_score:
        last_checked_score = score.score
        if fball_manager.odds > 5:
            fball_manager.odds -= 5
        elif 1 < fball_manager.odds <= 5:
            fball_manager.odds -= 1
        else:
            fball_manager.odds = 1

    # CHECK for GAME OVER!
    for fireball in fball_manager.fireballs:
        if player.distance(fireball) <= 40:
            game_on = False
            score.game_over()






screen.exitonclick()
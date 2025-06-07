from turtle import Screen
import time
from player import Player
from scoreboard import ScoreBoard
from car_manager import CarManager

# SCREEN STUFF
screen = Screen()
screen.title("Turtle Crossing!")
screen.setup(width=600, height=600)
screen.tracer(0)

player = Player()
car_manager = CarManager()
scoreboard = ScoreBoard()

screen.listen()
screen.onkeypress(player.move, "Up")


game_on = True
while game_on:
    time.sleep(0.1)
    screen.update()

    # Get cars to spawn somewhere random and move to left
    car_manager.make_car()
    car_manager.move_cars()

    # Check if off-screen
    car_manager.hide()

    # CHECK FOR LEVEL BEATEN!
    if player.ycor() >= 280:
        player.level_up()
        car_manager.level_up()
        scoreboard.level_up()

    # CHECK FOR GAME OVER!
    for car in car_manager.all_cars:
        if player.distance(car) <= 30:
            game_on = False
            scoreboard.game_over()

screen.exitonclick()

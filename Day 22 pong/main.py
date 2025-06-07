from turtle import Screen
from paddle import Paddle
from user_paddle import UserPaddle
from ball import Ball
from scoreboard import Score
import time
# SCREEN STUFF
screen = Screen()
screen.setup(width=800,height=600)
screen.bgcolor("light gray")
screen.title("Pong")
screen.tracer(0)

paddle = Paddle()
users_paddle = UserPaddle()
ball = Ball()
new_scoreboard = Score()

screen.listen()
screen.onkeypress(users_paddle.up, "Up")
screen.onkeypress(users_paddle.down, "Down")

game_on = True
while game_on:
    sleep_amount = 0.05
    time.sleep(sleep_amount)
    screen.update()

    paddle.move_paddle(ball.ball.ycor())
    ball.move_ball()
    # Ball bounce WALL mechanics
    if ball.ball.ycor() >= 280 or ball.ball.ycor() <= -280:
        ball.bounce_y()

    # Detect collision with com_paddle
    for segment in paddle.FULL_PADDLE:
        if ball.ball.distance(segment) <= 20 and ball.ball.xcor() >= 330:
            ball.bounce_x()

    # Detect collision with user_paddle
    for segment in users_paddle.FULL_PADDLE:
        if ball.ball.distance(segment) <= 20 and ball.ball.xcor() <= -330:
            ball.bounce_x()

    # Detect if com_paddle misses
    if ball.ball.xcor() > 380:
        new_scoreboard.user_point()
        ball.ball.goto(0,0)
        ball.bounce_x()
    # Detect if user paddle misses
    elif ball.ball.xcor() < -380:
        new_scoreboard.com_point()
        ball.ball.goto(0,0)
        ball.bounce_x()















screen.exitonclick()
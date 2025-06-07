import turtle as t

class Ball:
    def __init__(self):
        self.ball = t.Turtle()
        self.ball.penup()
        self.ball.shape("circle")
        self.x_move = 10
        self.y_move = 10

    def move_ball(self):
        new_x = self.ball.xcor() + self.x_move
        new_y = self.ball.ycor() + self.y_move
        self.ball.goto(new_x, new_y)

    def bounce_y(self):
        self.y_move *= -1

    def bounce_x(self):
        self.x_move *= -1


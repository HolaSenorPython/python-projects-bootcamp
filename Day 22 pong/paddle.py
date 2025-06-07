import turtle as t
import random
STARTING_POSITIONS = [(350, 20), (350, 0), (350, -20), (350, -40), (350, -60)]
MOVE_DISTANCE = 20

class Paddle:
    def __init__(self):
        self.FULL_PADDLE = []
        self.make_paddle()
        self.paddle_tip = self.FULL_PADDLE[0]

    def make_paddle(self):
        for position in STARTING_POSITIONS:
            self.add_paddle_piece(position)

    def add_paddle_piece(self, position):
        paddle_piece = t.Turtle()
        paddle_piece.penup()
        paddle_piece.color("red")
        paddle_piece.shape("square")
        paddle_piece.seth(90)
        paddle_piece.setpos(position)
        self.FULL_PADDLE.append(paddle_piece)

    def move_paddle(self, ball_y):
        if random.random() > 0.1:
            if self.FULL_PADDLE[0].ycor() < ball_y and self.FULL_PADDLE[0].ycor() < 280:
                for segment in self.FULL_PADDLE:
                    segment.goto(segment.xcor(), segment.ycor() + 10)
            elif self.FULL_PADDLE[-1].ycor() > ball_y and self.FULL_PADDLE[-1].ycor() > -280:
                for segment in self.FULL_PADDLE:
                    segment.goto(segment.xcor(), segment.ycor() - 10)

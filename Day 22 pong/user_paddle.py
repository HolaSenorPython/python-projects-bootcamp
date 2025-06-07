import turtle as t
from paddle import Paddle
STARTING_POSITIONS2 = [(-350, 20), (-350, 0), (-350, -20), (-350, -40), (-350, -60)]

class UserPaddle(Paddle):
    def __init__(self):
        super().__init__()

    def make_paddle(self):
        for position in STARTING_POSITIONS2:
            self.add_paddle_piece(position)

    def add_paddle_piece(self, position):
        paddle_piece = t.Turtle()
        paddle_piece.penup()
        paddle_piece.color("cyan")
        paddle_piece.shape("square")
        paddle_piece.seth(90)
        paddle_piece.setpos(position)
        self.FULL_PADDLE.append(paddle_piece)

    def up(self):
        if self.FULL_PADDLE[0].ycor() < 280:
            for piece in self.FULL_PADDLE:
                piece.goto(piece.xcor(), piece.ycor() + 10)

    def down(self):
        if self.FULL_PADDLE[-1].ycor() > -280:
            for piece in self.FULL_PADDLE:
                piece.goto(piece.xcor(), piece.ycor() - 10)
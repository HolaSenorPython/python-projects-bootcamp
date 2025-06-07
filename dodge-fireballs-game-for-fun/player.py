from turtle import Turtle

STARTING_POSITION = (0, -250)
# PLAYER IS 86 BY 66 PIXELS!!
class Player(Turtle):
    def __init__(self):
        super().__init__()
        self.shape('turtle.gif')
        self.penup()
        self.goto(STARTING_POSITION)

    def go_left(self):
        if self.xcor() >= -250:
            self.shape('turtle_left.gif')
            self.seth(180)
            self.forward(20)

    def go_right(self):
        if self.xcor() <= 250:
            self.shape('turtle.gif')
            self.seth(0)
            self.forward(20)
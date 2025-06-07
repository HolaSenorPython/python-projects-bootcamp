from turtle import Turtle
STARTING_POSITION = (0, -280)
MOVE_DISTANCE = 10
FINISH_LINE_Y = 280

class Player(Turtle):
    def __init__(self):
        super().__init__()
        self.penup()
        self.shape("turtle")
        self.color("black")
        self.setpos(STARTING_POSITION)
        self.seth(90)

    def move(self):
        if self.ycor() < 280:
            self.forward(MOVE_DISTANCE)

    def level_up(self):
        self.goto(STARTING_POSITION)

from turtle import Turtle
FONT = ("Courier", 24, "bold")
TEXT_X = -200
TEXT_Y = 250
class ScoreBoard(Turtle):

    def __init__(self):
        super().__init__()
        self.level = 1
        self.hideturtle()
        self.penup()
        self.setpos(TEXT_X, TEXT_Y)
        self.write(arg=f"Level: {self.level}",align="center",font=FONT)

    def level_up(self):
        self.clear()
        self.level += 1
        self.hideturtle()
        self.setpos(TEXT_X, TEXT_Y)
        self.write(arg=f"Level: {self.level}", align="center", font=FONT)

    def game_over(self):
        self.penup()
        self.setpos(0, 0)
        self.color("red")
        self.write(arg="Game Over!", align="center", font=FONT)


from turtle import Turtle
FONT = ("Trebuchet", 64, "bold")
SCORE_X = 0
SCORE_Y = 210
class Scoreboard(Turtle):

    def __init__(self):
        super().__init__()
        self.score = 0
        self.penup()
        self.hideturtle()
        self.setpos(SCORE_X, SCORE_Y)
        self.write(arg=f"{self.score}", align="center", font=FONT)

    def increase_score(self):
        self.clear()
        self.score += 1
        self.hideturtle()
        self.setpos(SCORE_X, SCORE_Y)
        self.write(arg=f"{self.score}", align="center", font=FONT)

    def game_over(self):
        self.penup()
        self.setpos(0, 0)
        self.color("crimson")
        self.write(arg="Game Over!", align="center", font=("Trebuchet", 32, "bold"))

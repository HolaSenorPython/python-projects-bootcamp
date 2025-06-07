from turtle import Turtle


class Score(Turtle):

    def __init__(self):
        super().__init__()
        self.color("cyan")
        self.penup()
        self.hideturtle()
        self.setpos(-100, 180)
        self.user_score = 0
        self.com_score = 0
        self.write(arg= self.user_score, align= "center", font=("Courier", 80, "bold"))
        self.goto(100,180)
        self.color("red")
        self.write(arg=self.com_score, align="center", font=("Courier", 80, "bold"))

    def user_point(self):
        self.user_score += 1
        self.clear()
        self.color("cyan")
        self.setpos(-100, 180)
        self.write(arg=self.user_score, align="center", font=("Courier", 80, "bold"))
        self.goto(100, 180)
        self.color("red")
        self.write(arg=self.com_score, align="center", font=("Courier", 80, "bold"))
    def com_point(self):
        self.com_score += 1
        self.clear()
        self.goto(100, 180)
        self.color("red")
        self.write(arg=self.com_score, align="center", font=("Courier", 80, "bold"))
        self.color("cyan")
        self.setpos(-100, 180)
        self.write(arg=self.user_score, align="center", font=("Courier", 80, "bold"))
from turtle import Turtle

class Congrats(Turtle):
    def __init__(self):
        super().__init__()
        self.color("deep pink")
        self.hideturtle()
        self.penup()
        self.goto(0,0)

    def write_text(self, score):
        self.write(arg=f"Congrats! You successfully guessed\n     {score}/50 states in America! :D", align="center", font=("Arial", 28, "bold"))
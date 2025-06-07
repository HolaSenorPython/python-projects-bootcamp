from turtle import Turtle
TEXT_X = -10
TEXT_Y = 260
FONT_TEXT = ("Arial", 24, "bold")
COLOR_TEXT = "purple"

import os

# At the top of the file
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
data_file_path = os.path.join(BASE_PATH, "data.txt")

class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.score = 0
        with open(data_file_path) as score_data:
            self.high_score = int(score_data.read())
        self.penup()
        self.color(COLOR_TEXT)
        self.setpos(TEXT_X, TEXT_Y)
        self.hideturtle()
        self.update_score()

    def update_score(self):
        self.clear()
        with open(data_file_path) as score_data:
            self.high_score = int(score_data.read())
        self.write(arg=f"Score: {self.score} High Score: {self.high_score}", align="center", font=FONT_TEXT)

    def increase(self):
        self.score += 1
        self.update_score()

    def reset(self):
        if self.score > self.high_score:
            with open(data_file_path, mode='w') as score_data:
                score_data.write(str(self.score))
        self.score = 0
        self.update_score()

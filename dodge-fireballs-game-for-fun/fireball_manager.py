from turtle import Turtle
import random
MOVE_DISTANCE = 15
# FIREBALL GIF is 32 by 53 PIXELS
class FireballManager:

    def __init__(self):
        self.fireballs = []
        self.odds = 30
    def make_fireball(self):
        random_n = random.randint(1, self.odds)
        if random_n == 1:
            new_fireball = Turtle('fireball.gif')
            new_fireball.penup()
            random_x = random.randint(-260, 260)
            new_fireball.goto(random_x, 300)
            self.fireballs.append(new_fireball)

    def move_fireball(self):
        for fireball in self.fireballs:
            fireball.seth(270)
            fireball.forward(MOVE_DISTANCE)

    def hide(self):
        for fireball in self.fireballs:
            if fireball.ycor() <= -300:
                fireball.hideturtle()
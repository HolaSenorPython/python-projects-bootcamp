##### THIS WAS DAY 18!!! ####
import turtle as t
import random as r

color_list = [(219, 254, 237), (84, 254, 155), (173, 146, 118),(245, 39, 191), (158, 107, 56), (2, 1, 176),
              (151, 54, 251), (221, 254, 101), (253, 146, 193), (3, 87, 176), (249, 1, 246), (35, 34, 253),
              (1, 213, 212), (249, 0, 0), (254, 147, 146), (253, 71, 70), (39, 249, 42), (85, 249, 253), (240, 1, 13),
              (5, 210, 216), (230, 126, 190), (2, 2, 107), (135, 152, 220), (174, 162, 249), (208, 118, 26), (253, 7, 4),
              (248, 6, 19)]

t.colormode(255)
tom = t.Turtle()
tom.hideturtle()
tom.penup()
tom.speed(0)
tom.setpos(-230,-180)

def dot_maker():
    for color in random_10:
        tom.dot(30, color)
        tom.forward(50)

for n in range(10):
    tom_y = tom.ycor()
    random_10 = r.choices(color_list, k=10)
    dot_maker()
    tom.setx(-230)
    tom.sety(tom_y + 50)




my_screen = t.Screen()
my_screen.exitonclick()
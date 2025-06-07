from turtle import Turtle, Screen
import random

game_on = False
screen = Screen()
screen.setup(500,400)
user_bet = screen.textinput("Make your bet", "Which turtle will win the race? Choose a color.").lower()
colors = ["red", "orange", "yellow", "green", "blue", "purple"]
random_distance = [1,2,3,4,5,6,7,8,9,10]
turtles = []
y = -110

for color in colors:
    new_turtle = Turtle("turtle")
    new_turtle.penup()
    new_turtle.color(color)
    turtles.append(new_turtle)

for turtle in turtles:
    y += 30
    turtle.setpos(-230, y)

if user_bet:
    game_on = True

while game_on:
    for turtle in turtles:
        if turtle.xcor() >= 230:
            if user_bet != turtle.pencolor():
                print(f"You lost! You chose the {user_bet} turtle, and the winner was the {turtle.pencolor()}.")
                game_on = False
            elif user_bet == turtle.pencolor():
                print(f"You won! You chose the {user_bet} turtle, and the winner was the {turtle.pencolor()}!")
                game_on = False
        turtle.forward(random.choice(random_distance))








screen.exitonclick()

import turtle
import pandas
from congrats import Congrats
from playsound import playsound
import pygame
import os

# Set up base path
BASE_PATH = os.path.dirname(os.path.abspath(__file__))

screen = turtle.Screen()
congrats_yay = Congrats()

screen.title("U.S. States Game")

# Use absolute path for the image
image_path = os.path.join(BASE_PATH, "blank_states_img.gif")
screen.addshape(image_path)
turtle.shape(image_path)

score = 0

# Use absolute path for the CSV file
csv_path = os.path.join(BASE_PATH, "50_states.csv")
state_data = pandas.read_csv(csv_path)

answer_state = screen.textinput("Guess the state!", "Name a state.").title()

def write_setup(state_input, x, y):
    new_t = turtle.Turtle()
    new_t.penup()
    new_t.hideturtle()
    new_t.goto(x, y)
    new_t.write(arg=f"{state_input}", align="center", font=("Arial", 8, "normal"))

states = state_data.state.to_list()
states_x = state_data.x.to_list()
states_y = state_data.y.to_list()

correct_guesses = []

# Use absolute path for music file
pygame.mixer.init()
music_path = os.path.join(BASE_PATH, "Cipher.mp3")
pygame.mixer.music.load(music_path)
pygame.mixer.music.play(-1)

game_on = True
while game_on:
    if answer_state == "Exit":
        game_on = False
        missing_states = [state for state in states if state not in correct_guesses]
        missing_s_data = pandas.DataFrame(missing_states)
        # Absolute path for export is optional, but can be done too:
        learn_path = os.path.join(BASE_PATH, "states_to_learn.csv")
        missing_s_data.to_csv(learn_path)
    elif answer_state in states and answer_state not in correct_guesses:
        correct_guesses.append(answer_state)
        write_setup(answer_state, states_x[states.index(answer_state)],
                    states_y[states.index(answer_state)])
        score += 1
        answer_state = screen.textinput(f"{score}/50 correct.", "Nice! Name another state.").title()
    elif answer_state not in states:
        answer_state = screen.textinput(f"{score}/50 correct.", "Sorry, that's not a state. Maybe you had a typo?").title()
    elif answer_state in correct_guesses:
        answer_state = screen.textinput(f"{score}/50 correct.", "You've already guessed that state!").title()

    if score == 50:
        game_on = False
        congrats_yay.write_text(score=score)
        win_sound_path = os.path.join(BASE_PATH, "roblox win sound effect.mp3")
        playsound(win_sound_path)

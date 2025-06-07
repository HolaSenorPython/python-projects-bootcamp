import os
import pandas as pd
import random
from tkinter import *

BACKGROUND_COLOR = "#B1DDC6"
LANG_FONT = ("Arial", 40, "italic")
WORD_FONT = ("Arial", 60, "bold")

# Base directory of the script
BASE_PATH = os.path.dirname(os.path.abspath(__file__))

# Paths to data and image folders
DATA_PATH = os.path.join(BASE_PATH, "data")
IMAGES_PATH = os.path.join(BASE_PATH, "images")

#-----------------FLIP THE CARD!----------------#
def flip_card():
    global eng_translation, card_back, front_card_image, random_card
    eng_translation = cards_dict[cards_dict.index(random_card)]["English"]
    canvas.itemconfig(front_card_image, image=card_back)
    canvas.itemconfig(language_title, text="English", fill="white")
    canvas.itemconfig(word, text=eng_translation, fill="white")

#-----------------MAKING FLASHCARDS-------------#
flashcards = pd.read_csv(os.path.join(DATA_PATH, "french_words.csv"))
flashcards_df = pd.DataFrame(flashcards)
cards_dict = flashcards_df.to_dict(orient="records")
random_card = random.choice(cards_dict)
random_french_wrd = cards_dict[cards_dict.index(random_card)]["French"]
eng_translation = cards_dict[cards_dict.index(random_card)]["English"]

def new_random_word():
    global random_card, random_french_wrd, timer
    window.after_cancel(timer)
    random_card = random.choice(cards_dict)
    random_french_wrd = cards_dict[cards_dict.index(random_card)]["French"]
    canvas.itemconfig(front_card_image, image=card_front)
    canvas.itemconfig(language_title, text="French", fill="black")
    canvas.itemconfig(word, text=random_french_wrd, fill="black")
    timer = window.after(3000, flip_card)

def save_word():
    global random_card
    new_data = pd.DataFrame([random_card])
    try:
        existing_data = pd.read_csv(os.path.join(DATA_PATH, "words_to_learn.csv"))
        updated_data = pd.concat([existing_data, new_data], ignore_index=True)
    except FileNotFoundError:
        updated_data = new_data
    updated_data.to_csv(os.path.join(DATA_PATH, "words_to_learn.csv"), index=False)
    new_random_word()

#-----------------USER INTERFACE-------------------#
window = Tk()
window.title("Flashcard App")
window.minsize(800,600)
window.config(bg=BACKGROUND_COLOR,padx=100,pady=100)

timer = window.after(3000, flip_card)

card_front = PhotoImage(file=os.path.join(IMAGES_PATH, "card_front.png"))
card_back = PhotoImage(file=os.path.join(IMAGES_PATH, "card_back.png"))
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
front_card_image = canvas.create_image(400, 263, image=card_front)
language_title = canvas.create_text(400, 150, font=LANG_FONT, text="French")
word = canvas.create_text(400, 263, font=WORD_FONT, text=random_french_wrd)
canvas.grid(column=0, row=0, columnspan=2)

right_img = PhotoImage(file=os.path.join(IMAGES_PATH, "right.png"))
wrong_img = PhotoImage(file=os.path.join(IMAGES_PATH, "wrong.png"))

right_btn = Button(image=right_img, command=new_random_word, highlightthickness=0, bg=BACKGROUND_COLOR, relief="flat")
right_btn.grid(column=1,row=1)

wrong_btn = Button(image=wrong_img, command=save_word, highlightthickness=0, bg=BACKGROUND_COLOR, relief="flat")
wrong_btn.grid(column=0,row=1)

window.mainloop()

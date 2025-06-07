from tkinter import *
import math
import os
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 1
CHECKS = ""
timer = None
# ---------------------------- TIMER RESET ------------------------------- # 
def reset_timer():
    global reps, CHECKS
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00")
    reps = 1
    CHECKS = ""
    check_marks.config(text=CHECKS)
    title_label.config(text="Timer",fg="green")
# ---------------------------- TIMER MECHANISM ------------------------------- # 
def start_timer():
    global reps
    work_sec = WORK_MIN * 60
    short_b_sec = SHORT_BREAK_MIN * 60
    long_b_sec = LONG_BREAK_MIN * 60
    if reps % 8 == 0:
        title_label.config(text="Long Break", fg=RED, bg=YELLOW)
        count_down(long_b_sec)
    elif reps % 2 != 0:
        title_label.config(text="Work", fg="green", bg=YELLOW)
        count_down(work_sec)
    elif reps % 2 == 0:
        title_label.config(text="Short Break", fg=PINK, bg=YELLOW)
        count_down(short_b_sec)
# ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 
def count_down(count):
    global reps, CHECKS, timer
    count_min = math.floor(count / 60)
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"
    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        timer = window.after(1000, count_down,count - 1)
    else:
        reps += 1
        start_timer()
        if reps % 2 == 0:
            CHECKS += "✔"
            check_marks.config(text=CHECKS)
# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
window.config(padx=100,pady=50,bg=YELLOW)

canvas = Canvas(width=200,height=224,bg=YELLOW,highlightthickness=0)
# Fix path for tomato.png
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
tomato_path = os.path.join(BASE_PATH, "tomato.png")
tomato = PhotoImage(file=tomato_path)

canvas.create_image(100, 112, image=tomato)
timer_text = canvas.create_text(100, 136, font=(FONT_NAME, 32, "bold"), text="00:00", fill="white")
canvas.grid(column=1, row=1)

title_label = Label(text="Timer", bg=YELLOW, fg="green", font=(FONT_NAME, 50, "bold"))
title_label.grid(column=1, row=0)

start_button = Button(text="Start",font=("Arial", 12, "bold"),command=start_timer)
start_button.grid(column=0,row=2)

reset_button = Button(text="Reset",font=("Arial", 12, "bold"),command=reset_timer)
reset_button.grid(column=2,row=2)

check_marks = Label(fg="green",bg=YELLOW,font=("Arial", 20))
check_marks.grid(column=1,row=3)





window.mainloop()
from tkinter import *
screen = Tk()
screen.title("Miles to Kilometers Converter")
screen.minsize(width=400,height=250)

user_miles = Entry()
user_miles.grid(column= 1, row= 0)

miles_label = Label(text="Miles",font=("Comic Sans MS", 16))
miles_label.grid(column= 2, row= 0)

is_equal_to = Label(text="is equal to",font=("Comic Sans MS", 16))
is_equal_to.grid(column= 0, row= 1)

km_label_count = Label(text=f"{0}", font=("Comic Sans MS", 24))
km_label_count.grid(column= 1, row= 1)

km_label = Label(text="Km", font=("Comic Sans MS", 24))
km_label.grid(column= 2, row= 1)

def calculate():
    km_total = float(user_miles.get()) * 1.609
    round_km = round(km_total, 2)
    km_label_count["text"] = f"{round_km}"

calculate_button = Button(text="Calculate!",font=("Comic Sans MS", 16),command=calculate)
calculate_button.grid(column= 1, row= 2)







screen.mainloop()
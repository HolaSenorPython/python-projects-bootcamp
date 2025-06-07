from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json
import os

FONT = ("Helvetica", 12, "bold")

# Get base path of current script
BASE_PATH = os.path.dirname(os.path.abspath(__file__))

DATA_PATH = os.path.join(BASE_PATH, "data.json")
LOGO_PATH = os.path.join(BASE_PATH, "logo.png")

# ---------------------------- SEARCH BUTTON ------------------------------- #
def search_password():
    website = website_entry.get().title()
    try:
        with open(DATA_PATH, "r") as data_file:
            contents = json.load(data_file)
            if website in contents:
                messagebox.showinfo(title=website, message=f"Email: {contents[website]['email']}\n"
                                                          f"Password: {contents[website]['password']}")
            else:
                messagebox.showerror(title="Error", message=f"No details for {website} exists.")
    except FileNotFoundError:
        messagebox.showerror(title="Error", message="No data file found. (Maybe add something first?)")

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
# PASSWORD GENERATOR CODE
def gen_pass():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 
               'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8,10)
    nr_symbols = random.randint(2,4)
    nr_numbers = random.randint(2,4)

    password_letters = [random.choice(letters) for _ in range(nr_letters)]
    password_symbol = [random.choice(symbols) for _ in range(nr_symbols)]
    password_numb = [random.choice(numbers) for _ in range(nr_numbers)]
    pass_list = password_letters + password_symbol + password_numb

    random.shuffle(pass_list)

    password_complete = "".join(pass_list)
    pass_entry.insert(0, password_complete)
    pyperclip.copy(password_complete)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_info():
    website = website_entry.get().title()
    email_or_user = email_user_entry.get()
    passw = pass_entry.get()
    new_data = {
        website: {
            "email": email_or_user,
            "password": passw,
        }
    }
    if len(website) > 0 and len(email_or_user) > 0 and len(passw) > 0:
        if email_user_entry.get() != "myemail@gmail.com":
            try:
                with open(DATA_PATH, mode="r") as data_file:
                    data = json.load(data_file)
            except FileNotFoundError:
                with open(DATA_PATH, mode="w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                data.update(new_data)
                with open(DATA_PATH, mode="w") as data_file:
                    json.dump(data, data_file, indent=4)
            finally:
                website_entry.delete(0, END)
                email_user_entry.delete(0, END)
                email_user_entry.insert(0, "myemail@gmail.com")
                pass_entry.delete(0, END)
        else:
            messagebox.showwarning(title="Placeholder Error", message="You are using the placeholder value for the email/"
                                                                    "username entry!")
    else:
        if len(website) == 0:
            messagebox.showwarning(title="Missing input", message="You are missing a website input!")
        elif len(email_or_user) == 0:
            messagebox.showwarning(title="Missing input", message="You are missing an email or a username input!")
        elif len(passw) == 0:
            messagebox.showwarning(title="Missing input", message="You are missing a password input!")

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)
canvas = Canvas(width=200, height=200)

logo = PhotoImage(file=LOGO_PATH)
canvas.create_image(100, 100, image=logo)
canvas.grid(column=1, row=0)

# Website stuff
website_label = Label(text="Website:", font=FONT)
website_label.grid(column=0, row=1)
website_entry = Entry(width=32)
website_entry.grid(column=1, row=1)
website_entry.focus()

# Search btn
search_btn = Button(text="Search", font=FONT, width=15, command=search_password)
search_btn.grid(column=2, row=1)

# Email Stuff
email_username_label = Label(text="Email/Username:", font=FONT)
email_username_label.grid(column=0, row=2)
email_user_entry = Entry(width=60)
email_user_entry.grid(column=1, row=2, columnspan=2)
email_user_entry.insert(0, "myemail@gmail.com")

# Password stuff
pass_label = Label(text="Password:", font=FONT)
pass_label.grid(column=0, row=3)
pass_entry = Entry(width=32)
pass_entry.grid(column=1, row=3)

# Other
gen_pass_btn = Button(text="Generate Password", font=FONT, command=gen_pass)
gen_pass_btn.grid(column=2, row=3)
add_btn = Button(text="Add", font=FONT, width=36, command=save_info)
add_btn.grid(column=1, row=4, columnspan=2)

window.mainloop()

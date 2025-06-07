import pandas as pd
import os

# Get the full path to the CSV file
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(BASE_PATH, "nato_phonetic_alphabet.csv")

# Load the CSV and create the dictionary
alphabet_df = pd.read_csv(csv_path)
alphabet_dict = {row.letter: row.code for (index, row) in alphabet_df.iterrows()}

print("Welcome to the Python NATO Alphabet converter.")

def generate():
    user_input = input("Enter a word: ").upper()
    try:
        new_word = [alphabet_dict[letter] for letter in user_input]
    except KeyError:
        print("Only letters in the alphabet, s'il vous plait.")
        generate()
    else:
        print(new_word)

generate()

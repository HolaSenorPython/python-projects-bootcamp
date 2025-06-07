import random
from art import logo
numbers = []

for n in range(1, 101):
    numbers.append(n)

computer_number = random.choice(numbers)

def game_mechanics():
    easy_or_hard = input("Choose 'easy' or hard' Don't try any funny business...\n").lower()
    attempts = 0
    if easy_or_hard == "easy":
        attempts += 10
        print(f"You have {attempts} attempts left.")
    elif easy_or_hard == "hard":
        attempts += 5
        print(f"You have {attempts} attempts left.")
    else:
        print("Invalid input :) You're in SUPER hard mode.")
        attempts += 3
        print(f"You have {attempts} attempts left.")

    while True:
        guess = int(input("Guess a number: "))
        if guess == computer_number:
            print(f"CONGRATS! You guessed: {guess}, and the computer was thinking of {computer_number}!")
            break
        elif guess != computer_number:
            if guess > computer_number:
                attempts -= 1
                print("Too high.")
                print(f"You have {attempts} attempts remaining.")
            elif guess < computer_number:
                attempts -= 1
                print("Too low.")
                print(f"You have {attempts} attempts remaining.")

        if attempts == 0:
            print("Game over.")
            print(f"The computer was thinking of: {computer_number}.")
            break

print(logo)
print("Welcome to the number guessing game!")
print("I'm thinking of a number 1-100.")
game_mechanics()
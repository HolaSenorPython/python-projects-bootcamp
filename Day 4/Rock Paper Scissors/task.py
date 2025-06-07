import random
# ascii art
rock = '''
    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)
'''

paper = '''
    _______
---'   ____)____
          ______)
          _______)
         _______)
---.__________)
'''

scissors = '''
    _______
---'   ____)____
          ______)
       __________)
      (____)
---.__(___)
'''

print("Welcome to Rock Paper Scissors vs a computer. I hope you enjoy and have fun!")
user_input = input("What do you choose? Type 0 for Rock, 1 for Paper, and 2 for Scissors!\n")
options_pictures = [rock, paper, scissors]
options = ["Rock", "Paper", "Scissors"]
#beginning setup for code

#if statements and stuff
if user_input == "0":
    print("You chose: Rock")
    print(rock)
    #computer choice
    computer_choice = random.choice(options)
    computer_picture = options_pictures[options.index(computer_choice)]

    print("Computer chose:")
    print(computer_picture)
    print(computer_choice)

    if computer_picture == rock:
        print("It's a draw! Play again?")
    elif computer_picture == paper:
        print("You lost! Play again?")
    elif computer_picture == scissors:
        print("You won! Play again?")
elif user_input == "1":
    print("You chose: Paper")
    print(paper)
# computer choice
    computer_choice = random.choice(options)
    computer_picture = options_pictures[options.index(computer_choice)]
    print("Computer chose:")
    print(computer_picture)
    print(computer_choice)

    if computer_picture == rock:
        print("You won! Play again?")
    elif computer_picture == paper:
        print("It's a draw! Play again?")
    elif computer_picture == scissors:
        print("You lost! Play again?")
elif user_input == "2":
    print("You chose: Scissors!")
    print(scissors)
    #computer choice
    computer_choice = random.choice(options)
    computer_picture = options_pictures[options.index(computer_choice)]
    print("Computer chose:")
    print(computer_picture)
    print(computer_choice)

    if computer_picture == rock:
        print("You lost! Play again?")
    elif computer_picture == scissors:
        print("It's a draw! Play again?")
    elif computer_picture == paper:
        print("You won! Play again?")
else:
    print("Invalid input. Start the game over and enter the right input!")























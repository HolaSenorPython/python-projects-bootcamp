import random
from art import logo


cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]

while True:
    ### THIS IS WHERE THE GAME BEGINS!
    wanna_play = input("Do you want to play a game of ♠️Blackjack?♠️ Type 'y' if yes, or 'n' for no.\n").lower()
    if wanna_play == "y":
        print(logo)
        user_score = 0
        com_score = 0
        user_cards = random.choices(cards, k=2)
        com_cards = random.choices(cards, k=2)
        user_score += sum(user_cards)
        com_score += sum(com_cards)
        print(f"Your cards: {user_cards}, your current score is {user_score}")
        first_card_computer = com_cards[0]
        print(f"The computer's first card is: {first_card_computer}")

    ### THIS IS WHERE IF YOU HAVE BLACKJACK, GAME ENDS
        if com_cards == [11,10] or com_cards == [10,11]:
            print("Computer has Blackjack.")
            print("You lose!🥺")
        elif user_cards == [11,10] or user_cards == [10,11]:
            print("You have Blackjack!")
            print("You win!😁")
    ### THIS IS WHERE IF IT'S GREATER THAN 21 and YOU have an ACE, TRY AND TURN ACE INTO A 1 AND SEE if IT GETS BETTER
        elif user_score > 21:
            for card in user_cards:
                if card == 11:
                    user_score -= 10
                    if user_score <= 21:
                        break
    ### THIS IS WHERE IF THE SCORE IN THE BEGINNING IS LOWER THAN 21, ASK IF THEY WANT TO DRAW AGAIN!!
        elif user_score < 21:
            while True:
                draw_again = input("Would you like to draw another card? Type 'y' or 'n'.\n").lower()
                if draw_again == "y":
                    new_card = random.choice(cards)
                    user_cards.append(new_card)
                    user_score += new_card
                    print(f"Your cards: {user_cards}, your current score is {user_score}")
                    if user_score > 21:
                        print(f"The computer's cards were: {com_cards}")
                        print("You lose!🥺")
                        break
                    elif user_score < 21:
                        print(f"The computer's first card is: {first_card_computer}")
                        continue
    ### THIS IS WHERE IF THEY SAY NO, THE COMPUTER PLAYS!!!
                elif draw_again == "n":
                    while com_score < 17:
                        new_com_card = random.choice(cards)
                        com_cards.append(new_com_card)
                        com_score += new_com_card
    ### THIS IS WHAT HAPPENS AT THE END!!!
                if com_score > 21:
                    print(f"Your final hand: {user_cards}, your final score is {user_score}")
                    print(f"Computer's final hand: {com_cards}, computers final score: {com_score}")
                    print("You win!😏😁")
                    break
                elif com_score < 21:
                    if com_score > user_score:
                        print(f"Your final hand: {user_cards}, your final score is {user_score}")
                        print(f"Computer's final hand: {com_cards}, computers final score: {com_score}")
                        print("You LOSE!😭😂")
                        break
                    elif user_score > com_score and user_score < 21:
                        print(f"Your final hand: {user_cards}, your final score is {user_score}")
                        print(f"Computer's final hand: {com_cards}, computers final score: {com_score}")
                        print("You WIN!🤑🤑")
                        break
                    elif user_score == com_score:
                        print(f"Your final hand: {user_cards}, your final score is {user_score}")
                        print(f"Computer's final hand: {com_cards}, computers final score: {com_score}")
                        print("It's a draw!🤔🤔")
                        break
    elif wanna_play == "n":
        print("Ok. Bye!")
        break
    else:
        print("Invalid input. Go back and try again.")
        break

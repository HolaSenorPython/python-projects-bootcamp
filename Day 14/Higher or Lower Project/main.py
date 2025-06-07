import random
from art import logo, vs
from game_data import data

score = 0

def formatted_data(option):
    option_name = option['name']
    option_description = option['description']
    option_country = option['country']
    return f"{option_name}, a {option_description}, from {option_country}"

option_a = random.choice(data)
print(logo)
while True:
    option_b = random.choice(data)
    print(f"Compare A: {formatted_data(option_a)}")
    print(vs)
    print(f"Compare B: {formatted_data(option_b)}")

    who_is_more_popular = input("Who has more followers? Choose either 'A' or 'B'.\n").lower()

    if who_is_more_popular == "a":
        if option_a['follower_count'] > option_b['follower_count']:
            score += 1
            print(logo)
            print(f"You're right! Current score: {score}")
            option_a = option_b
            continue
        elif option_a['follower_count'] < option_b['follower_count']:
            print(f"Sorry you're wrong. Final score: {score}")
            break
    elif who_is_more_popular == "b":
        if option_b['follower_count'] > option_a['follower_count']:
            score += 1
            print(logo)
            print(f"You're right! Current score: {score}")
            option_a = option_b
            continue
        elif option_b['follower_count'] < option_a['follower_count']:
            print(f"Sorry you're wrong. Final score: {score}")
            break
    else:
        print("Invalid input.")

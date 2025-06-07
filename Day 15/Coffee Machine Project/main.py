MENU = {
    "espresso": {
        "ingredients": {
            "water": 50,
            "coffee": 18,
        },
        "cost": 1.50,
    },
    "latte": {
        "ingredients": {
            "water": 200,
            "milk": 150,
            "coffee": 24,
        },
        "cost": 2.50,
    },
    "cappuccino": {
        "ingredients": {
            "water": 250,
            "milk": 100,
            "coffee": 24,
        },
        "cost": 3.00,
    }
}

resources = {
    "water": 300,
    "milk": 200,
    "coffee": 100,
}

def report():
    water_count = resources["water"]
    milk_count = resources["milk"]
    coffee_count = resources["coffee"]
    keys = resources.keys()
    water = (list(keys)[0]).title()
    milk = (list(keys)[1]).title()
    coffee = (list(keys)[2]).title()
    return f"{water}: {water_count}ml\n{milk}: {milk_count}ml\n{coffee}: {coffee_count}g\nMoney: ${money}"

def money_checker(espresso_cost, latte_cost, cappuccino_cost, drink_choice):
    global MENU, resources, money
    print("Please insert coins.")
    quarter_amount = int(input("How many quarters?: ")) * 0.25
    dime_amount = int(input("How many dimes?: ")) * 0.10
    nickel_amount = int(input("How many nickels?: ")) * 0.05
    penny_amount = int(input("How many pennies?: ")) * 0.01
    final_total = (quarter_amount + dime_amount + nickel_amount + penny_amount)
    if final_total < espresso_cost and drink_choice == "espresso":
        resources["water"] += 50
        resources["coffee"] += 18
        print(f"Sorry that's not enough money. You have ${final_total} and an espresso is ${espresso_cost}.")
    elif final_total == espresso_cost and drink_choice == "espresso":
        money += MENU["espresso"]["cost"]
        print("Here is your espresso☕, enjoy!")
    elif final_total > espresso_cost and drink_choice == "espresso":
        final_total -= espresso_cost
        money += MENU["espresso"]["cost"]
        print(f"Here's your ${round(final_total, 2)} in change.")
        print("Here is your espresso☕, enjoy!")

    if final_total < latte_cost and drink_choice == "latte":
        resources["water"] += 200
        resources["milk"] += 150
        resources["coffee"] += 24
        print(f"Sorry that's not enough money. You have ${final_total} and a latte is ${latte_cost}.")
    elif final_total == latte_cost and drink_choice == "latte":
        money += MENU["latte"]["cost"]
        print("Here is your latte☕, enjoy!")
    elif final_total > latte_cost and drink_choice == "latte":
        final_total -= latte_cost
        money += MENU["latte"]["cost"]
        print(f"Here's your ${round(final_total, 2)} in change.")
        print("Here is your latte☕, enjoy!")

    if final_total < cappuccino_cost and drink_choice == "cappuccino":
        resources["water"] += 250
        resources["milk"] += 100
        resources["coffee"] += 24
        print(f"Sorry that's not enough money. You have ${final_total} and a cappuccino is ${cappuccino_cost}.")
    elif final_total == cappuccino_cost and drink_choice == "cappuccino":
        money += MENU["cappuccino"]["cost"]
        print("Here is your cappuccino☕, enjoy!")
    elif final_total > cappuccino_cost and drink_choice == "cappuccino":
        final_total -= cappuccino_cost
        money += MENU["cappuccino"]["cost"]
        print(f"Here's your ${round(final_total, 2)} in change.")
        print("Here is your cappuccino☕, enjoy!")

money = 0
keys_again = resources.keys()

while True:
    user_input = input("What would you like? (espresso/latte/cappuccino)\n").lower()

    if user_input == "off":
        break

    if user_input == "report":
        print(report())

    if user_input == "espresso":
        if resources["water"] < 50:
            print(f"Sorry, there is not enough {(list(keys_again)[0])}.")
        elif resources["coffee"] < 18:
            print(f"Sorry, there is not enough {(list(keys_again)[2])}.")
        else:
            resources["water"] -= 50
            resources["coffee"] -= 18
            money_checker(MENU["espresso"]["cost"], MENU["latte"]["cost"], MENU["cappuccino"]["cost"], user_input)

    elif user_input == "latte":
        if resources["water"] < 200:
            print(f"Sorry, there is not enough {(list(keys_again)[0])}.")
        elif resources["milk"] < 150:
            print(f"Sorry, there is not enough {(list(keys_again)[1])}.")
        elif resources["coffee"] < 24:
            print(f"Sorry, there is not enough {(list(keys_again)[2])}.")
        else:
            resources["water"] -= 200
            resources["milk"] -= 150
            resources["coffee"] -= 24
            money_checker(MENU["espresso"]["cost"], MENU["latte"]["cost"], MENU["cappuccino"]["cost"], user_input)

    elif user_input == "cappuccino":
        if resources["water"] < 250:
            print(f"Sorry, there is not enough {(list(keys_again)[0])}.")
        elif resources["milk"] < 100:
            print(f"Sorry, there is not enough {(list(keys_again)[1])}.")
        elif resources["coffee"] < 24:
            print(f"Sorry, there is not enough {(list(keys_again)[2])}.")
        else:
            resources["water"] -= 250
            resources["milk"] -= 100
            resources["coffee"] -= 24
            money_checker(MENU["espresso"]["cost"], MENU["latte"]["cost"], MENU["cappuccino"]["cost"], user_input)

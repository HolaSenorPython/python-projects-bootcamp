### THIS WAS DAY 16!!! ###
from menu import Menu, MenuItem
from coffee_maker import CoffeeMaker
from money_machine import MoneyMachine

coffee_maker = CoffeeMaker()
menu = Menu()
money_machine = MoneyMachine()
print("☕☕☕Welcome to the Python coffee machine!☕☕☕")
while True:
    user_input = input(f"What would you like? ({menu.get_items()}):\n").lower()
    if user_input == "off":
        break
    elif user_input == "report":
        coffee_maker.report()
        money_machine.report()
    elif not menu.find_drink(user_input):
        break
    else:
        drink = menu.find_drink(user_input)
        if coffee_maker.is_resource_sufficient(drink) and money_machine.make_payment(drink.cost):
            coffee_maker.make_coffee(drink)

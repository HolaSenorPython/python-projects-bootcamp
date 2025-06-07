from art import logo

def add(n1, n2):
    return n1 + n2

def subtract(n1, n2):
    return n1 - n2

def multiply(n1, n2):
    return n1 * n2

def divide(n1, n2):
    return n1 / n2

operations = {"+": add, "-": subtract, "*": multiply, "/": divide}
#inputs and stuff starts here
print(logo)

answer = None

first_number = float(input("What's the first number?:\n"))
while True:
    arithmetic = input("What is the math operator? Choose '+', '-', '*', or '/'.\n")
    if arithmetic not in operations:
        print("Invalid input. Choose from the options above.")
        continue
    second_number = float(input("What's the second number?:\n"))

    if arithmetic == "+":
        answer = operations["+"](first_number, second_number)
        print(f"{first_number} + {second_number} = {answer}")
    elif arithmetic == "-":
        answer = operations["-"](first_number, second_number)
        print(f"{first_number} - {second_number} = {answer}")
    elif arithmetic == "*":
        answer = operations["*"](first_number, second_number)
        print(f"{first_number} * {second_number} = {answer}")
    elif arithmetic == "/":
        answer = operations["/"](first_number, second_number)
        print(f"{first_number} / {second_number} = {answer}")

    use_again = input(f"Would you like to calculate again with {answer}? Type 'y' for yes, or 'n' to make a new calculation.\n"
                      "You may also type 'STOP' to stop.").lower()
    if use_again == "y":
        first_number = answer
        continue
    elif use_again == "n":
        print("\n" * 40)
        first_number = float(input("What's the first number?:\n"))
        continue
    elif use_again == "stop":
        print("Bye!")
        break

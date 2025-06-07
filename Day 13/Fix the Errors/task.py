try:
    age = int(input("How old are you?"))
except ValueError:
    print("Invalid input. Try inputting a number like '15' instead.")
    age = int(input("How old are you?"))

if age > 18:
    print(f"You can drive at age {age}.")

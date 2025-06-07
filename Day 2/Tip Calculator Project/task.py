print("Welcome to the tip calculator! This should help next time you're out!")
bill = float(input("What was the total of the bill?$"))
tip = int(input("What percentage tip would you like to pay, 12, 15, or 20?"))
people = int(input("How many people are splitting the bill?"))
bill_plus_tip = bill * (tip / 100 + 1)
total = bill_plus_tip / people
rounded_total = round(total,2)
print(f"Each person should pay ${rounded_total}")























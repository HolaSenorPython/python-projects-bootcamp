print(r'''
*******************************************************************************
          |                   |                  |                     |
 _________|________________.=""_;=.______________|_____________________|_______
|                   |  ,-"_,=""     `"=.|                  |
|___________________|__"=._o`"-._        `"=.______________|___________________
          |                `"=._o`"=._      _`"=._                     |
 _________|_____________________:=._o "=._."_.-="'"=.__________________|_______
|                   |    __.--" , ; `"=._o." ,-"""-._ ".   |
|___________________|_._"  ,. .` ` `` ,  `"-._"-._   ". '__|___________________
          |           |o`"=._` , "` `; .". ,  "-._"-._; ;              |
 _________|___________| ;`-.o`"=._; ." ` '`."\ ` . "-._ /_______________|_______
|                   | |o ;    `"-.o`"=._``  '` " ,__.--o;   |
|___________________|_| ;     (#) `-.o `"=.`_.--"_o.-; ;___|___________________
____/______/______/___|o;._    "      `".o|o_.--"    ;o;____/______/______/____
/______/______/______/_"=._o--._        ; | ;        ; ;/______/______/______/_
____/______/______/______/__"=._o--._   ;o|o;     _._;o;____/______/______/____
/______/______/______/______/____"=._o._; | ;_.--"o.--"_/______/______/______/_
____/______/______/______/______/_____"=.o|o_.--""___/______/______/______/____
/______/______/______/______/______/______/______/______/______/______/_____ /
*******************************************************************************
''')
print("Welcome to Treasure Island.")
print("Your mission is to find the treasure.")
print("You enter the island and find yourself at a crossroad. Do you go left or right?")
first_decision = input("Type 'left' or 'right'\n")
# what happens after left or right
if first_decision == "left":
    print("You went left and found yourself at a lake with an island in the middle. Do you swim or wait for a boat?")
    second_decision = input("Type 'swim' or 'wait'\n")
# What happens after second decision (swim or wait)
    if second_decision == "wait":
        print("You wait for a boat, and a kind fisherman passing by gives you a ride to the island safely.")
        print("You must now pick between four doors you see on the only house on the island.")
        third_decision = input("Type 'red', 'yellow','blue', or 'green'\n")
# third decision
        if third_decision == "red":
            print("You enter the red door, and immediately fall in a pit of fire. Game over!")
        elif third_decision == "yellow":
            print("You enter the yellow door and the room is illuminated.\nBeautiful gems of all different colors appear, and you open the chest."
                  "\nWithin it is a poisonous material and you die. Game over!")
        elif third_decision == "green":
            print("You enter the green door and see the beauty of nature and a luxurious treasure chest. Within is all the world's treasures. "
                  "You won, congrats!")
        elif third_decision == "blue":
            print("You open the door and immediately get surrounded by water. It slowly fills up the house and you "
                  "unfortunately drown. Game over!")
        else:
            print(":D Invalid answer again? I know where you live, stay safe!")
    elif second_decision == "swim":
        print("You attempt to swim to the island yourself. However, your impatience got you eaten by a shark. Game over!")
    else:
        print("Stop choosing invalid answers.")
# this stuff is part of first decision, ignore if confused
elif first_decision == "right":
   print("You follow the path on the right and find yourself in a never ending forest."
         "\nThree black bears appear suddenly, and they attack you and you die. Game over.")
else:
    print("Invalid answer. Do the game again lil bro lol")


















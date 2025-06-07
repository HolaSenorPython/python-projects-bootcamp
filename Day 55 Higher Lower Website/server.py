from flask import Flask

app = Flask(__name__) # Make app

import random


@app.route("/")
def home_page():
    return ("<h1>Guess the number between 1 and 10!</h1>"
            "<img src='https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZmwxd3R3czRmZG9naG83bGViYmR1aXJzdmYxeHFmcG1jb3c5NnZ6eCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/cMso9wDwqSy3e/giphy.gif' />")

@app.route("/<int:number>")
def guess(number):
    random_number = random.randint(1, 10)  # Grab the random number
    if number > random_number:
        return ("<h1 color:purple>Too high! Try again! 🤣</h1>"
                "<img src='https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExeGhzbG4yeGdwamhjcXBnZ3NndWtmZXlid2t5Y3RtZGU2N2cwajRjbSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/l2YWy9pD8sZEUMF0s/giphy.gif' />")
    elif number < random_number:
        return ("<h1 color:red>Too low! Try again! 😴</h1>"
                "<img src='https://media.giphy.com/media/UqsBoa3FnNEDYvQbyt/giphy.gif?cid=ecf05e47amive41sc4xdli09j2rwlgyrliz78w88hsv3y9mo&ep=v1_gifs_search&rid=giphy.gif&ct=g' />")
    elif number == random_number:
        return (f"<h1 color:green>You found it! The correct number was {random_number}.</h1>"
                f"<img src='https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExM3czOWQ3d3lpYWNyZ2szZW93MGlob2IwdGJyc3M0ajhhamZjd2tqdSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/1RzW2NT5inH9wFKx0k/giphy.gif' width='300'/>"
                f"<img src='https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZDkxdWVmcmxyNnFwdThqbXhmMGdzYnlhZTg3YnVrZ2NyMjFlOHV5eCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/NqiE7mIiXNAhYVUaZD/giphy.gif' width='300'/>")

@app.route("/secret")
def oh_nah():
    return ("<h1 color:brown text-align:center>What are you doing here? 😏</h1>"
            "<img src='https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcXpzdWhtYzAzMGllMDZyOWoxYXU4amJoYnlqNnQxNmJmaDh6cWx1YyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/fKNTlqx1hvfeE/giphy.gif' width='500'/>")

if __name__ == "__main__":
    # Ensure that this script is only run if I'M the one running it (basically if its being run in this file and not imported elsewhere)
    app.run(debug=True) # Set debug mode active
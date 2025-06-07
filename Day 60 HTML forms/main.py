from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def receive_data():
    if request.method == 'POST':
        name = request.form['username']
        password = request.form['password']
        h1_string = f"<h1>Name: {name} Password: {password}</h1>"
        return h1_string

if __name__ == "__main__":
    app.run(debug=True)
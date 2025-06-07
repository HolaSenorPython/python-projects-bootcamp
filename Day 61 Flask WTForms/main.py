from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from flask_bootstrap import Bootstrap5
import os
from dotenv import load_dotenv

load_dotenv()
'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''
class MyForm(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired(), Email(message='Please enter a valid email address!')])
    password = PasswordField(label='Password', validators=[DataRequired(), Length(min=8, max=20)])
    submit = SubmitField(label='Login')

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_KEY')
bootstrap = Bootstrap5(app)

def right_info_check(form_object):
    # Define correct email and pass
    correct_email = "admin@email.com"
    correct_password = "12345678"
    # Define user email and pass
    user_email = form_object.email.data.lower()
    user_password = form_object.password.data
    # RETURN TRUE OR FALSE DEPENDING ON WHAT WAS INPUTTED
    if user_email == correct_email and user_password == correct_password:
        return True
    else:
        return False

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = MyForm()
    if form.validate_on_submit(): # BASICALLY, IF A POST REQUEST WAS SENT TO THIS URL
        # Do the correct info check function
        result = right_info_check(form_object=form)
        if result:
            return render_template('success.html')
        else:
            return render_template('denied.html')
    return render_template('login.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)

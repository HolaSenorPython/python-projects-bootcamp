from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.simple import URLField
from wtforms.fields import TimeField, SelectField
from wtforms.validators import DataRequired, URL
import csv
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

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_KEY')
bootstrap = Bootstrap5(app=app)


class CafeForm(FlaskForm):
    name = StringField('Cafe name', validators=[DataRequired()])
    url = URLField('Cafe Location on Google Maps (URL)', validators=[DataRequired(),
                                                                     URL(message='Please enter a valid URL.')])
    open = TimeField('Opening Time', validators=[DataRequired()])
    close = TimeField('Closing Time', validators=[DataRequired()])
    coffee_rating = SelectField('Coffee Rating', choices=[
        ('☕', '☕'),
        ('☕☕', '☕☕'),
        ('☕☕☕', '☕☕☕'),
        ('☕☕☕☕', '☕☕☕☕'),
        ('☕☕☕☕☕', '☕☕☕☕☕')], validators=[DataRequired()])
    wifi_rating = SelectField('Wi-Fi Strength Rating', choices=[
        ('❌', '❌'),
        ('🛜', '🛜'),
        ('🛜🛜', '🛜🛜'),
        ('🛜🛜🛜', '🛜🛜🛜'),
        ('🛜🛜🛜🛜', '🛜🛜🛜🛜'),
        ('🛜🛜🛜🛜🛜', '🛜🛜🛜🛜🛜')], validators=[DataRequired()])
    power_rating = SelectField('Power Socket Availability/Plug Availability', choices=[
        ('❌', '❌'),
        ('🔌', '🔌'),
        ('🔌🔌', '🔌🔌'),
        ('🔌🔌🔌', '🔌🔌🔌'),
        ('🔌🔌🔌🔌', '🔌🔌🔌🔌'),
        ('🔌🔌🔌🔌🔌', '🔌🔌🔌🔌🔌')], validators=[DataRequired()])
    submit = SubmitField('Submit')

# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
#e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit(): # IF A POST REQUEST IS MADE, ADD TO THE CSV!
        cafe_name = form.name.data.title()
        cafe_url = form.url.data
        open_time = form.open.data.strftime("%I:%M %p")
        close_time = form.close.data.strftime("%I:%M %p")
        coffee_rank = form.coffee_rating.data
        wifi_rank = form.wifi_rating.data
        plug_rank = form.power_rating.data
        print((cafe_name, cafe_url, open_time, close_time, coffee_rank, wifi_rank, plug_rank)) # Print what was input just to double check
        with open('cafe-data.csv', 'a', encoding='utf-8') as csv_file: # OPEN THE CSV FILE, APPEND TO IT, MAKE SURE NEWLINE IS AT END TO ENSURE THEY DON'T STACK ON EACH OTHER
            csv_file.write(f"{cafe_name},{cafe_url},{open_time},{close_time},{coffee_rank},{wifi_rank},{plug_rank}\n")
    # Exercise:
    # Make the form write a new row into cafe-data.csv
    # with   if form.validate_on_submit()
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, 'cafe-data.csv')

    with open(csv_path, newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = [row for row in csv_data]

    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)

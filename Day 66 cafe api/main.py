from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
import random
import os
from dotenv import load_dotenv

load_dotenv()
'''
Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)

# CREATE DB
class Base(DeclarativeBase):
    pass
# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)

    def make_dict(self):
        dictionary = {}

        for column in self.__table__.columns:
            dictionary[column.name] = getattr(self, column.name)
        return dictionary

with app.app_context():
    db.create_all()


@app.route("/")
def home():
    documentation = "https://documenter.getpostman.com/view/44858011/2sB2jAanRy"
    return render_template("index.html", docs=documentation)


# HTTP GET - Read Record
@app.route('/random')
def get_random_cafe():
    with app.app_context():
        result = db.session.execute(db.select(Cafe).order_by(Cafe.id))
        all_cafes = list(result.scalars())
        random_cafe = random.choice(all_cafes)
    return jsonify(cafe=random_cafe.make_dict())

@app.route('/all')
def get_all_cafes():
    with app.app_context():
        result = db.session.execute(db.select(Cafe).order_by(Cafe.id))
        all_cafes = list(result.scalars())
        cafes_json = []
        for cafe in all_cafes:
            cafe_dict = cafe.make_dict()
            cafes_json.append(cafe_dict)
    return jsonify(cafes=cafes_json)

@app.route('/search')
def search_cafe():
    location = request.args.get("loc")  # looks for an argument in the URL like '?loc='
    if not location: # If it doesnt exist, return this
        return jsonify(error={"Missing parameter": "You must provide a location like ?loc=Paris"}), 400

    selected_cafes = db.session.execute(db.select(Cafe).where(Cafe.location == location))
    list_of_cafes = list(selected_cafes.scalars())
    if list_of_cafes: # so if there IS a GIVEN LOCATION, and it MATCHES cafes in our table, do this
        cafes_json = [cafe.make_dict() for cafe in list_of_cafes]

        response = {f"Cafes in {location}": cafes_json} # MAKE DICTIONARY WITH LOCATION AS KEY NAME, AND VALUE AS OUR LIST OF CAFE DICTS
        return jsonify(response) # jsonify the WHOLE SHABANG
    else: # ELSE, return this (the given location doesn't match any cafes in our table)
        return jsonify(error={"Not found": f"Sorry, we don't have a cafe in {location}."})
# HTTP POST - Create Record
@app.route('/add', methods=['POST'])
def add_cafe():
    new_cafe = Cafe(
        name=request.form.get("name"),
        map_url=request.form.get("map_url"),
        img_url=request.form.get("img_url"),
        location=request.form.get("location"),
        seats=request.form.get("seats"),
        has_toilet=bool(request.form.get("has_toilet")),
        has_wifi=bool(request.form.get("has_wifi")),
        has_sockets=bool(request.form.get("has_sockets")),
        can_take_calls=bool(request.form.get("can_take_calls")),
        coffee_price=request.form.get("coffee_price"),
    )
    db.session.add(new_cafe)
    db.session.commit()
    if new_cafe:
        return jsonify({"response": {"success": "Successfully added the new cafe."}})
# HTTP PUT/PATCH - Update Record
@app.route('/update-cafe/<int:cafe_id>', methods=['PATCH'])
def update_cafe(cafe_id):
    new_price = request.args.get("new_price")
    cafe = Cafe.query.get(cafe_id)
    if not cafe:
        return jsonify({"error": {"Not Found": "The ID inputted doesn't match a cafe in our database."}}), 404
    else:
        cafe.coffee_price = new_price
        db.session.commit()
        return jsonify({"success": "Successfully updated the price."}), 200
# HTTP DELETE - Delete Record
@app.route('/report-closed/<int:cafe_id>', methods=['DELETE'])
def delete_cafe(cafe_id):
    api_key = request.args.get("api_key")
    if api_key != os.environ.get('API_KEY'):
        return jsonify({"error": "Sorry, that's not allowed. Make sure you have the correct API key!"}), 401
    cafe = Cafe.query.get(cafe_id)
    if not cafe:
        return jsonify({"error": {"Not Found": "The ID inputted doesn't match a cafe in our database."}}), 404
    else:
        db.session.delete(cafe)
        db.session.commit()
        return jsonify({"success": "The cafe selected was successfully deleted from the database."})

if __name__ == '__main__':
    app.run(debug=True)

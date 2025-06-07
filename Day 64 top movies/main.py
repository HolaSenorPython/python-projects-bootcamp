from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float, asc
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
import requests
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

# FUNCTION FOR FINDING MOVIES THROUGH THE API
def search_movies(title):
    print("Accessing movies API...")
    url = "https://api.themoviedb.org/3/search/movie"
    api_key = os.environ.get('API_KEY')
    parameters = {
        "api_key": api_key,
        "query": {title},
        "include-adult": True,
        "language": "en-US",
        "page": 1,
    }
    response = requests.get(url=url, params=parameters)
    response.raise_for_status()
    print("Accessed successfully! Things should be showing shortly...")
    data = response.json()
    movies_list = []
    for movie_dict in data['results']:
        title = movie_dict['title']
        release = movie_dict['release_date']
        movie_id = movie_dict['id']
        movie_tuple = (movie_id, release, title)
        movies_list.append(movie_tuple)
    return movies_list

# Make the movie form for UPDATING movies
class UpdateForm(FlaskForm):
    new_rating = StringField('Your rating 1-10 as a DECIMAL. (e.g. 7.5)', validators=[DataRequired()])
    new_review = StringField('Your review', validators=[DataRequired(), Length(min=20)])
    submit = SubmitField('Done')
# Make movie form for ADDING movies
class AddMovieForm(FlaskForm):
    movie_name = StringField('Movie Title', validators=[DataRequired()])
    submit_movie = SubmitField('Add Movie')

# Define the db class
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
# add conifgs to our app
app.config['SECRET_KEY'] = os.environ.get('FLASK_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies-collection.db'
Bootstrap5(app)
# Initialize app db with these configs (I think?)
db.init_app(app=app)

# CREATE DB
class Movies(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String, nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=True)
    ranking: Mapped[int] = mapped_column(Integer, nullable=True)
    review: Mapped[str] = mapped_column(String(250), nullable=True)


# CREATE TABLE
with app.app_context():
    db.create_all()

@app.route("/")
def home():
    movie_deleted = request.args.get('movie_deleted') == 'true'
    with app.app_context():
        result = db.session.execute(db.select(Movies).order_by(asc(Movies.rating)))
        all_movies = list(result.scalars())

    for i in range(len(all_movies)):
        all_movies[i].ranking = len(all_movies) - i

    return render_template("index.html", movies=all_movies, movie_deleted=movie_deleted)

@app.route("/edit/<int:movie_id>", methods=['GET', 'POST'])
def edit_movie(movie_id):
    form = UpdateForm()
    requested_movie = None
    movie_updated = False
    if form.validate_on_submit(): # IF TEH FORM IS SUBMITTED / POST REQUEST MADE
        rating = float(form.new_rating.data)
        review = form.new_review.data.title()
        with app.app_context():
            movie_to_update = db.session.execute(db.select(Movies).where(Movies.id == movie_id)).scalar()
            movie_to_update.rating = rating
            movie_to_update.review = review
            db.session.commit()
            movie_updated = True

    with app.app_context():
        result = db.session.execute(db.select(Movies).order_by(asc(Movies.rating)))
        all_movies = list(result.scalars())
        for movie in all_movies:
            if movie.id == movie_id:
                requested_movie = movie
    return render_template('edit.html', movie=requested_movie, movie_updated=movie_updated, form=form)

@app.route("/delete/<int:movie_id>")
def delete_movie(movie_id):
    with app.app_context():
        movie_to_del = db.session.execute(db.select(Movies).where(Movies.id == movie_id)).scalar()
        if movie_to_del:
            db.session.delete(movie_to_del)
            db.session.commit()
    return redirect(url_for('home', movie_deleted='true'))

@app.route('/add', methods=['GET', 'POST'])
def add_movie():
    form = AddMovieForm()
    if form.validate_on_submit(): # If a POST request is made...
        movie_title = form.movie_name.data.title()
        movies = search_movies(movie_title) # FIND THE MOVIE USING THIS FUNCTION
        return render_template('select.html', movies=movies)

    return render_template('add.html', form=form)

@app.route("/find/<int:api_movie_id>")
def find_and_add_movie(api_movie_id):
    url = f"https://api.themoviedb.org/3/movie/{api_movie_id}"
    api_key = os.environ.get('API_KEY')
    parameters = {
        "api_key": api_key,
        "language": "en-US"
    }
    response = requests.get(url=url, params=parameters)
    data = response.json()
    movie_title = data['original_title']
    movie_overview = data['overview']
    img_url = f"https://image.tmdb.org/t/p/w342{data['poster_path']}"
    year = data['release_date'].split("-")[0]
    new_movie = Movies(
        title=movie_title,
        year=year,
        description=movie_overview,
        img_url=img_url,
    )
    with app.app_context():
        db.session.add(new_movie)
        db.session.commit()
    # REQUERY the NEW movie JUST made/added so that it doesn't go stale/detached
    new_movie = db.session.execute(db.select(Movies).where(Movies.title == movie_title)).scalar()
    return redirect(url_for('edit_movie', movie_id=new_movie.id))


if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float, text
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

# Make a database
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
# Make app
app = Flask(__name__)
# configure SQLite database, this is relative to our app instance folder (main.py?)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///new-books-collection.db"
# Initialise our app with this configuration
db.init_app(app=app)

# Define the table, and set up its content
class Book(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)

# Create table
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    book_deleted = request.args.get('book_deleted') == 'true'
    with app.app_context():
        result = db.session.execute(db.select(Book).order_by(Book.id))
        all_books = list(result.scalars())
    return render_template('index.html', books=all_books, book_deleted=book_deleted)

@app.route("/add", methods=['GET', 'POST'])
def add():
    book_added = False
    if request.method == 'POST':
        book_name = request.form['bookname']
        author = request.form['author']
        rating = request.form['rating']
        with app.app_context():
            new_book = Book(title=book_name.title(), author=author.title(), rating=float(rating))
            db.session.add(new_book)
            db.session.commit()
        book_added = True
    return render_template('add.html', book_added=book_added)

@app.route('/edit/<int:book_id>', methods=['GET', 'POST'])
def edit_rating(book_id):
    requested_book = None
    book_updated = False
    if request.method == 'POST':
        new_rating = float(request.form['rating'])
        book_to_update = db.session.execute(db.select(Book).where(Book.id == book_id)).scalar()
        book_to_update.rating = new_rating
        db.session.commit()
        book_updated = True

    with app.app_context():
        result = db.session.execute(db.select(Book).order_by(Book.id))
        all_books = list(result.scalars())
        for book in all_books:
            if book.id == book_id:
                requested_book = book
    return render_template('edit.html', book_updated=book_updated, book=requested_book)

@app.route('/delete/<int:book_id>')
def delete_book(book_id):
    with app.app_context():
        book_to_delete = db.session.execute(db.select(Book).where(Book.id == book_id)).scalar()
        if book_to_delete:
            db.session.delete(book_to_delete)
            db.session.commit()

    return redirect(url_for('home', book_deleted='true'))

@app.route('/reset')
def reset_db():
    secret = request.args.get('secret')
    if secret != os.environ.get('SECRET'): # This is the secret parameter to insert into the url
        return "Unauthorized", 403

    # Deletes all table data
    with app.app_context():
        db.session.execute(text("DELETE FROM book;"))
        try:
            db.session.execute(text("DELETE FROM sqlite_sequence WHERE name='book';"))
        except Exception as e:
            print("No sqlite_sequence table found, skipping:", e)
            db.session.commit()

        # Use VACUUM to reset the auto-increment counter
        db.session.execute(text("VACUUM;"))  # Rebuild the database and reset autoincrement
        db.session.commit()
    return "Database reset successfully! 😳"

if __name__ == "__main__":
    app.run(debug=True)


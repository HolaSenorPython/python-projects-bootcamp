from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
import datetime as dt
from datetime import date
import os
from dotenv import load_dotenv

load_dotenv()

'''
Make sure the required packages are installed: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from the requirements.txt for this project.
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_KEY')
Bootstrap5(app)

# CREATE CKEDITOR
app.config['CKEDITOR_PKG_TYPE'] = 'standard' # choose editor type
ckeditor = CKEditor(app=app) # initialize the ckeditor

# CREATE DATABASE
class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# CONFIGURE TABLE
class BlogPost(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)


with app.app_context():
    db.create_all()

# Create the WTFORM for ADDING POSTS
class PostForm(FlaskForm):
    title = StringField('Blog Post Title', validators=[DataRequired()])
    subtitle = StringField('Subtitle', validators=[DataRequired()])
    the_users_name = StringField('Your Name', validators=[DataRequired()])
    img_url = StringField('Blog Image Url', validators=[DataRequired(), URL()])
    body = CKEditorField('Blog Content', validators=[DataRequired()])
    submit = SubmitField('Submit Post')

@app.route('/')
def get_all_posts():
    # TODO: Query the database for all the posts. Convert the data to a python list.
    with app.app_context():
        result = db.session.execute(db.select(BlogPost).order_by(BlogPost.id))
        posts = list(result.scalars())
    return render_template("index.html", all_posts=posts)

# TODO: Add a route so that you can click on individual posts.
@app.route('/post/<int:post_id>')
def show_post(post_id):
    requested_post = None
    # TODO: Retrieve a BlogPost from the database based on the post_id
    with app.app_context():
        result = db.session.execute(db.select(BlogPost).order_by(BlogPost.id))
        all_posts = list(result.scalars())
        for post in all_posts:
            if post.id == post_id:
                requested_post = post
    return render_template("post.html", post=requested_post)

def get_date():
    date_raw = dt.datetime.now()
    date_semi_formatted = date(date_raw.year, date_raw.month, date_raw.day) # turn date into this format: XXXX-XX-XX
    final_date = date_semi_formatted.strftime('%B %d, %Y')
    return final_date

# TODO: add_new_post() to create a new blog post
@app.route('/new-post', methods=['GET', 'POST'])
def add_new_post():
    post_added = False
    form = PostForm()
    if form.validate_on_submit(): # If a post request is made:
        today_date = get_date() # use the function to get today's date
        new_post = BlogPost(
            title=request.form.get('title'),
            subtitle=request.form.get('subtitle'),
            author=request.form.get('the_users_name'),
            img_url=request.form.get('img_url'),
            body=request.form.get('body'),
            date=today_date,
        )
        db.session.add(new_post)
        db.session.commit()
        post_added = True

    return render_template('make-post.html', form=form, post_added=post_added)
# TODO: edit_post() to change an existing blog post
@app.route('/edit-post/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    wants_edit = True
    requested_post = None
    # Get the necessary post
    with app.app_context():
        result = db.session.execute(db.select(BlogPost).order_by(BlogPost.id))
        all_posts = list(result.scalars())
        for post in all_posts:
            if post.id == post_id:
                requested_post = post
    edit_form = PostForm(
        title=requested_post.title,
        subtitle=requested_post.subtitle,
        the_users_name=requested_post.author,
        img_url=requested_post.img_url,
        body=requested_post.body,
        date=requested_post.date,
    )
    # If they are done editing the form of their choice
    if edit_form.validate_on_submit():
        with app.app_context(): # Update the database
            post_to_update = db.session.get(BlogPost, post_id)
            post_to_update.title = request.form.get('title')
            post_to_update.subtitle = request.form.get('subtitle')
            post_to_update.author = request.form.get('the_users_name')
            post_to_update.img_url = request.form.get('img_url')
            post_to_update.body = request.form.get('body')
            db.session.commit()

        return redirect(url_for('show_post', post_id=post_id)) # Redirect them to their post!

    return render_template('make-post.html', post=requested_post, wants_edit=wants_edit, form=edit_form)

# TODO: delete_post() to remove a blog post from the database
@app.route('/delete-post/<int:post_id>')
def delete_post(post_id):
    requested_post = None
    # Get the necessary post
    with app.app_context():
        result = db.session.execute(db.select(BlogPost).order_by(BlogPost.id))
        all_posts = list(result.scalars())
        for post in all_posts:
            if post.id == post_id:
                requested_post = post
    # Delete the post
    db.session.delete(requested_post)
    db.session.commit()
    return redirect(url_for('get_all_posts', posts=all_posts))
# Below is the code from previous lessons. No changes needed.
@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True, port=5003)

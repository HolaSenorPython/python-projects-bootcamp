from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
from sqlalchemy.exc import NoResultFound, MultipleResultsFound
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_KEY')


# CREATE LOGIN MANAGER
login_manager = LoginManager()
login_manager.init_app(app=app)

# CREATE DATABASE
class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# CREATE DATA FOR TABLE AND WHAT A USER LOOKS LIKE
class User(db.Model, UserMixin):
    __allow_unmapped__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(120))
    name: Mapped[str] = mapped_column(String(100))

    def __init__(self, email: str, password: str, name: str):
        self.email = email
        self.password = password
        self.name = name

with app.app_context():
    db.create_all()

# USER LOADER CALLBACK
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, user_id)

@app.route('/')
def home():
    return render_template("index.html", logged_in=current_user.is_authenticated)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')

        result = db.session.execute(db.select(User).where(User.email == email))
        user = result.scalar()

        if user:
            flash(f"You've already signed up with that email! ({email}) 🤦‍♂️ Try logging in instead.")
            return redirect(url_for('login'))

        hashy_salty_password = generate_password_hash(request.form.get('password'), method='pbkdf2:sha256', salt_length=8)
        new_user = User(
            email=request.form.get('email'),
            name=request.form.get('name'),
            password=hashy_salty_password, # HASH THE PASSWORD FOR SECURITY!
        )

        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        return redirect(url_for('secrets'))

    return render_template("register.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            requested_user = db.session.execute(
                db.select(User).where(User.email == email)
            ).scalar_one()
        except NoResultFound:
            flash(f"The email {email} doesn't exist in our database. Maybe register it? 😳")
            return redirect(url_for('login'))
        except MultipleResultsFound:
            flash("Something went wrong! — multiple accounts with the same email exist. Contact support. 🤔")
            return redirect(url_for('login'))

        password_check = check_password_hash(requested_user.password, password)
        # Now it's safe to check password
        if password_check:
            login_user(requested_user)
            flash("Successfully logged in!")
            return redirect(url_for('secrets'))
        else:
            flash("Wrong password! 🤣")
            return redirect(url_for('login'))
    else:
        return render_template("login.html")


@app.route('/secrets')
@login_required
def secrets():
    print(current_user.name)

    return render_template("secrets.html", name=current_user.name)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/download/<string:name>')
@login_required
def download(name):
    upload_folder = os.path.join(app.root_path, 'static', 'files')
    return send_from_directory(directory=upload_folder, path=name, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)

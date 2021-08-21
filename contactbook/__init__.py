from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

"""
	initializing flask app
"""
app = Flask(__name__)
app.config['SECRET_KEY'] = 'my secret'


"""
	specific the data case path
"""
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contack_book.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


"""
	contecting db with app
"""
db = SQLAlchemy(app)


"""
	importing route and models
"""
from . import routes
from .models import Contact_Book, User


"""
	initializing and creating the modeds
"""
if not path.exists('contactbook/' + 'contack_book.db'):
    db.create_all()
    db.session.commit()
    print("Database Created")


"""
	Login manager for user session
"""

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

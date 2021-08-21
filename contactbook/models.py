from contactbook import db
from flask_login import UserMixin

"""
    Contact_Book schema is the blueprint of contacts in the database
"""
class Contact_Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=False)
    phone_number = db.Column(db.String(20), nullable=True, unique=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    """ 
        __table_args is used to make the email and user_id as unique key
        to differentiate data between user and serve them separately
    """
    __table_args__ = (
        db.UniqueConstraint('email', 'user_id'),
    )

"""
    User schema is the blueprint of User in the database
"""
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    firstname = db.Column(db.String(80), nullable=False)
    contact_book = db.relationship('Contact_Book')

    def __repr__(self):
        return f"User('{self.email},{self.password},{self.firstname}')"

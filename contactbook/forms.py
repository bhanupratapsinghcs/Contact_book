from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Email, Length

"""
	form validation module for checking the contact validity
"""


class FormValidation(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=-1, max=80, message='You cannot have more than 80 characters in name')])
    email = StringField('E-Mail', validators=[Email(), Length(min=-1, max=100, message='You cannot have more than 100 characters in email')])
    phone_number = StringField('Phone', validators=[Length(min=-1, max=20, message='You cannot have more than 20 characters phone_number')])

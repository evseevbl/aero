from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class Registration(FlaskForm):
    name = StringField('Name')
    surname = StringField('Surname')
    passport = StringField('Passport')
    search = SubmitField('search')

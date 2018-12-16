from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField


class Registration(FlaskForm):
    name = StringField('Name')
    surname = StringField('Surname')
    passport = StringField('Passport')
    flight = SelectField('Flight', choices=[])
    search = SubmitField('search')

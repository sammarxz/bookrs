from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.fields.html5 import EmailField
from wtforms.validators import (DataRequired, Regexp, ValidationError,
                                Length, EqualTo)


from app import db
import models


def name_exists(form, field):
    if db.session.query(db.exists().where(models.User.username == field.data)).scalar():
        raise ValidationError('User with that username already exists.')


def email_exists(form, field):
    if db.session.query(db.exists().where(models.User.email == field.data)).scalar():
        raise ValidationError('User with that email already exists.')


class RegistrationForm(FlaskForm):
    name = StringField(
        'Name', 
        validators=[
            DataRequired(),
            Length(max=50),
        ])
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Regexp(
                r'^[a-zA-Z0-9_]+$',
                message=("Username should be one word, letters,"
                         "numbers and underscores only.")
            ),
            name_exists
        ])
    email = EmailField(
        'Email',
        validators=[
            DataRequired(),
            email_exists
        ])
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=6),
            EqualTo('password2', message='Password must match')
        ])
    password2 = PasswordField('Confirm Password', validators=[DataRequired()])


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class ProfileForm(FlaskForm):
    name = StringField('Name')
    current_password = PasswordField(
        'Current Password',
        validators=[DataRequired()]
    )
    new_password = PasswordField(
        'New Password',
        validators=[EqualTo('new_password2', message='Password mus match')]
    )
    new_password2 = PasswordField('Confirm new Password')


class BookForm(FlaskForm):
    title = StringField('Book Title', validators=[DataRequired()])
    status = SelectField(
        'Status',
        choices=[
            ('read', 'Read'),
            ('reading', 'Currently Reading'),
            ('to-read', 'Want to Read')
        ],
        validators=[DataRequired()]
    )

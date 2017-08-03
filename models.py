import datetime

from app import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    username = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(200))
    books = db.relationship('Book', backref='users', lazy='dynamic')

    def __init__(self, name, username, email, password):
        self.name = name
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username


class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    status = db.Column(db.String(30))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User')

    def __init__(self, title, status, user_id):
        self.title = title
        self.status = status
        self.user_id = user_id

    def __repr__(self):
        return '<Book %r>' % self.title

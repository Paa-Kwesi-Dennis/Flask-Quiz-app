from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    questions = db.relationship('Question', backref='admin')


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(400))
    answer = db.Column(db.String(150))
    author = db.Column(db.Integer, db.ForeignKey('admin.id'))
    # options = db.Column(db.String(400))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now()) 


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    score = db.Column(db.Integer)


    
     
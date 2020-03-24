from datetime import datetime
from app import db
from flask_login import UserMixin
'''from werkzeug.security import generate_password_hash, check_password_hash'''
'''from flask_bcrypt import generate_password_hash, check_password_hash'''


class User(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), index=True, unique=True)
    email = db.Column(db.String(50), index=True, unique=True)
    password = db.Column(db.String(50))

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Questions(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer)
    question = db.Column(db.String(300))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Question {}>'.format(self.question)


class Question(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('user.id'))
    question = db.Column(db.String(300))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Question {}>'.format(self.question)


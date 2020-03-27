'''For setting up the various models required for the project'''

from datetime import datetime
from app import db

class User(db.Model):
    '''Model for the user'''
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), index=True, unique=True)
    email = db.Column(db.String(50), index=True, unique=True)
    password = db.Column(db.String(50))

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Questions(db.Model):
    '''Model for the questions'''

    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer)
    question = db.Column(db.String(300))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Question {}>'.format(self.question)

'''For setting up the various models required for the project'''

from datetime import datetime
from app import db, login
from flask_login import UserMixin
from app.search import add_to_index, remove_from_index, query_index


class SearchableMixin(object):
    @classmethod
    def search(cls, expression, page):
        ids, total = query_index(cls.__tablename__, expression, page, cls.__searchable__)
        if total == 0:
            return cls.query.filter_by(id=0), 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return cls.query.filter(cls.id.in_(ids)), total

    @classmethod
    def before_commit(cls, session):
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }

    @classmethod
    def after_commit(cls, session):
        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['delete']:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)


db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    '''Model for the user'''
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), index=True, unique=True)
    email = db.Column(db.String(50), index=True, unique=True)
    password = db.Column(db.String(50))

    def __repr__(self):
        return '<User --> ID ->{} USERNAME ->{}>'.format(self.id, self.username)       


class Questions(SearchableMixin, db.Model):
    '''Model for the questions'''

    __searchable__ = ['question']

    id = db.Column(db.Integer, primary_key = True)
    userid = db.Column(db.Integer, db.ForeignKey('user.id'))
    question = db.Column(db.String(300))
    timestamp = db.Column(db.DateTime, index = True, default = datetime.utcnow)

    def __repr__(self):
        return '<Question --> ID ->{} QUESTION->{} USERID->{}>'.format(self.id, self.question , self.userid)
     

class Answers(db.Model):
    '''Model for the answers'''

    id = db.Column(db.Integer, primary_key = True)
    userid = db.Column(db.Integer, db.ForeignKey('user.id'))
    quesid = db.Column(db.Integer, db.ForeignKey('questions.id'))
    answer_of_ques = db.Column(db.String(500))
    timestamp = db.Column(db.DateTime, index = True, default = datetime.utcnow)

    def __repr__(self):
        return '<Answer --> ID->{} ANSWER->{} USERID->{} QUESTIONID->{}>'.format(self.id, self.answer_of_ques, self.userid, self.quesid)


'''For various forms'''

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length, Email, ValidationError, EqualTo
from flask_wtf.file import FileField, FileAllowed
from app.models import User, Questions
from flask_login import current_user
from app.models import User
from flask_babel import _, lazy_gettext as _l
from flask import request


class RegistrationForm(FlaskForm):
    '''Registration form for a user'''

    username = StringField('Username', validators = [DataRequired()])
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_username_email(self, email):
        user_username = User.query.filter_by(username=username.data).first()
        user_email = User.query.filter_by(email=email.data).first()
        if user_username:
            raise ValidationError('That username is taken please take another one')
        if user_email:
            raise ValidationError('That email is taken please take another one')


class LoginForm(FlaskForm):
    '''Login form for a user'''

    username = StringField('Username', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired()])
    submit = SubmitField('Login')


class UpdateUserForm(FlaskForm):
    '''Update form for a user'''

    username = StringField('New Username', validators = [DataRequired()])
    email = StringField('New Email', validators = [DataRequired(), Email()])
    submit = SubmitField('Update Details')    

    def validate_username_email(self, email):
        user_username = User.query.filter_by(username=username.data).first()
        user_email = User.query.filter_by(email=email.data).first()
        if user_username:
            raise ValidationError('That username is taken please take another one')
        if user_email:
            raise ValidationError('That email is taken please take another one')


class QuestionForm(FlaskForm):
    '''Form for adding and updating question'''

    question = TextAreaField('Question', validators=[DataRequired()])
    submit = SubmitField('Submit')


class AnswerForm(FlaskForm):
    '''Form for adding and updating answer'''

    answer = TextAreaField('Answer', validators=[DataRequired()])
    submit = SubmitField('Submit')


class SearchForm(FlaskForm):
    '''Form for search'''

    q = StringField(_l('Search'), validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(SearchForm, self).__init__(*args, **kwargs)

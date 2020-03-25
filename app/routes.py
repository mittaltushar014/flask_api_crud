from flask import render_template, flash, redirect, url_for, request, Flask, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db
from app.models import User, Questions
from app.config import Config
from functools import wraps
import jwt


def token_verify(function):
    """ This function is used to verify token and act as step of authorization"""

    @wraps(function)
    def decorated(*args, **kwargs):
        token = None
        if 'token' in request.headers:
            token = request.headers['token']
            print(token)

        if not token:
            return jsonify({'message': 'Missing Token!', "status": "401"})

        try:
            token_verify = jwt.decode(token, Config.SECRET_KEY)
            active_user= User.query.filter_by(id=token_verify['user_id']).first()
            active_user_id=active_user.id
        except:
            return jsonify({'message': 'Invalid token!', "status": "404"})

        return function(active_user_id, *args, **kwargs)

    return decorated



@app.route('/login')
def login():
    """For checking authorization and creating token for further use"""
    
    credentials = request.authorization

    if not credentials or not credentials.username or not credentials.password:
        return make_response('Verification not done', 401)

    user = User.query.filter_by(username=credentials.username).first()

    if not user:
        return make_response('No such user', 401)

    if check_password_hash(user.password, credentials.password):
        hashed_token = jwt.encode(
            {'user_id': user.id},
            Config.SECRET_KEY)

        return jsonify({'hashed_token': hashed_token.decode('UTF-8')})


@app.route('/signup', methods=['POST'])
def signup():
    '''For adding user to User table'''

    if request.method == "POST":
        request_JSON = request.json
        print(request_JSON)
        username_sent = request_JSON['username']
        email_sent = request_JSON['email']
        password_sent = generate_password_hash(request_JSON['password'], method='sha256')
        newuser= User(username=username_sent, email=email_sent, password=password_sent)
        db.session.add(newuser)
        db.session.commit()

        return jsonify({"response":"User " + username_sent + " added successfully!"})


@app.route('/users', methods=['GET'])
def users():
    '''For displaying all users'''

    if request.method == "GET":
        users_data = User.query.all()
        print(users_data)
        list_data=[]
        for user in users_data:
            user_data1={"id":user.id, "username":user.username, "email": user.email}
            list_data.append(user_data1)
        return jsonify({"response:" : list_data})


@app.route('/users/<int:user_id>',methods=['GET'])
@token_verify
def user(active_user_id ,user_id):
    '''For displaying a particular user'''

    if request.method == "GET":
        user = User.query.filter_by(id = active_user_id).first()

    a_user = {'id': user.id, 'username': user.username, 'email': user.email}
    
    return jsonify({'user': a_user})        


@app.route('/users/<int:user_id>', methods=['PUT'])
@token_verify
def update_user(active_user_id, user_id):
    '''For updating a user details'''

    if request.method == "PUT":

        user = User.query.filter_by(id = active_user_id).first()
        new_details = request.json

        if not user:
            return jsonify({'message': 'No user found!', "status": "404"})


        user.username = new_details["username"]
        user.email = new_details["email"]

        db.session.commit()

        return jsonify({'message': 'The user has been updated!'})


@app.route('/users/<int:user_id>', methods=['DELETE'])
@token_verify
def delete_user(active_user_id ,user_id):
    '''For deleting a user'''

    if request.method == "DELETE":
        user = User.query.filter_by(id=active_user_id).first()

        if not user:
            return jsonify({'message': 'User not found', "status": "404"})

        db.session.delete(user)
        db.session.commit()

        return jsonify({'message': 'The user id deleted!', "status": "200"})


@app.route('/users/<int:user_id>/question_new', methods=['POST'])
@token_verify
def question_new(active_user_id, user_id):
    '''For adding a new question for a particular user'''

    if request.method == "POST":
        request_JSON = request.json
        question_sent = request_JSON['question']
        question = Questions(question=question_sent, userid=active_user_id)
        db.session.add(question)
        db.session.commit()

        return jsonify({"response":"Your question is added successfully!"})        


@app.route('/users/questions',methods=['GET'])
def all_questions():
    '''For displaying all questions of all users'''

    if request.method == "GET":
        all_questions = Questions.query.all()

    list_of_ques = []

    for question in all_questions:
        a_question = {'id': question.id, 'question': question.question,'user_id':question.userid, 'time': question.timestamp}
        list_of_ques.append(a_question)

    return jsonify({'questions': list_of_ques, "status": "200"})


@app.route('/users/<user_id>/questions',methods=['GET'])
@token_verify
def questions(active_user_id, user_id):
    '''For displaying all questions of a particular user'''

    if request.method == "GET":
        questions = Questions.query.filter_by(userid=active_user_id).all()

    list_of_ques = []

    for question in questions:
        a_question = {'id': question.id, 'question': question.question,'user_id':question.userid, 'time': question.timestamp}
        list_of_ques.append(a_question)

    return jsonify({'questions': list_of_ques, "status": "200"})


@app.route('/users/<int:user_id>/questions/<int:question_id>',methods=['GET'])
@token_verify
def a_question_user(active_user_id ,user_id, question_id):
    '''For displaying a question of a particular user'''

    if request.method == "GET":
        question = Questions.query.filter_by(userid = active_user_id, id = question_id).first()

    a_question = {'id': question.id, 'question': question.question,'user_id':question.userid, 'time': question.timestamp}

    return jsonify({'question': a_question, "status": "200"})


@app.route('/users/<int:user_id>/questions/<int:question_id>', methods=['PUT'])
@token_verify
def update_question(active_user_id ,user_id, question_id):
    '''For updating a question of a partcular user'''

    if request.method == "PUT":
        update_question = request.json
        question = Questions.query.filter_by(id=question_id, userid=active_user_id).first()

        if not question:
            return jsonify({'message': 'No question found!', "status": "404"})

        question.question = update_question['question']

        db.session.commit()

        return jsonify({'message': 'Question has been changed!', "status": "200"})


@app.route('/users/<int:user_id>/questions/<int:question_id>', methods=['DELETE'])
@token_verify
def delete_question(active_user_id, user_id, question_id):
    '''For deleting a question of a user'''

    if request.method == "DELETE":
        question = Questions.query.filter_by(id=question_id, userid=active_user_id).first()

        if not question:
            return jsonify({'message': 'No question found!', "status": "404"})

        db.session.delete(question)
        db.session.commit()

        return jsonify({'message': 'Question item deleted!', "status": "200"})

from flask import render_template, flash, redirect, url_for, request, Flask, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db
from app.models import User, Question, Questions

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


@app.route('/users/<user_id>',methods=['GET'])
def user(user_id):
    '''For displaying a particular user'''

    if request.method == "GET":
    user = User.query.filter_by(userid=user_id).all()

    list_of_user = []

    for a_user in user:
        a_user = {'id': a_user.id, 'username': a_user.username, 'email': a_user.email}
        list_of_user.append(a_user)

    return jsonify({'response': list_of_user, "status": "200"})        


@app.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    '''For updating a user details'''

    user = User.query.filter_by(userid=user_id).first()
    new_details = request.json

    if not user:
        return jsonify({'message': 'No user found!', "status": "404"})

    if new_details["username"]:
        user.username = new_details["username"]

    if new_details["email"]:
        user.email = new_details["email"]

    db.session.commit()

    return jsonify({'message': 'The user has been updated!'})


@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    '''For deleting a user'''

    user = User.query.filter_by(id=user_id).first()

    if not user:
        return jsonify({'message': 'User not found', "status": "404"})

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'user deleted', "status": "200"})


@app.route('/users/<int:user_id>/question_new', methods=['POST'])
def question_new(user_id):
    '''For adding a new question for a particular user'''

    if request.method == "POST":
        request_JSON = request.json
        question_sent = request_JSON['question']
        question= Questions(question=question_sent, userid=user_id)
        db.session.add(question)
        db.session.commit()

        return jsonify({"response":"Your Question added successfully!"})        


@app.route('/users/questions',methods=['GET'])
def all_questions():
    '''For displaying all questions of all users'''

    if request.method == "GET":
    all_questions = Questions.query.all()

    list_of_ques = []

    for question in all_questions:
        a_question = {'id': question.id, 'text': question.question, 'time': question.timestamp}
        list_of_ques.append(a_question)

    return jsonify({'questions': list_of_ques, "status": "200"})



@app.route('/users/<user_id>/questions',methods=['GET'])
def questions(user_id):
    '''For displaying all questions of a particular user'''

    if request.method == "GET":
    questions = Questions.query.filter_by(userid=user_id).all()

    list_of_ques = []

    for question in questions:
        a_question = {'id': question.id, 'text': question.question, 'time': question.timestamp}
        list_of_ques.append(a_question)

    return jsonify({'questions': list_of_ques, "status": "200"})



@app.route('/users/user_id/questions/<question_id>', methods=['PUT'])
def update_question(user_id, question_id):
    '''For updating a question of a partcular user'''

    update_question = request.json
    question = Questions.query.filter_by(id=question_id, userid=user_id).first()

    if not question:
        return jsonify({'message': 'No question found!', "status": "404"})

    question.question = update_question['question']

    db.session.commit()

    return jsonify({'message': 'Question has been changed!', "status": "200"})


@app.route('/users/user_id/questions/<question_id>', methods=['DELETE'])
def delete_question(user_id, question_id):
    '''For deleting a question of a user'''

    question = Questions.query.filter_by(id=question_id, userid=user_id).first()

    if not question:
        return jsonify({'message': 'No question found!', "status": "404"})

    db.session.delete(question)
    db.session.commit()

    return jsonify({'message': 'Question item deleted!, "status": "200"'})

'''For directing the various API hits and the action to be performed on hits'''

from flask import render_template, flash, redirect, url_for, request, Flask, jsonify, make_response, request, \
     g, url_for, abort, current_app
from flask_login import logout_user, login_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db
from app.forms import  RegistrationForm, LoginForm, QuestionForm, AnswerForm, SearchForm, UpdateUserForm
from app.models import User, Questions
from app.config import Config
from functools import wraps
import jwt
import uuid
import datetime
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import (jwt_required, get_jwt_identity, create_access_token, get_raw_jwt)
from flask_babel import _, get_locale




@app.route("/covid/signup", methods=['GET', 'POST'])
def covid_signup():

    '''For registering a user'''

	#if current_user.is_authenticated:
	#	return redirect('userhome.html')

    form = RegistrationForm()

    if form.validate_on_submit():

        hashed_password = generate_password_hash(form.password.data, method = 'sha256')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)

        db.session.add(user)
        db.session.commit()

        flash(f'Your account has been created! You are now able to login', 'success')

        return redirect(url_for('covid_login'))

    return render_template('register.html', title='Register', form=form)


@app.route("/covid")
@app.route("/covid/login", methods=['GET', 'POST'])
def covid_login():
    '''For logging in a user'''

    #if current_user.is_authenticated:
    #    return render_template('userhome.html')
  
    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(username = form.username.data).first()
        questions = Questions.query.filter_by(userid = user.id)

        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect('userhome.html', user = user, questions = questions)
        else:
            flash(f'Login Unsuccessful. Please check email and password', 'danger')

    return render_template('login.html', title='Login', form=form)


@app.route('/covid/logout')
@login_required
def covid_logout():
    logout_user()
    return redirect(url_for('covid_login'))


@app.route('/covid/users')
def covid_all_users():
    """To display all users """
    
    users = User.query.all()
    
    return render_template('users.html', users=users)



@app.route('/covid/users/questions')
def covid_all_questions():
    """To display all questions"""

    questions = Questions.query.all()

    return render_template('questions.html', title='home', questions=questions)

'''
@app.route('/covid/user/<int:id>')
def covid_userhome(username, id):
    """To display current user details"""

    user = User.query.filter_by(name=username).first_or_404()
    questions = Questions.query.filter_by(user_id=current_user.id)
    return render_template('user.html', user=user, questions=questions, answers=answers)
'''

@app.route('/covid/user/<int:user_id>')
@login_required
def covid_user_account_details(user_id):
    """To display current user details"""

    user = User.query.filter_by(id=user_id).first()

    return render_template('useraccount.html', user = user)


@app.route("/covid/users/<int:user_id>", methods=['GET', 'POST'])
@login_required
def covid_updateuser(user_id):
    '''For updating a user'''

    user = User.query.filter_by(id = user_id).first()
    form = UpdateUserForm()

    if form.validate_on_submit():

        user = User.query.filter_by(id = user_id).first()

        user.username=form.username.data
        user.email=form.email.data

        db.session.commit()

        questions_user = Questions.query.filter_by(userid=user_id).all()

        flash(f'Details Updated', 'success')

        return redirect('userhome.html', user = user, questions = questions_user)

    return render_template('updateuser.html', title = 'Register', form = form, user = user)



@app.route('/covid/user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def covid_user_account_delete(user_id):
    """To delete the user"""

    user = User.query.filter_by(id=user_id).first()

    db.session.delete(user)
    db.session.commit()

    flash(f'User Deleted', 'success')

    return render_template('login.html')



@app.route('/covid/user/<int:user_id>/new_question', methods=['GET', 'POST'])
@login_required
def covid_new_question_for_account(user_id):
    """Function to add questions"""

    form = QuestionForm()

    if form.validate_on_submit():
        
        question = Questions(question=form.question.data, userid = current_user.id)
        
        db.session.add(question)
        db.session.commit()
        
        questions_user = Questions.query.filter_by(userid=user_id).all()
        user = User.query.filter_by(id=user_id).first() 

        flash('New question is added!')

        return  render_template('userhome.html', title='Question',user = user, questions = questions_user)

    return render_template('newquestion.html', title='Question', form=form)


@app.route('/covid/users/<int:user_id>/questions/<question_id>', methods=['GET', 'POST'])
@login_required
def covid_user_question_edit(user_id, question_id):
    '''To update a question'''

    question = Questions.query.filter_by(id = question_id).first()
    user = User.query.filter_by(id = user_id).first()   
    form = QuestionForm()
    form.question.data = question.question
        
    if form.validate_on_submit():
                
        question = Questions.query.filter_by(id = question_id).first()        
        question.question = form.question.data
                
        db.session.commit()

        questions_user = Questions.query.filter_by(userid = user_id).all()

        flash(f'Question Updated', 'success')

        return redirect('userhome.html', user = user, questions = questions_user)

    return render_template('editquestion.html', title = 'Register', form = form, user = user)



@app.route('/covid/users/<int:user_id>/questions/<question_id>', methods=['GET', 'POST'])
@login_required
def covid_user_question_delete(user_id, question_id):
    '''To delete a question'''

    question = Questions.query.filter_by(id = question_id).first()
    user = User.query.filter_by(id = user_id).first()   
    
    db.session.delete(question)
    db.session.commit()

    flash(f'Question Deleted', 'success')

    questions_user = Questions.query.filter_by(userid = user_id).all()

    flash(f'Question Updated', 'success')

    return redirect('userhome.html', user = user, questions = questions_user)




















#---------------------------------------------------------------------------------------------------------------

def jwt__required(function):
    """This function is used to verify token and act as step of authorization"""

    @wraps(function)
    def verify_token_for_user(*args, **kwargs):
        
        token = None
        if 'token' in request.headers:
            token = request.headers['token']
            print(token)

        if not token:
            return make_response('Missing Token', 401)
        
        try:
            jwt__required = jwt.decode(token, Config.SECRET_KEY)
            active_user = User.query.filter_by(id = jwt__required['user_id']).first()
            active_user_id = active_user.id
        except:
            return make_response('Invalid token', 404)

        return function(active_user_id, *args, **kwargs)

    return verify_token_for_user



@app.route('/api/login')
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

        return jsonify({'hashed_token': hashed_token.decode('UTF-8'), "status" : "200 OK"})


@app.route('/api/signup', methods = ['POST'])
def signup():
    '''For adding user to User table'''

    if request.method == "POST":
        request_JSON = request.json
        print(request_JSON)
        username_sent = request_JSON['username']
        email_sent = request_JSON['email']
        password_sent = generate_password_hash(request_JSON['password'], method = 'sha256')
        newuser = User(username = username_sent, email = email_sent, password = password_sent)
        db.session.add(newuser)
        db.session.commit()

        return jsonify({"response":"User " + username_sent + " added successfully!", "status": "200 OK"})


@app.route('/api/users', methods = ['GET'])
def all_users():
    '''For displaying all users'''

    if request.method == "GET":
        users_data = User.query.all()

        if not users_data:
            return jsonify({'message': 'No user present in table!', "status": "404"})

        print(users_data)
        list_data = []
        for user in users_data:
            user_data1 = {"id":user.id, "username":user.username, "email": user.email}
            list_data.append(user_data1)
        return jsonify({"response:" : list_data, "status": "200 OK"})


@app.route('/api/users/<int:user_id>',methods = ['GET'])
@jwt__required
def user(active_user_id ,user_id):
    '''For displaying a particular user'''

    if request.method == "GET":
        user = User.query.filter_by(id = active_user_id).first()

        if not user:
            return make_response('No such user', 401)    

    a_user = {'id': user.id, 'username': user.username, 'email': user.email}
    
    return jsonify({'user': a_user, "status": "200 OK"})        


@app.route('/api/users/<int:user_id>', methods = ['PUT'])
@jwt__required
def update_user(active_user_id, user_id):
    '''For updating a user details'''

    if request.method == "PUT":

        user = User.query.filter_by(id = active_user_id).first()
        
        if not user:
            return make_response('No such user found', 404)

        new_details = request.json
        user.username = new_details["username"]
        user.email = new_details["email"]

        db.session.commit()

        return jsonify({'message': 'The user has been updated!', "status": "200 OK"})


@app.route('/api/users/<int:user_id>', methods = ['DELETE'])
@jwt__required
def delete_user(active_user_id ,user_id):
    '''For deleting a user'''

    if request.method == "DELETE":
        user = User.query.filter_by(id=active_user_id).first()

        if not user:
            return make_response('User not found', 404)

        db.session.delete(user)
        db.session.commit()

        return make_response('The user is deleted', 200)


@app.route('/api/users/<int:user_id>/question_new', methods = ['POST'])
@jwt__required
def question_new(active_user_id, user_id):
    '''For adding a new question for a particular user'''

    if request.method == "POST":
        request_JSON = request.json
        question_sent = request_JSON['question']
        question = Questions(question = question_sent, userid = active_user_id)
        db.session.add(question)
        db.session.commit()

        return jsonify({"response":"Your question is added successfully!", "status": "200 OK"})        


@app.route('/api/users/questions',methods = ['GET'])
def all_questions():
    '''For displaying all questions of all users'''

    if request.method == "GET":
        all_questions = Questions.query.all()

        if not all_questions:
            return jsonify({'message': 'No questions found!', "status": "404"})

    list_of_ques = []

    for question in all_questions:
        a_question = {'id': question.id, 'question': question.question,'user_id':question.userid, \
                      'time': question.timestamp}
        list_of_ques.append(a_question)

    return jsonify({'questions': list_of_ques, "status": "200 OK"})


@app.route('/api/users/<user_id>/questions',methods = ['GET'])
@jwt__required
def questions(active_user_id, user_id):
    '''For displaying all questions of a particular user'''

    if request.method == "GET":
        questions = Questions.query.filter_by(userid = active_user_id).all()

        if not questions:
            return jsonify({'message': 'No questions found!', "status": "404"})

    list_of_ques = []

    for question in questions:
        a_question = {'id': question.id, 'question': question.question,'user_id':question.userid, \
                      'time': question.timestamp}
        list_of_ques.append(a_question)

    return jsonify({'questions': list_of_ques, "status": "200 OK"})


@app.route('/api/users/<int:user_id>/questions/<int:question_id>',methods = ['GET'])
@jwt__required
def a_question_user(active_user_id ,user_id, question_id):
    '''For displaying a question of a particular user'''

    if request.method == "GET":
        question = Questions.query.filter_by(userid = active_user_id, id = question_id).first()

        if not question:
            return jsonify({'message': 'No question found!', "status": "404"})
            
    a_question = {'id': question.id, 'question': question.question,'user_id':question.userid, \
                  'time': question.timestamp}

    return jsonify({'question': a_question, "status": "200 OK"})


@app.route('/api/users/<int:user_id>/questions/<int:question_id>', methods=['PUT'])
@jwt__required
def update_question(active_user_id ,user_id, question_id):
    '''For updating a question of a partcular user'''

    if request.method == "PUT":
        update_question = request.json
        question = Questions.query.filter_by(id=question_id, userid = active_user_id).first()

        if not question:
            return jsonify({'message': 'No question found!', "status": "404"})

        question.question = update_question['question']

        db.session.commit()

        return jsonify({'message': 'Question has been changed!', "status": "200"})


@app.route('/api/users/<int:user_id>/questions/<int:question_id>', methods = ['DELETE'])
@jwt__required
def delete_question(active_user_id, user_id, question_id):
    '''For deleting a question of a user'''

    if request.method == "DELETE":
        question = Questions.query.filter_by(id = question_id, userid = active_user_id).first()

        if not question:
            return make_response('No question forund', 404)

        db.session.delete(question)
        db.session.commit()

        return make_response('The question is deleted', 200)


#------------------------------------------------------------------------------------------------------------------













#---------------------------------------------------------------------------------------------------------------------


'''
@app.route('/users/<int:user_id>/questions/<int:question_id>answer_new', methods = ['POST'])
@jwt__required
def answer_new(active_user_id, user_id, question_id):
    For adding a new answer for a particular question
    if request.method == "POST":
        received_data = request.json
        answer_received = received_data['answer_of_ques']
        answer = Answers(answer_of_ques = answer_received, quesid = question_id)
        db.session.add(answer)
        db.session.commit()

        return jsonify({"response":"Your answer is added successfully!", "status": "200 OK"})        


@app.route('/users/<int:user_id>/questions/<int:question_id>/<int:answer_id>',methods = ['GET'])
@jwt__required
def a_question_user(active_user_id ,user_id, question_id):
    For displaying a question of a particular user

    if request.method == "GET":
        question = Questions.query.filter_by(userid = active_user_id, id = question_id).first()

        if not question:
            return jsonify({'message': 'No question found!', "status": "404"})
            
    a_question = {'id': question.id, 'question': question.question,'user_id':question.userid, \
                  'time': question.timestamp}

    return jsonify({'question': a_question, "status": "200 OK"})


@app.route('/users/<int:user_id>/questions/<int:question_id>', methods=['PUT'])
@jwt__required
def update_question(active_user_id ,user_id, question_id):
    For updating a question of a partcular user

    if request.method == "PUT":
        update_question = request.json
        question = Questions.query.filter_by(id=question_id, userid = active_user_id).first()

        if not question:
            return jsonify({'message': 'No question found!', "status": "404"})

        question.question = update_question['question']

        db.session.commit()

        return jsonify({'message': 'Question has been changed!', "status": "200"})


@app.route('/users/<int:user_id>/questions/<int:question_id>', methods = ['DELETE'])
@jwt__required
def delete_question(active_user_id, user_id, question_id):
    For deleting a question of a user

    if request.method == "DELETE":
        question = Questions.query.filter_by(id = question_id, userid = active_user_id).first()

        if not question:
            return make_response('No question forund', 404)

        db.session.delete(question)
        db.session.commit()

        return make_response('The question is deleted', 200)

'''

#--------------------------------------------------------------------------------------------------------------------------
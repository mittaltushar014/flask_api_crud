'''For directing the various API hits and the action to be performed on hits'''

import requests
from flask import render_template, flash, redirect, url_for, request, Flask, jsonify, make_response, request, \
     g, url_for, abort, current_app, json
from flask_login import logout_user, login_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db
from app.forms import  RegistrationForm, LoginForm, QuestionForm, AnswerForm, SearchForm, UpdateUserForm
from app.models import User, Questions, Answers
from app.config import Config
from app.background_jobs import update_covid_stats
from app.graph import plot_graph
from functools import wraps
import jwt
import uuid
import datetime
from sqlalchemy.exc import IntegrityError
from flask_babel import _, get_locale


@app.before_request
def before_request():
    '''For making active the form so that changes can be seen and made in elasticsearch table'''

    if current_user.is_authenticated:
        g.search_form = SearchForm()
    g.locale = str(get_locale())


@app.route("/graph", methods=['GET'])
def web_graph():
    '''Function to analyse and display graphs'''

    plot_graph()
    return render_template('graph.html')


@app.route("/signup", methods=['GET', 'POST'])
def web_signup():
    '''For registering a user'''

    form = RegistrationForm()

    if form.validate_on_submit():

        hashed_password = generate_password_hash(form.password.data, method = 'sha256')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)

        db.session.add(user)
        db.session.commit()

        flash(f'Your account has been created! You are now able to login', 'success')

        return redirect(url_for('web_login'))

    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def web_login():
    '''For logging in a user'''

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(username = form.username.data).first()
        questions = Questions.query.filter_by(userid = user.id).all()
        answers = Answers.query.filter_by(userid = user.id).all()

        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return render_template('userhome.html', user = user, questions = questions, answers = answers)
        else:
            flash(f'Login Unsuccessful. Please check username and password', 'danger')

    plot_graph.delay()
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
@login_required
def web_logout():
    logout_user()
    return redirect(url_for('web_login'))


@app.route('/users')
def web_all_users():
    """To display all users """
    
    users = User.query.all()
    
    return render_template('users.html', users=users)


@app.route('/users/questions')
def web_all_questions():
    """To display all questions"""

    questions = Questions.query.all()
    answers = Answers.query.all()

    return render_template('questions.html', title='Questions', questions = questions, answers = answers)


@app.route('/users/questions/<int:question_id>/answers/answer')
def web_public_answer(question_id):
    '''To display answer of a particular question in public'''

    answer= Answers.query.filter_by(quesid = question_id).first()

    return render_template('publicanswer.html', title='Answer', answer = answer)


@app.route('/users/<int:user_id>')
@login_required
def web_user_account_details(user_id):
    """To display current user details"""

    user = User.query.filter_by(id=user_id).first()

    return render_template('useraccount.html', user = user)


@app.route("/users/<int:user_id>/edit", methods=['GET', 'POST'])
@login_required
def web_update_user(user_id):
    '''For updating a user'''

    user = User.query.filter_by(id = user_id).first()
    form = UpdateUserForm()

    if form.validate_on_submit():

        user = User.query.filter_by(id = user_id).first()

        user.username=form.username.data
        user.email=form.email.data

        db.session.commit()

        questions_user = Questions.query.filter_by(userid=user_id).all()
        answers_user = Answers.query.filter_by(userid = user_id).all()

        flash(f'Details Updated', 'success')

        return render_template('userhome.html', user = user, questions = questions_user, answers = answers_user)

    return render_template('updateuser.html', title = 'Update User', form = form, user = user)



@app.route('/users/<int:user_id>/delete', methods=['GET', 'POST'])
@login_required
def web_delete_user(user_id):
    """To delete the user"""

    user = User.query.filter_by(id=user_id).first()

    db.session.delete(user)
    db.session.commit()

    flash(f'User Deleted', 'success')

    form = LoginForm()
    return render_template('login.html', title='Login', form = form)



@app.route('/users/<int:user_id>/question_new', methods=['GET', 'POST'])
@login_required
def web_new_question_for_account(user_id):
    """Function to add questions"""

    form = QuestionForm()

    if form.validate_on_submit():
        
        question = Questions(question=form.question.data, userid = current_user.id)
        
        db.session.add(question)
        db.session.commit()
        
        questions_user = Questions.query.filter_by(userid=user_id).all()
        user = User.query.filter_by(id=user_id).first()
        answers_user = Answers.query.filter_by(userid=user_id).all()

        flash('New question is added!')
        
        if answers_user:
            return  render_template('userhome.html', title='User Home',user = user, questions = questions_user, answers = answers_user)
        else:
            return  render_template('userhome.html', title='User Home',user = user, questions = questions_user)
    
    return render_template('newquestion.html', title='New Question', form=form)


@app.route('/users/<int:user_id>/questions/<int:question_id>/edit', methods=['GET', 'POST'])
@login_required
def web_user_question_edit(user_id, question_id):
    '''To update a question'''

    question = Questions.query.filter_by(id = question_id).first()
    user = User.query.filter_by(id = user_id).first()   
    form = QuestionForm()
    form.question.data = question.question
        
    if form.validate_on_submit():

        question = Questions.query.filter_by(id = question_id).first()            
        question.question=form.question.data
        
        db.session.commit()

        questions_user = Questions.query.filter_by(userid = user_id).all()
        answers_user = Answers.query.filter_by(userid = user_id).all()

        flash(f'Question Updated', 'success')

        if answers_user:
            return render_template('userhome.html', user = user, questions = questions_user, answers = answers_user)
        else:
            return render_template('userhome.html', user = user, questions = questions_user)    

    return render_template('editquestion.html', title = 'Edit Question', form = form, user = user)


@app.route('/users/<int:user_id>/questions/<int:question_id>/delete', methods=['GET', 'POST'])
@login_required
def web_user_question_delete(user_id, question_id):
    '''To delete a question'''

    question = Questions.query.filter_by(id = question_id).first()
    user = User.query.filter_by(id = user_id).first()
    
    db.session.delete(question)
    db.session.commit()

    flash(f'Question Deleted', 'success')

    questions_user = Questions.query.filter_by(userid = user_id).all()

    return render_template('userhome.html', user = user, questions = questions_user)


@app.route('/users/<int:user_id>/questions/<int:question_id>/answers')
@login_required
def web_user_question_answer(user_id, question_id):
    '''To display answer for a particular question for a particular user'''

    answer = Answers.query.filter_by(quesid = question_id).first()
    user = User.query.filter_by(id = user_id).first()
    question = Questions.query.filter_by(id= question_id).first() 

    return render_template('useranswer.html', title='Answer', user = user, question = question, answer = answer)


@app.route('/users/<int:user_id>/questions/<int:question_id>/answer_new', methods=['GET', 'POST'])
@login_required
def web_new_answer_for_account(user_id, question_id):
    """To add answer for a particular question"""

    form = AnswerForm()

    if form.validate_on_submit():

        answer = Answers(answer_of_ques = form.answer.data, userid = user_id, quesid = question_id )

        db.session.add(answer)
        db.session.commit()
        
        questions_user = Questions.query.filter_by(userid=user_id).all()
        user = User.query.filter_by(id=user_id).first()
        answers_user = Answers.query.filter_by(userid=user_id).all()

        flash('New answer is added!')

        return  render_template('userhome.html', title='User Home',user = user, questions = questions_user, answers = answers_user)

    return render_template('newanswer.html', title='New Answer', form=form)


@app.route('/users/<int:user_id>/questions/<question_id>/answers/edit', methods=['GET', 'POST'])
@login_required
def web_user_answer_edit(user_id, question_id):
    '''To update an answer'''

    user = User.query.filter_by(id = user_id).first()   
    answer= Answers.query.filter_by(userid = user_id, quesid = question_id).first()
    form = AnswerForm()
    form.answer.data = answer.answer_of_ques
        
    if form.validate_on_submit():
                
        answer = Answers.query.filter_by(quesid = question_id).first()        
        answer.answer_of_ques = form.answer.data
                
        db.session.commit()

        questions_user = Questions.query.filter_by(userid = user_id).all()
        answers_user = Answers.query.filter_by(userid = user_id).all()

        flash(f'Answer Updated', 'success')

        return render_template('userhome.html', user = user, questions = questions_user, answers = answers_user)

    return render_template('editanswer.html', title = 'Edit Answer', form = form, user = user)


@app.route('/users/<int:user_id>/questions/<question_id>/answers/delete', methods=['GET', 'POST'])
@login_required
def web_user_answer_delete(user_id, question_id):
    '''To delete an answer'''

    user = User.query.filter_by(id = user_id).first()
    answer = Answers.query.filter_by(quesid = question_id).first()  
    
    db.session.delete(answer)
    db.session.commit()

    flash(f'Answer Deleted', 'success')

    questions_user = Questions.query.filter_by(userid = user_id).all()

    return render_template('userhome.html', user = user, questions = questions_user)    


@app.route('/search')
@login_required
def search():
    if not g.search_form.validate():
        user = User.query.filter_by(id = current_user.id).first()
        questions = Questions.query.filter_by(userid = user.id).all()
        answers = Answers.query.filter_by(userid = user.id).all()
        
        return render_template('userhome.html', user = user, questions = questions, answers = answers)

    page = request.args.get('page', 1, type=int)
    
    questions, total = Questions.search(g.search_form.q.data, page)

    user_this = User.query.filter_by(id=current_user.id).first()
   
    if total:
        return render_template('search.html', title='Search', user=user_this, questions=questions)
    else:
        return render_template('search.html', title='Search', user=user_this)








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

        return {'hashed_token': hashed_token.decode('UTF-8')}, 200


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

        return {"response":"User " + username_sent + " added successfully!"}, 200


@app.route('/api/users', methods = ['GET'])
def all_users():
    '''For displaying all users'''

    if request.method == "GET":
        users_data = User.query.all()

        if not users_data:
            return {'message': 'No user present in table!'}, 404

        print(users_data)
        list_data = []
        for user in users_data:
            user_data1 = {"id":user.id, "username":user.username, "email": user.email}
            list_data.append(user_data1)
        return {"response:" : list_data}, 200


@app.route('/api/users/<int:user_id>',methods = ['GET'])
@jwt__required
def user(active_user_id ,user_id):
    '''For displaying a particular user'''

    if request.method == "GET":
        user = User.query.filter_by(id = active_user_id).first()

        if not user:
            return make_response('No such user', 401)    

    a_user = {'id': user.id, 'username': user.username, 'email': user.email}
    
    return {'user': a_user}, 200        


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
        questions = Questions.query.filter_by(userid=active_user_id).all()
        answers = Auestions.query.filter_by(userid=active_user_id).all()
        

        if not user:
            return make_response('User not found', 404)

        db.session.delete(user)
        
        if questions:
            db.session.delete(questions)
        
        if answers:
            db.session.delete(answers)
        
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

        return make_response("Your question is added successfully!", 200)     


@app.route('/api/users/questions',methods = ['GET'])
def all_questions():
    '''For displaying all questions of all users'''

    if request.method == "GET":
        all_questions = Questions.query.all()

        if not all_questions:
            return make_response("No questions found!", 404)

    list_of_ques = []

    for question in all_questions:
        a_question = {'id': question.id, 'question': question.question,'user_id':question.userid, \
                      'time': question.timestamp}
        list_of_ques.append(a_question)

    return {'questions': list_of_ques}, 200


@app.route('/api/users/<user_id>/questions',methods = ['GET'])
@jwt__required
def user_questions(active_user_id, user_id):
    '''For displaying all questions of a particular user'''

    if request.method == "GET":
        questions = Questions.query.filter_by(userid = active_user_id).all()

        if not questions:
            return make_response('No questions found!', 404)

    list_of_ques = []

    for question in questions:
        a_question = {'id': question.id, 'question': question.question,'user_id':question.userid, \
                      'time': question.timestamp}
        list_of_ques.append(a_question)

    return {'questions': list_of_ques}, 200


@app.route('/api/users/<int:user_id>/questions/<int:question_id>',methods = ['GET'])
@jwt__required
def a_user_question(active_user_id ,user_id, question_id):
    '''For displaying a question of a particular user'''

    if request.method == "GET":
        question = Questions.query.filter_by(userid = active_user_id, id = question_id).first()

        if not question:
            return make_response('No question found!', 404)
            
    a_question = {'id': question.id, 'question': question.question,'user_id':question.userid, \
                  'time': question.timestamp}

    return {'question': a_question}, 200


@app.route('/api/users/<int:user_id>/questions/<int:question_id>', methods=['PUT'])
@jwt__required
def update_question(active_user_id ,user_id, question_id):
    '''For updating a question of a partcular user'''

    if request.method == "PUT":
        update_question = request.json
        question = Questions.query.filter_by(id=question_id, userid = active_user_id).first()

        if not question:
            return make_response('No question found!', 404)

        question.question = update_question['question']

        db.session.commit()

        return make_response('Question has been changed!', 200)


@app.route('/api/users/<int:user_id>/questions/<int:question_id>', methods = ['DELETE'])
@jwt__required
def delete_question(active_user_id, user_id, question_id):
    '''For deleting a question of a user'''

    if request.method == "DELETE":
        question = Questions.query.filter_by(id = question_id, userid = active_user_id).first()
        answers = Answers.query.filter_by(quesid = question_id).all()

        if not question:
            return make_response('No question forund', 404)

        db.session.delete(question)

        if answers:
            db.session.delete(answers)
        
        db.session.commit()

        return make_response('The question is deleted', 200)








@app.route('/api/users/<int:user_id>/questions/<int:question_id>/answer_new', methods = ['POST'])
@jwt__required
def answer_new(active_user_id, user_id, question_id):
    '''For adding a new answer for a particular question of a particular answer'''

    if request.method == "POST":
        request_JSON = request.json
        answer_sent = request_JSON['answer']
        answer = Answers(answer_of_ques = answer_sent, userid = active_user_id, quesid = question_id)
        db.session.add(answer)
        db.session.commit()

        return make_response("Your answer is added successfully!", 200)            


@app.route('/api/users/questions/answers',methods = ['GET'])
def all_answers():
    '''For displaying all answers of all questions of all users'''

    if request.method == "GET":
        all_answers = Answers.query.all()

        if not all_answers:
            return make_response('No answers found!', 404)

    list_of_answers = []

    for answer in all_answers:
        an_answer = {'id': answer.id, 'answer': answer.answer_of_ques,'user_id':answer.userid, \
                      'question_id': answer.quesid, 'time': answer.timestamp}
        list_of_answers.append(an_answer)

    return {'answers': list_of_answers}, 200



@app.route('/api/users/<int:user_id>/questions/answers',methods = ['GET'])
@jwt__required
def all_answers_user(active_user_id, user_id):
    '''For displaying all answers of a particular user'''

    if request.method == "GET":
        answers = Answers.query.filter_by(userid = active_user_id).all()

        if not answers:
            return make_response('No answers found!', 404)

    list_of_answers = []

    for answer in answers:
        an_answer = {'id': answer.id, 'answer': answer.answer_of_ques,'user_id':answer.userid, \
                      'question_id': answer.quesid, 'time': answer.timestamp}
        list_of_answers.append(an_answer)

    return {'answers': list_of_answers}, 200


@app.route('/api/users/<int:user_id>/questions/<int:question_id>/answers',methods = ['GET'])
@jwt__required
def an_answer_of_question(active_user_id ,user_id, question_id):
    '''For displaying an answer of a particular question of a particular user'''

    if request.method == "GET":
        answer = Answers.query.filter_by(userid = active_user_id, quesid = question_id).first()

        if not answer:
            return make_response('No answer found!', 404)
            
    an_answer = {'id': answer.id, 'answer': answer.answer_of_ques,'user_id':answer.userid, \
                  'question_id': answer.quesid, 'time': answer.timestamp}

    return {'answer': an_answer}, 200


@app.route('/api/users/<int:user_id>/questions/<int:question_id>/answers', methods=['PUT'])
@jwt__required
def update_answer(active_user_id ,user_id, question_id):
    '''For updating an answer for a particular question of a partcular user'''

    if request.method == "PUT":
        update_answer = request.json
        answer = Answers.query.filter_by(userid = active_user_id, quesid = question_id).first()

        if not answer:
            return make_response('No answer found', 404)

        answer.answer_of_ques = update_answer['answer']

        db.session.commit()

        return make_response('Answer has been changed', 200)


@app.route('/api/users/<int:user_id>/questions/<int:question_id>/answers', methods = ['DELETE'])
@jwt__required
def delete_answer(active_user_id, user_id, question_id):
    '''For deleting an answer for a particular queston of a particular user'''

    if request.method == "DELETE":
        answer = Answers.query.filter_by(userid = active_user_id, quesid = question_id).first()

        if not answer:
            return make_response('No answer forund', 404)

        db.session.delete(answer)
        db.session.commit()

        return make_response('The answer is deleted', 200)


@app.route('/api/covid_stats', methods=['PUT'])
def update_covid_data_api():
    '''Handles PUT requests to update the Covid infection stats from a csv file.'''

    task = update_covid_stats.delay(app.config['COVID_DATA_INDEX'])
    return {"msg": "Updating covid data in the background",
            "task_id": task.task_id}

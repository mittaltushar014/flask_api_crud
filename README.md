Project implementing Create, Read, Update, Delete features for Users and the questions posted by them using Flask and API from backend.

####Features:
>Register user

>Browse all questions and users

>Create a user              
>Update a user     
>Delete a user  
>View a user              

>Post a question              
>Edit a question     
>Delete a question  
>View a question              

####Technologies Used:

Python  
Flask   
SQLAlchemy  
SQLite  
Postman 

####How to:
>Install python 3.7.

>Run in termainal:

    pip install -r requirements.txt

>Read documentation for how to create url for getting the response.

>Run in terminal:

    flask run

>Do API hits using Postman.


####Directory Structure:    
    
.   
├── app 
│   ├── __init__.py 
│   ├── models.py   
│   └── routes.py   
├── app.db  
├── config.py   
├── Documentation   
│   ├── API_Documentation   
│   └── DB_Documentation    
├── question_work.py    
├── README.md   
└── requirements.txt    


####API Documentation


Creating question of a user
    
    • URL
      users/user_id/question_new/
    • METHOD
      POST
    • URL Params
      Required
      id = user_id
    • DATA Params
      Required
      question=”The question asked”
    • SUCCESS RESPONSE
      Code: 200
      Content:{status:”New Question added!”}
    • ERROR RESPONSE
      Code:400 BAD REQUEST
      Content: {status:”Invalid User_id to post question” or status: "No content of question!"}

Getting a question of a user

    • URL
      users/user_id/questions/question_id 
    • METHOD
      GET
    • URL Params
      Required
      id's = [question_id, user_id]
    • SUCCESS RESPONSE
      Code: 200
      Content:{question:”The content of question”}
    • ERROR RESPONSE
      Code:400 BAD REQUEST
      Content: {status:”invalid id provided}

Getting all questions of a user

    • URL
      users/user_id/questions
    • METHOD
      GET
    • URL Params
      Required
      id = [user_id]
    • SUCCESS RESPONSE
      Code: 200
      Content:{question:”The content of questions”}
    • ERROR RESPONSE
      Code:400 BAD REQUEST
      Content: {status:”invalid id provided}

Getting all questions of all users

    • URL
      users/questions
    • METHOD
      GET
    • URL Params
      Required
      None
    • SUCCESS RESPONSE
      Code: 200
      Content:{question:”The content of questions”}
    • ERROR RESPONSE
      Code:400 BAD REQUEST
      Content: {status:”invalid id provided}
      

Updating a question of a user
    
    • URL
      users/user_id/questions/question_id
    • METHOD
      PUT
    • URL Params
      Required
      id’s = [user_id, question_id]
    • DATA Params
      Required
      question="mew content of question"
    • SUCCESS RESPONSE
      Code: 200
      Content:{status:”Question edited!”}
    • ERROR RESPONSE
      Code:400 BAD REQUEST
      Content: {status:"Invalid User id or Question id"}
    
Deleting Questions
    
    • URL
      users/user_id/questions/question_id
    • METHOD
      DELETE
    • URL Params
      Required
      id’s = [user_id, question_id]
    • DATA Params
      None
    • SUCCESS RESPONSE
      Code: 200
      Content:{status:”Question deleted!”}
    • ERROR RESPONSE
      Code:400 BAD REQUEST
      Content: {status:"Invalid User id or Question id"}



Creating a user
    
    • URL
      signup/
    • METHOD
      POST
    • URL Params
      Required
      None
    • DATA Params
      Required
      username="the name of user"
      email="email of user"
      password="the password of user"
    • SUCCESS RESPONSE
      Code: 200
      Content:{status:”New User added!”}
    • ERROR RESPONSE
      Code:400 BAD REQUEST
      Content: {status:”Invalid"}

Getting all users

    • URL
      /users
    • METHOD
      GET
    • URL Params
      Required
      None
    • SUCCESS RESPONSE
      Code: 200
      Content:{username:”The name of user”}
    • ERROR RESPONSE
      Code:400 BAD REQUEST
      Content: {status:"invalid"}

Getting details of a particular user

    • URL
      /users/user_id
    • METHOD
      GET
    • URL Params
      Required
      id=[user_id]
    • SUCCESS RESPONSE
      Code: 200
      Content:{username:”The name of user”}
    • ERROR RESPONSE
      Code:400 BAD REQUEST
      Content: {status:"invalid"}

Updating a user
    
    • URL
      users/user_id
    • METHOD
      PUT
    • URL Params
      Required
      id’s = [user_id]
    • DATA Params
      Required
      username="new name of user"
      email="new email of user"
    • SUCCESS RESPONSE
      Code: 200
      Content:{status:"User updated!”}
    • ERROR RESPONSE
      Code:400 BAD REQUEST
      Content: {status:"Invalid User id"}


Deleting a user
    
    • URL
      users/user_id
    • METHOD
      DELETE
    • URL Params
      Required
      id’s = [user_id]
    • DATA Params
      Required
      None
    • SUCCESS RESPONSE
      Code: 200
      Content:{status:"User deleted!”}
    • ERROR RESPONSE
      Code:400 BAD REQUEST
      Content: {status:"Invalid User id"}



####Database Documentation

Schema for Database:

User - Table :

id          --- int            --- primary key(auto incremented)
name        --- string(25)     --- unique value
email       --- string(25)     --- unique value
password    --- string(25)     --- hashed password


Questions - Table :

id          --- int            --- primary key(auto incremented)
user_id     --- int            --- foreign key(linked with id in user table)
question    --- string(200)    --- 
Datetime    --- datetime       --- date and time of posting of question



      
      
      
    

Project implementing Create, Read, Update, Delete features for Users and their questions and answers posted by them using Flask and API from backend and frontend.   

####Features:
>Register user

>Browse all questions and answers and users.    

>Create a user              
>Update a user     
>Delete a user  
>View a user              

>Post a question              
>Edit a question     
>Delete a question  
>View a question              

>Post an answer              
>Edit an answer     
>Delete an answer  
>View an answer              


####Technologies Used:

Python  
Flask   
SQLAlchemy  
SQLite  
Postman     

####How to: 
>Install python 3.6.    

>Run in termainal:  

    pip install -r requirements.txt     

>Read documentation for how to create url for getting the response.     

>Run in terminal:   
    
    flask run   

>Do API hits using Postman.     
>Open frontend and use the website.     


####Directory Structure:     
          
.   
├── app     
│   ├── config.py   
│   ├── forms.py    
│   ├── __init__.py     
│   ├── models.py   
│   ├── routes.py   
│   ├── search.py   
│   └── templates   
│       ├── base.html   
│       ├── editanswer.html     
│       ├── editquestion.html   
│       ├── login.html  
│       ├── newanswer.html  
│       ├── newquestion.html    
│       ├── publicanswer.html   
│       ├── questions.html  
│       ├── register.html   
│       ├── search.html     
│       ├── updateuser.html     
│       ├── useraccount.html    
│       ├── useranswer.html     
│       ├── userhome.html       
│       └── users.html      
├── app.db  
├── config.py   
├── Documentation   
│   ├── API_Documentation   
│   └── DB_Documentation    
├── main_run.py     
├── Postman_Collection      
│   └── flask_api_crud.postman_collection.json  
├── README.md   
├── requirements.txt    
├── User_Stories    
│   └── user_story.txt  
└── Wireframes  
    ├── Account_Page.png    
    ├── Login.png   
    ├── SignUp.png  
    ├── User_Account_Details_Update.png     
    └── User_account_first_page.png     
            
    
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
        
Answers - Table :   
    
id                  --- int            --- primary key(auto incremented)    
userid              --- int            --- foreign key(linked with id in user table)    
quesid              --- int            --- foreign key(linked with id in questions table)   
answer_of_ques      --- string(200)    ---  
Datetime            --- datetime       --- date and time of posting of answer   



      
      
      
    

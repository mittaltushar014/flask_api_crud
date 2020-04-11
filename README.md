Project implementing Create, Read, Update, Delete features for Users and their questions and answers posted by them using Flask and API from backend and frontend.   
In frontend searching for questions and answers functionality is also added.

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

>Search in questions and answers.   


####Technologies Used:

Python  
Flask   
SQLAlchemy  
SQLite  
Postman     

####How to:     
>Install python 3.6.    
>Install redis:     
    wget http://download.redis.io/redis-stable.tar.gz       
    tar xvzf redis-stable.tar.gz        
    cd redis-stable     
    make    
    sudo make install   

>Run in termainal:  

    pip install -r requirements.txt     

>Start Elasticsearch, Redis and Celery.     
    Elasticsearch -> sudo -i service elasticsearch start    
    Celery -> celery -A app.celery worker --loglevel=info   
    Redis -> redis-server   

>Run in terminal:   
    
    flask run   

>Read documentation for how to create url for getting the response.     

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



      
      
      
    

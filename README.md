# CITS3403

## Name of the application
ChatSome

## Purpose of the application
The aim of ChatSome is to provide personalised learning and professional development
by leveraging the power of one-on-one communication. With today's evolution on digital world, ChatSome brings back the human touch to education and mentorship, fostering meaningful connections that drive success for the users. 

Some key objectives that highlights the ChatSome: 

1.Personalized Learning Experience - provide customized feedback and guidance that adapts to each other's pace and progress and empowering students to achieve their
academic goals through personalized interaction with expert tutors.

2.Effective Mentorship - facilitate our users in exchanging their knowledge and skills in flexible environment, support career growth through meaningful mentor-
mentee relationships by connecting with them in their field of interest.

3.Enhanced Engagement - encouraging active participation and dialogue, and provide
a supportive, welcoming community where learners and professionals feel valued and
motivated. 

### Design and Use
The focus on the ChatSome's design is on simplicity, user-friendliness, and robust
functionality, to ensure a seamless experience for both tutors and students. 

The design features on this application consists of:

1.Private Chatrooms - users can create their own private chatrooms for one-on-one
interactions, ensuring a focused and personalized communication envirionment. Also,
this facilitates a real-time messaging in their own chatrooms, enabling instant 
feedback and continuous dialogue between users. 

2.File Sharing - provide the capabilities for file sharing, which allow users to 
exchange documents, assignments, resources and feedbacks directly within the 
chatroom. Our application supports various file formarts, which accomodate different
types of educational and mentoring materials.

3.User Profiles - Each user has their own profile, which provides them the capability
to change their password of their account if required to do so. 

4.Account Management - this includes secure login and logout processes and password
change options, which ensures that user data is protected and accessible only by
authorized individuals.

5.Tutorial page - a detailed tutorial is to guide new users through the features
and functionalities of the application, providing step-by-step instructions to assist
users on getting started with ChatSome. 

## Team Members
| UWA ID | Name | Github Username |
| --------------- | --------------- | --------------- |
| 22848932 | Celyn Chew | CelynChew |
| 23641633  | Chuen Yui Lam  | Roy-Lam  |
| 23251142  | Benjamin Cooper | bc163836 |
| 23237969 | Felicia Sindhu | sindhufelicia |

## How to launch the application
Create Virtual Environment:

```python3 -m venv .venv```

Activate Environment:                              

Mac ```. .venv/bin/activate```   

Windows ``` .venv/Scripts/activate```     IF ERROR ```Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser```

Install Requirements (if needed):

1. Update pip: ```pip install --upgrade pip```

2. Requirements: ```pip install -r requirements.txt```

Initialise Database: 

```flask db init```                                

```flask db migrate -m "Initial migration"```  

- If error occurs (start from ```flask db init```  after making new directory in migration)

- ```Remove-Item -Recurse -Force migrations```

- ```mkdir migrations```

Create tables:

```flask db upgrade```

Run Server:

```flask run```

For mobile:

1. Connect your laptop to your phone's mobile hotspot
2. Run ```flask run --host=0.0.0.0``` and use the second link. 

## How to run the tests for the application
Unit Test:

```python unittests.py```

Selenium Test:
1. Run Flask application in a virtual environment
2. In a seperate terminal, create and activate virtual environment. Install the requirements and ```python selenium_test.py```
3. 


## Resource Reference (APA)
Bayer, M. (2012). SQLAlchemy: The Database Toolkit for Python. Retrieved from https://www.sqlalchemy.org

Ecma International. (2011). ECMAScript Language Specification (ECMA-262). Retrieved from https://www.ecma-international.org/publications/standards/Ecma-262.htm

Ronacher, A. (n.d.). Flask. Retrieved from https://flask.palletsprojects.com

Hipp, D. (n.d.). SQLite. Retrieved from https://www.sqlite.org

Otto, M., & Thornton, J. (n.d.). Bootstrap. Retrieved from https://getbootstrap.com

Python. (2019). os — Miscellaneous operating system interfaces — Python 3.8.0 documentation. Python.org. https://docs.python.org/3/library/os.html

Roy, M., & Grinberg, M. (n.d.). Flask-Login. Retrieved from https://flask-login.readthedocs.io/en/latest/

SeleniumHQ. (n.d.). Selenium WebDriver. Retrieved from https://www.selenium.dev

Server Installation | Socket.IO. (2024, April 10). Socket.io. https://socket.io/docs/v3/server-installation/

W3C. (1999). HTML 4.01 Specification. Retrieved from https://www.w3.org/TR/html401/

W3C. (2011). Cascading Style Sheets (CSS) Snapshot 2010. Retrieved from https://www.w3.org/TR/css-2010/

WTForms. (n.d.). WTForms Documentation. Retrieved from https://wtforms.readthedocs.io/en/stable/

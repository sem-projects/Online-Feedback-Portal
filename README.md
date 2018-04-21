# DBMS-Project
Sem 4 DBMS Project

## Online feedback portal is a medium through which students can give feedback to professors based on their teaching, assignments, and other skills. Professors can see these reviews and it will encourage them to understand problems of students better and adapt themselves in a way that is helpful for all.

## Features 
* Student portal for giving ratings and review
* Professor portal for seeing the reviews given by student in a particular subject or in a year etc. He/She can see those ratings in graph format showing a clear picture of how much improvement has been made from before.
* Admin portal where admin can answer to any query asked by Student or Teacher and he/she can edit details of users if necessary.

## Building on your machine

### Setup an environment:
```
git clone https://github.com/arindam-modak/Online-Feedback-Portal.git
cd Online-Feedback-Portal
virtualenv venv
source venv/bin/activate
```
### Installation: 
```
pip install -r requirements.txt
```
### Setting up mail server: 
```
Set app.config['MAIL_USERNAME'] = 'server_gmail_address'
SET app.config['MAIL_PASSWORD'] = 'server_gmail_password'
Make sure in server gmail address, access to less secure apps mode is ON
You may change other SMTP settings in app.py file
python manage.py runserver
```
### Running Project: 
```
python app.py
```

## Contributors:
* Parth Agarwal [xxator](https://github.com/xxator)
* Rishab Agarwal [rishu-12](https://github.com/rishu-12)
* Arindam Das Modak [arindam-modak](https://github.com/arindam-modak)

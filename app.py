from flask import Flask,render_template,redirect, url_for, request
import sqlite3
from datetime import datetime, date
from functools import wraps
from flask import Flask,render_template,redirect, url_for,request,session,flash
import os
import random
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy 
from werkzeug import secure_filename
import json
import tkMessageBox

app = Flask(__name__, static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
app.config['SECRET_KEY'] = "random string"
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://///C:/Users/DELL/new/DBMS-Project/dbms.db'
db = SQLAlchemy(app)

UPLOAD_FOLDER = 'static/upload'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

class courses(db.Model):
	__tablename__ = 'courses'
	column_display_pk = True
	course_code = db.Column(db.String(20), primary_key=True)
	course_name = db.Column(db.String(40))
	credits = db.Column(db.Integer)
	semester = db.Column(db.Integer)
	department = db.Column(db.String(40))

		

class users(db.Model):
	__tablename__ = 'users'
	column_display_pk = True
	email = db.Column(db.String(40),primary_key=True)
	username = db.Column(db.String(40))
	name = db.Column(db.String(50))
	dob = db.Column(db.Date())
	password = db.Column(db.String(50))
	type1 = db.Column(db.String(20))
	semester = db.Column(db.Integer)
	department = db.Column(db.String(30))
	is_active = db.Column(db.Integer)
	secret_key = db.Column(db.Integer)
	image_link = db.Column(db.String(200))

class users_courses(db.Model):
	column_display_pk = True
	S_no = db.Column(db.Integer, primary_key = True, autoincrement=True)
	useremail = db.Column(db.String(40), db.ForeignKey('users.email'))
	course_code = db.Column(db.String(20),db.ForeignKey('courses.course_code'))

class admin(db.Model):
	column_display_pk = True
	username = db.Column(db.String(40), primary_key = True)
	password = db.Column(db.String(40))
	email = db.Column(db.String(40))

class query(db.Model):
	column_display_pk = True
	S_no = db.Column(db.Integer, primary_key = True, autoincrement=True)
	useremail = db.Column(db.String(40), db.ForeignKey('users.email'))
	query = db.Column(db.String(40))
	reply_to_query = db.Column(db.String(40))
	seen = db.Column(db.Integer)
	



class questions(db.Model):
	column_display_pk = True
	S_no = db.Column(db.Integer,primary_key=True, autoincrement=True)
	question_type = db.Column(db.String(30))
	question = db.Column(db.String(200))

class rating(db.Model):
	column_display_pk = True
	r_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
	course_code = db.Column(db.String(30),db.ForeignKey('courses.course_code')) 
	question_id = db.Column(db.Integer,db.ForeignKey('questions.S_no')) 
	faculty_email = db.Column(db.String(50),db.ForeignKey('users.email'))  
	student_email = db.Column(db.String(50),db.ForeignKey('users.email'))
	rating = db.Column(db.Integer)
	date1 = db.Column(db.Date())

class MyRatingView(ModelView):
	column_display_pk = True
	can_create = True
	column_list = ('r_id', 'course_code','question_id','faculty_email','student_email','rating','date1')
	form_columns = ['r_id', 'course_code','question_id','faculty_email','student_email','rating','date1']
	column_filters = ['r_id', 'course_code','question_id','faculty_email','student_email','rating','date1']

class MyCourseView(ModelView):
	column_display_pk = True
	can_create = True
	column_list = ('course_code', 'course_name', 'credits','semester','department')
	form_columns = ['course_code', 'course_name', 'credits','semester','department']
	column_filters = ['course_code', 'course_name', 'credits','semester','department']

class MyUserView(ModelView):
	column_display_pk = True
	can_create = True
	column_list = ('email','username','name','dob','password','type1','semester','department','is_active','secret_key','image_link')
	form_columns = ['email','username','name','dob','password','type1','semester','department','is_active','secret_key','image_link']
	column_filters = ['email','username','name','dob','password','type1','semester','department','is_active','secret_key','image_link']

class MyUserCoursesView(ModelView):
	column_display_pk = True
	can_create = True
	column_list = ('S_no','useremail', 'course_code')
	form_columns = ['S_no','useremail', 'course_code']
	column_filters = ['S_no','useremail', 'course_code']

class MyQueryView(ModelView):
	column_display_pk = True
	can_create = True
	column_list = ('S_no','useremail','query','reply_to_query','seen')
	form_columns = ['S_no','useremail','query','reply_to_query','seen']
	column_filters = ['S_no','useremail','query','reply_to_query','seen']

class MyQuestionView(ModelView):
	column_display_pk = True
	can_create = True
	column_list = ('S_no','question_type','question')
	form_columns = ['S_no','question_type','question']
	column_filters = ['S_no','question_type','question']

'''conn = sqlite3.connect('students.sqlite3')
cur = conn.cursor()
cur.execute("DROP TABLE rating")
conn.commit()'''
adminlog = False
@app.route('/adminlogin', methods=['GET','POST'])
def adminlogin():
	print "hi"
	global adminlog
	if request.method == 'GET':
		return render_template('adminlogin.html')
	if request.method == 'POST':
	    if request.form['password'] == 'password' and request.form['username'] == 'admin':
	        adminlog = True
	        print "auth done.................................."
	        return redirect('http://127.0.0.1:5000/admin')				####change to host
	    else:
	        flash('wrong password!')
	

class MyAdminIndexView(AdminIndexView):
	def is_accessible(self):
		global adminlog
		if adminlog==False:
			return False
		if adminlog==True:
			adminlog=False
			return True


db.create_all()
admin = Admin(app,index_view=MyAdminIndexView())
admin.add_view(MyCourseView(courses,db.session))
admin.add_view(MyUserView(users,db.session))
admin.add_view(MyUserCoursesView(users_courses,db.session))
admin.add_view(MyQueryView(query,db.session))
admin.add_view(MyQuestionView(questions,db.session))
admin.add_view(MyRatingView(rating,db.session))
#list_columns=['r_id','course_code','question_id','faculty_email','student_email','rating']



'''@app.route('/new', methods = ['GET', 'POST'])
def new():
   if request.method == 'POST':
      if not request.form['name'] or not request.form['city'] or not request.form['addr']:
         flash('Please enter all the fields', 'error')
      else:
         student = students(request.form['name'], request.form['city'],
            request.form['addr'], request.form['pin'])
         
         db.session.add(student)
         db.session.commit()
         flash('Record was successfully added')
         return redirect(url_for('show_all'))
   return render_template('new.html')'''


app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'iit2016047@iiita.ac.in'
app.config['MAIL_PASSWORD'] = 'cricketstar'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)


#sqliteAdminBP = sqliteAdminBlueprint(dbPath = 'students.sqlite3')
'''conn = sqlite3.connect('students.sqlite3')
print ("Opened database successfully")

sqliteAdminBP = sqliteAdminBlueprint(dbPath = 'students.sqlite3')
#app.register_blueprint(sqliteAdminBP, url_prefix='/admin')

conn.execute('CREATE TABLE IF NOT EXISTS courses (course_code TEXT primary key,couse_name TEXT, credits INT, department TEXT, semester INT)')
print ("COURSES Table created successfully")

conn.execute('CREATE TABLE IF NOT EXISTS users ( email TEXT primary key, username TEXT,name TEXT, dob DATE, pass TEXT, type TEXT, semester INT,department TEXT,is_active INT,secret_key INT)')
print ("USERS Table created successfully")

conn.execute('CREATE TABLE IF NOT EXISTS users_courses (S_no integer not null primary key AUTOINCREMENT,useremail TEXT,course_code TEXT, foreign key(useremail) references users(email),foreign key (course_code) references courses(course_code))')
print ("USERS_courses Table created successfully")

conn.execute('CREATE TABLE IF NOT EXISTS admin (username TEXT primary key, pass TEXT, email TEXT)')
print ("ADMIN Table created successfully")

conn.execute('CREATE TABLE IF NOT EXISTS query (S_no integer not null primary key AUTOINCREMENT,useremail TEXT,query TEXT,reply_to_query TEXT,seen integer,foreign key (useremail) references users(email))')
print ("QUERY Table created successfully")

conn.execute('CREATE TABLE IF NOT EXISTS questions (question_id TEXT primary key, question_type TEXT, question TEXT)')
print ("QUESTIONS Table created successfully")

conn.execute('CREATE TABLE IF NOT EXISTS question_answer (S_no integer not null primary key AUTOINCREMENT,question_id TEXT, useremail TEXT,foreign key (useremail) references users(email),foreign key (question_id) references questions(question_id))')
print ("QUESTIONS Table created successfully")

conn.execute('CREATE TABLE IF NOT EXISTS rating (r_id integer not null primary key AUTOINCREMENT,course_code TEXT, question_id TEXT, faculty_email TEXT,student_email TEXT,rating INT)')
print ("RATING Table created successfully")
cur = conn.cursor()
cur.execute("SELECT * FROM users")
al = cur.fetchall()
print (al)
cur.execute("SELECT * FROM query")
al = cur.fetchall()
print (al)
conn.close()'''



'''


sqliteAdminBP = sqliteAdminBlueprint(
  dbPath = 'students.sqlite3',
  decorator = do_admin_login
)	
app.register_blueprint(sqliteAdminBP, url_prefix='/admin')'''


current = None
type1 = ""


@app.route('/')
def index():
   return render_template("index.html")


@app.route('/login',methods = ['GET','POST'])
def login():
	message = None
	global current,type1
	if session.get('logged_in'):
		conn = sqlite3.connect('students.sqlite3')
		print ("Opened database successfully")
		curr = conn.cursor()
		curr.execute('SELECT type1 FROM users where email = (?)',(current+"@iiita.ac.in",))
		typeo = curr.fetchone()[0]
		if typeo=="Student":
			return redirect(url_for('dashboard',id = current))
		elif typeo=="Faculty":
			return redirect(url_for('facultydashboard',id = current))

	if request.method == 'GET':
		return render_template("login.html",message = None)
		
	if request.method == 'POST':
		username=request.form.get('username',)
		password=request.form.get('pass',)
		print (username)
		print (password)
		if password == 'password' and username == 'admin':
			session['admin_logged_in'] = True
			return redirect('http://127.0.0.1:5000/admin')						#### change to host url 
		conn = sqlite3.connect('students.sqlite3')
		print ("Opened database successfully")
		curr = conn.cursor()
		#curr.execute("SELECT count(*) FROM users WHERE email = ?", (request.form.get('username',''),))
		curr.execute("SELECT count(*) FROM users WHERE email = (?)",(username,))
		data = curr.fetchone()[0]
		if data ==0:
			print('There is no user%s'%request.form.get('username'))
			message = "PLEASE REGISTER USER DOES NOT EXIST"
		else:
			print('Component %s found in %s row(s)'%(username,data))
			curr.execute("SELECT count(*) FROM users WHERE email = (?) and is_active = (?)",(username,1))
			check = curr.fetchone()[0]
			if check==0:
				return render_template("login.html",message = "Please verify your email first")

			curr.execute("SELECT count(*) FROM users WHERE email = (?) and password = (?) and is_active = (?)",(username,password,1))
			check = curr.fetchall()[0]
			print "the value of ----- :",check[0]
			if check[0] != 0:
				message = "success"
				print ("success")
				user=username.split("@")[0]
				session['logged_in'] = True
				current = user

				curr.execute("SELECT type1 FROM users WHERE email = (?)",(username,))
				user_type=curr.fetchone()[0]
				conn.close()
				if user_type == "Student" :
					type1="Student"
					return redirect(url_for('dashboard',id=user))
				elif user_type == "Faculty" :
					type1 = "Faculty"
					return redirect(url_for('facultydashboard',id=user))
			else:
				return render_template("login.html",message = "INCORRECT PASSWORD")	
		conn.close()
	return render_template("login.html",message = message)
      


@app.route('/register',methods = ['GET','POST'])
def register():
	message = None
	if request.method == 'GET':
		return render_template("student_register.html", message = message)
	if request.method == 'POST':
		nm = request.form.get('name',)
		dob = str(request.form.get('dob',))
		email = request.form.get('email',)
		password=request.form.get('pass',)
		passwordc=request.form.get('passc',)
		if email.split("@")[1] != "iiita.ac.in":
			message="invalid email"
			return render_template("student_register.html", message = message)
		if password != passwordc:
			print ("successf")
			message="password doesn't match"
			return render_template("student_register.html", message = message)
		if password == passwordc:
			print ("success")
			conn = sqlite3.connect('students.sqlite3')
			cur = conn.cursor()
			sub = email[:3].upper()
			user_type = None
			if 	sub == "IIT" or sub == "BIM" or \
				sub == "IBM" or sub == "BIM" or \
				sub == "ICM" or sub == "IHM" or \
				sub == "IIM" or sub == "IRM" or \
				sub == "ISM" or sub == "ITM" or \
				sub == "IWM" or sub == "IEC" or \
				sub == "IMM" or sub == "ECM":
				user_type = "Student"
			else:
				user_type = "Faculty"
			secret = random.randint(1000324312,10000000000123)
			conn = sqlite3.connect('students.sqlite3')
			cur = conn.cursor()
			cur.execute("INSERT INTO USERS (email,username,name,dob,password,type1,is_active,secret_key) values (?,?,?,?,?,?,?,?)",\
				(email,email.split("@")[0],nm,dob,password,user_type,0,secret))	
			conn.commit() 
			conn.close()
			print ("insert into user success")
			msg = Message('Hello', sender = 'iit2016047@iiita.ac.in', recipients = [email])
			msg.body = "Hello confirm your email " + "http://127.0.0.1:5000/emailverify/"+email.split("@")[0]+"/"+str(secret)
			mail.send(msg)
			return redirect(url_for('login'))
	return render_template("student_register.html", message = message)


@app.route('/emailverify/<id>/<key>')
def validemail(id,key):
	conn = sqlite3.connect('students.sqlite3')
	cur = conn.cursor()
	cur.execute("SELECT secret_key FROM users WHERE username = (?)",(id,))
	users = cur.fetchone()[0]
	if users==int(key):
		cur.execute("UPDATE users set is_active = (?) where username = (?)",(1,id))
		conn.commit()
		conn.close()
	return redirect(url_for('login'))

@app.route('/forgotpwdemail',methods=['GET','POST'])
def forgotpwdemail():
	message = None
	mails = None
	if request.method == 'GET':
		return render_template("forgotpwdemail.html", message = message)
	if request.method == 'POST':
		email = request.form.get('mail',)
		if email.split("@")[1] != "iiita.ac.in":
			message="Invalid Email."
			return render_template("forgotpwdemail.html", message = message)
		else:
			mails=[]
			conn = sqlite3.connect('students.sqlite3')
			cur = conn.cursor()
			cur.execute("SELECT count(*) from users where email = (?)",(email,))
			mails = cur.fetchall()[0]
			if mails==[]:
				message="Email does not exist."
				return render_template("forgotpwdemail.html", message = message)
			else:
				secret = random.randint(1000324312,10000000000123)
				cur.execute("UPDATE users set secret_key = (?) where email = (?)",(secret,email,))
				conn.commit() 
				conn.close()
				msg = Message('Hello', sender = 'iit2016047@iiita.ac.in', recipients = [email])
				msg.body = "Click on the given link for changing password " + "http://127.0.0.1:5000/forgotpwd/"+email.split("@")[0]+"/"+str(secret)
				mail.send(msg)
				return redirect(url_for('login'))
	return render_template("forgotpwdemail.html", message = message)

@app.route('/forgotpwd/<id>/<key>',methods=['GET','POST'])
def forgotpwd(id,key):
	message = None
	if request.method == 'GET':
		return render_template("forgotpwd.html", message = message)
	if request.method == 'POST':
		new_pass = request.form.get('new_pass',)
		confirm_pass = request.form.get('confirm_pass',)
		conn = sqlite3.connect('students.sqlite3')
		cur = conn.cursor()
		if new_pass != confirm_pass:
			message="Password does not match."
			return render_template("forgotpwd.html", message = message)
		else:
			cur.execute("UPDATE users set password = (?) where username = (?) and secret_key = (?)",(new_pass,id,key,))
			conn.commit()
			conn.close()
			message="Password changed you can login now."
			return redirect(url_for('login'))
	return render_template("forgotpwd.html", message = message)


@app.route('/admin_course/add',methods=['GET','POST'])
def admin_course_add():
	if request.method=="POST":
		conn = sqlite3.connect('students.sqlite3')
		cur = conn.cursor()
		cur.execute("INSERT into courses values (?,?,?,?,?)",(request.form.get('course_id',),request.form.get('course_name',),int(request.form.get('course_credits',)),int(request.form.get('course_semester',)),request.form.get('course_department',)))
		conn.commit()
		conn.close()
	return render_template("admin_course_add.html")

@app.route('/admin_question/add',methods=['GET','POST'])
def admin_question_add():
	if request.method=="POST":
		conn = sqlite3.connect('students.sqlite3')
		cur = conn.cursor()
		cur.execute("INSERT into questions values (?,?)",(request.form.get('question_type',),request.form.get('question',)))
		conn.commit()
		conn.close()
	return render_template("admin_question_add.html")



@app.route('/dashboard/<id>')
def dashboard(id):
	global current,type1
	if session.get('logged_in') and id == current:
		conn = sqlite3.connect('students.sqlite3')
		cur = conn.cursor()
		cur.execute("SELECT * FROM users WHERE username = (?)",(id,))
		users = cur.fetchone()
		cur.execute("SELECT courses.course_code,courses.course_name,courses.credits,courses.department FROM users_courses,courses WHERE useremail = (?) and users_courses.course_code = courses.course_code",(id+"@iiita.ac.in",))
		courses = cur.fetchall()
		#cur.execute("SELECT * FROM query where username = (?) and reply_to_query = (?)",(id,));
		print (users)
		print (courses)
		cur = conn.cursor()
		cur.execute("SELECT * FROM query WHERE useremail = (?) and seen = (?) and reply_to_query != (?)",(id+"@iiita.ac.in",0,"None",))
		notifications = cur.fetchall()
		if notifications==[]:
			notifications=None
		conn.close()
		return render_template("dashboard.html",type1=type1,users=users,notifications=notifications,courses = courses)
	return redirect(url_for('login'))




@app.route('/facultydashboard/<id>')
def facultydashboard(id):
	global current,type1

	if session.get('logged_in') and id == current:
		conn = sqlite3.connect('students.sqlite3')
		cur = conn.cursor()
		cur.execute("SELECT * FROM users WHERE username = (?)",(id,))
		users = cur.fetchone()
		cur.execute("SELECT courses.course_code,course_name,credits,department FROM users_courses,courses WHERE useremail = (?) and users_courses.course_code = courses.course_code",(id+"@iiita.ac.in",))
		courses = cur.fetchall()
		#cur.execute("SELECT * FROM query where username = (?) and reply_to_query = (?)",(id,));
		print (users)
		print (courses)
		cur = conn.cursor()
		cur.execute("SELECT * FROM query WHERE useremail = (?) and seen = (?) and reply_to_query!=(?)",(id+"@iiita.ac.in",0,"None",))
		notifications = cur.fetchall()
		if notifications==[]:
			notifications=None
		conn.close()
		return render_template("facultydashboard.html",type1=type1,users=users,notifications=notifications,courses = courses)
	return redirect(url_for('login'))


@app.route('/feedbackanalysis',methods=['GET','POST'])
def feedbackanalysis():
	global current,type1
	if session.get('logged_in') :
		conn = sqlite3.connect('students.sqlite3')
		cur = conn.cursor()
		cur2 = conn.cursor()
		cur.execute("SELECT * FROM users WHERE username = (?)",(current,))
		users = cur.fetchone()
		cur.execute("SELECT * FROM query WHERE useremail = (?) and seen = (?) and reply_to_query != (?)",(current+"@iiita.ac.in",0,"None",))
		notifications = cur.fetchall()
		cur.execute("SELECT * FROM users_courses where useremail = (?)",(current+"@iiita.ac.in",))
		subject = cur.fetchall()
		if subject==[]:
			subject=None
		
		sub=None
		message=None
		select_subject=None
		types = ['Overall','Theory']
		data1=None
		data2=None
		graph=None
		year1=None
		graph1=None
		r1 = 0
		r2 = 0
		r3 = 0
		r4 = 0
		r5 = 0
		sub = request.args.get('sub')
		select_subject=sub
		select_type=None
		temp=None
		cur.execute("SELECT * FROM courses where course_code = (?)",(sub,))
		if cur.fetchall()!=[]:
			cur.execute("SELECT * FROM users_courses where useremail = (?)",(current+"@iiita.ac.in",))
			if cur.fetchall()==[]:
				message = "Don't use foul means :p"
			else:
				if sub[-2:-1]!='0':
					types.append('Lab')
				select_subject=sub
		else:
			message = "Don't use foul means :p"
		year = None
		if request.method=="POST":
			graph1=None
			temp=None
			select_type = request.form.get('type1',)
			if select_type=="Overall":
				cur.execute('SELECT avg(rating) as average, strftime((?), date1) as year FROM rating WHERE faculty_email = (?) and course_code=(?) group by year',('%Y',current+"@iiita.ac.in",sub,))
				cur2.execute('SELECT strftime((?), date1) as year FROM rating WHERE faculty_email = (?) and course_code=(?) group by year',('%Y',current+"@iiita.ac.in",sub,))	
			elif select_type=="Lab":
				cur2.execute('SELECT strftime((?), date1) as year FROM rating INNER JOIN questions ON rating.question_id=questions.S_no WHERE faculty_email = (?) and course_code=(?) and question_type=(?) group by year',('%Y',current+"@iiita.ac.in",sub,'Lab',))
				cur.execute('SELECT avg(rating) as average,strftime((?), date1) as year FROM rating INNER JOIN questions ON rating.question_id=questions.S_no WHERE faculty_email = (?) and course_code=(?) and question_type=(?) group by year',('%Y',current+"@iiita.ac.in",sub,'Lab',))
			elif select_type=="Theory":
				cur.execute('SELECT avg(rating) as average,strftime((?), date1) as year FROM rating INNER JOIN questions ON rating.question_id=questions.S_no WHERE faculty_email = (?) and course_code=(?) and question_type!=(?) group by year',('%Y',current+"@iiita.ac.in",sub,'Lab',))
				cur2.execute('SELECT strftime((?), date1) as year FROM rating INNER JOIN questions ON rating.question_id=questions.S_no WHERE faculty_email = (?) and course_code=(?) and question_type!=(?) group by year',('%Y',current+"@iiita.ac.in",sub,'Lab',))
			data = cur.fetchall()
			year = cur2.fetchall()
			print(data)
			data1=[]
			data2=[]
			graph=True
			year1=[]
			temp = request.form.get('year1',)
			if temp!= None:
				graph1 = True
				cur.execute('SELECT count(rating) FROM rating WHERE strftime((?), date1) = (?) and faculty_email = (?) and course_code=(?) and rating = 1',('%Y',temp,current+"@iiita.ac.in",sub,))
				r1 = cur.fetchone()[0]
				cur.execute('SELECT count(rating) FROM rating WHERE strftime((?), date1) = (?) and faculty_email = (?) and course_code=(?) and rating = 2',('%Y',temp,current+"@iiita.ac.in",sub,))
				r2 = cur.fetchone()[0]
				cur.execute('SELECT count(rating) FROM rating WHERE strftime((?), date1) = (?) and faculty_email = (?) and course_code=(?) and rating = 3',('%Y',temp,current+"@iiita.ac.in",sub,))
				r3 = cur.fetchone()[0]
				cur.execute('SELECT count(rating) FROM rating WHERE strftime((?), date1) = (?) and faculty_email = (?) and course_code=(?) and rating = 4',('%Y',temp,current+"@iiita.ac.in",sub,))
				r4 = cur.fetchone()[0]
				cur.execute('SELECT count(rating) FROM rating WHERE strftime((?), date1) = (?) and faculty_email = (?) and course_code=(?) and rating = 5',('%Y',temp,current+"@iiita.ac.in",sub,))
				r5 = cur.fetchone()[0]
				
			print temp,'======='
			for d in data:
				data2.append(d[0])
				data1.append(d[1])
			for y in year:
				year1.append(y[0])
         	
		if notifications==[]:
			notifications=None


		return render_template('facultygraph.html',r1=r1,r2=r2,r3=r3,r4=r4,r5=r5,year = year1,type1=type1,users=users,graph1=graph1,graph=graph,notifications=notifications,data1=json.dumps(data1),data2=json.dumps(data2),types=types,temp=temp,subject=subject,select_type=select_type,select_subject=select_subject,message=message)
	else:
		return redirect(url_for('login'))


@app.route('/profile/<id>',methods = ['GET','POST'])
def profile(id=None):
	global current,type1
	message=None
	img=None
	if session.get('logged_in') :
		if request.method == 'GET':
			conn = sqlite3.connect('students.sqlite3')
			cur = conn.cursor()
			cur.execute("SELECT * FROM users WHERE username = (?)",(current,))
			users = cur.fetchone()
			cur.execute("SELECT * FROM query WHERE useremail = (?) and seen = (?) and reply_to_query != (?)",(current+"@iiita.ac.in",0,'None'))
			notifications = cur.fetchall()
			if notifications==[]:
				notifications=None
			conn.close()
			print(type1)
			return render_template("user.html",type1=type1,users=users,notifications=notifications,message=message)
	
		if request.method == 'POST':
			conn = sqlite3.connect('students.sqlite3')
			cur = conn.cursor()
			nm = request.form.get('name',)
			email=request.form.get('mail',)
			dob = str(request.form.get('dob',))
			sem = request.form.get('sem',)
			depart = request.form.get('depart',)
			file = request.files['file']
			if file.filename == '':
				flash('No selected file')
				return redirect(url_for('profile',id=current))
			if file:
				filename = secure_filename(file.filename)
				file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
				img = "../upload/"+filename
			
			message = "profile editied successfully"
			cur.execute("UPDATE users SET name = (?) , dob = (?) , semester = (?) , department = (?), image_link = (?) WHERE username = (?)",(nm,dob,sem,depart,img,current,))
			conn.commit()
			cur.execute("SELECT * FROM users WHERE username = (?)",(current,))
			users = cur.fetchone()
			cur.execute("SELECT * FROM query WHERE useremail = (?) and seen = (?)",(id+"@iiita.ac.in",0,))
			notifications = cur.fetchall()
			if notifications==[]:
				notifications=None
			conn.close()
			return render_template("user.html",type1=type1,users=users,notifications=notifications,message=message)
	
	return redirect(url_for('login'))

@app.route('/courses',methods = ['GET','POST'])
def courses():
	global current,type1
	course = None 
	if session.get('logged_in'):
		conn = sqlite3.connect('students.sqlite3')
		cur = conn.cursor()
		cur.execute("SELECT * FROM users WHERE username = (?)",(current,))
		users = cur.fetchone()
		cur.execute("SELECT type1 from users where username = (?)",(current,))
		type1 = cur.fetchone()[0]
		cur.execute("SELECT * FROM query WHERE useremail = (?) and seen = (?) and reply_to_query != (?)",(current+"@iiita.ac.in",0,"None",))
		notifications = cur.fetchall()
		if notifications==[]:
			notifications=None
		if type1 == "Student" :
			cur.execute("SELECT semester from users where username = (?)",(current,))
			sem = int(cur.fetchone()[0])
			cur.execute("SELECT course_code,course_name from courses where semester = (?) ",(sem,))
			course = cur.fetchall()
		else :
			cur.execute("SELECT course_code,course_name from courses order by semester ")
			course = cur.fetchall()

		if request.method=="POST":
			for course_c in course:
				if request.form.get(course_c[0],):
					cur.execute("INSERT into users_courses (course_code,useremail) values (?,?)",(course_c[0],current+"@iiita.ac.in"))
					conn.commit()
			return redirect(url_for('dashboard',id=current))
		
		exist = None
		cur.execute("SELECT * FROM users_courses WHERE useremail = (?)",(current+"@iiita.ac.in",))
		users_cour = cur.fetchall()
		if users_cour != []:
			exist = True
		return render_template("courses.html",type1=type1,users=users,courses=course,exist=exist,notifications=notifications)
	return redirect(url_for('login'))




@app.route('/query',methods = ['GET','POST'])
def query():
	global current,type1
	if session.get('logged_in'):
		if request.method == 'GET':
			conn = sqlite3.connect('students.sqlite3')
			cur = conn.cursor()
			cur.execute("SELECT * FROM users WHERE username = (?)",(current,))
			users = cur.fetchone()
			conn.close()
			return render_template("query.html",type1=type1,users=users,message = None)
		if request.method == 'POST':
			conn = sqlite3.connect('students.sqlite3')
			cur = conn.cursor()
			cur.execute("SELECT * FROM users WHERE username = (?)",(current,))
			users = cur.fetchone()
			print ("query post")
			qu = request.form.get('query',)
			print (qu)
			cur.execute("INSERT INTO query (useremail,query,reply_to_query,seen) values (?,?,?,?)",\
				(current+"@iiita.ac.in",qu,"None",0,))
			conn.commit()
			print ("query updated")
			conn.close()
			return render_template("query.html",type1=type1,users=users,message = "Query updated successfully")

	return redirect(url_for('login'))


@app.route('/feedback', methods = ['GET','POST'])
def feedback():
	global current,type1
	if session.get('logged_in'):
		conn = sqlite3.connect('students.sqlite3')
		cur = conn.cursor()
		cur.execute("SELECT * FROM questions")
		questions = cur.fetchall()
		cur.execute("SELECT department FROM users WHERE username = (?)",(current,))
		department = cur.fetchone()[0]
		cur.execute("SELECT * FROM query WHERE useremail = (?) and seen = (?) and reply_to_query!=(?)",(current+"@iiita.ac.in",0,"None",))
		notifications = cur.fetchall()
		if request.method == 'GET' :
			
			if notifications==[]:
				notifications=None
			select_teacher=request.args.get('prof')
			print(select_teacher)
			if select_teacher == None:
				teacher = None
				courses = None
			else:
				teacher = select_teacher
				cur.execute("SELECT course_code from users_courses where useremail = (?)",(select_teacher+"@iiita.ac.in",))
				courses_teacher=cur.fetchall()
				cur.execute("SELECT course_code from users_courses where useremail = (?)",(current+"@iiita.ac.in",))
				courses_student=cur.fetchall()
				courses=[]
				for c in courses_teacher:
					for cour in courses_student:
						if c[0]==cour[0]:
							courses.append(c)

			cur.execute("SELECT * FROM users WHERE type1 = (?) ",('Faculty',))	
			teach = cur.fetchall()
			cur.execute("SELECT course_code from users_courses where useremail = (?)",(current+"@iiita.ac.in",))
			courses_stu=cur.fetchall()
			teachers = []
			for t in teach:
				for c in courses_stu:
					print(00000000000000)
					cur.execute("SELECT * from users_courses where useremail = (?) and course_code = (?)",(t[0],c[0],))
					courses_stu1=cur.fetchall()
					if courses_stu1 != []:

						teachers.append(t)

			return render_template("feedback.html",type1=type1,questions = None,users = current,teachers = teachers,teacher=teacher,courses=courses,notifications=notifications)
			
		elif request.method == "POST":
			if notifications==[]:
				notifications=None
			return redirect(url_for('question',f_id=request.form.get("pid",),s_id=current,c_id=request.form.get("course",)))

		
	return redirect(url_for('login'))



@app.route('/question/<f_id>/<s_id>/<c_id>',methods = ['GET','POST'])
def question(f_id,s_id,c_id):

	global current,type1

	if session.get('logged_in'):
		conn = sqlite3.connect('students.sqlite3')
		cur = conn.cursor()
		cur.execute("SELECT * FROM users WHERE username = (?)",(current,))
		users = cur.fetchone()
		cur.execute("SELECT * from questions")
		questions = cur.fetchall()
		cur.execute("SELECT * FROM query WHERE useremail = (?) and seen = (?) and reply_to_query !=(?)",(s_id+"@iiita.ac.in",0,"None",))
		notifications = cur.fetchall()
		if notifications==[]:
			notifications=None
		if questions==[]:
			assn=None
			theory=None
			lab=None
			classroom=None
		assn=[]
		theory=[]
		lab=[]
		classroom=[]
		if questions !=[]:
			for ques in questions:
				if ques[1]=="Assignment and Quiz":
					assn.append(ques)
				elif ques[1]=="Theory Lecture":
					theory.append(ques)
				elif ques[1]=="Classroom Ability":
					classroom.append(ques)
				elif c_id[-3:-1] == "32" and ques[1]=="Lab":
					lab.append(ques)

		if c_id[-3:-1] == "32":
			lab_occurs=True
		else:
			lab_occurs=None

		if request.method=="POST":
			for q in questions:
				if request.form.get(str(q[0])+"1",):
					cur.execute('INSERT into rating (course_code,question_id,faculty_email,student_email,rating,date1) values (?,?,?,?,?,?)',(c_id,q[0],f_id+"@iiita.ac.in",s_id+"@iiita.ac.in",1,date.today(),));
					conn.commit()
				elif request.form.get(str(q[0])+"2",):
					cur.execute('INSERT into rating (course_code,question_id,faculty_email,student_email,rating,date1) values (?,?,?,?,?,?)',(c_id,q[0],f_id+"@iiita.ac.in",s_id+"@iiita.ac.in",2,date.today(),));
					conn.commit()
				elif request.form.get(str(q[0])+"3",):
					cur.execute('INSERT into rating (course_code,question_id,faculty_email,student_email,rating,date1) values (?,?,?,?,?,?)',(c_id,q[0],f_id+"@iiita.ac.in",s_id+"@iiita.ac.in",3,date.today(),));
					conn.commit()
				elif request.form.get(str(q[0])+"4",):
					cur.execute('INSERT into rating (course_code,question_id,faculty_email,student_email,rating,date1) values (?,?,?,?,?,?)',(c_id,q[0],f_id+"@iiita.ac.in",s_id+"@iiita.ac.in",4,date.today(),));
					conn.commit()
				elif request.form.get(str(q[0])+"5",):
					cur.execute('INSERT into rating (course_code,question_id,faculty_email,student_email,rating,date1) values (?,?,?,?,?,?)',(c_id,q[0],f_id+"@iiita.ac.in",s_id+"@iiita.ac.in",5,date.today(),));
					conn.commit()
			return redirect(url_for('feedback'))
		conn.close()
		return render_template("questions.html",type1=type1,users=users,notifications=notifications,assn=assn,theory=theory,lab=lab,classroom=classroom,lab_occurs=lab_occurs)

	return redirect(url_for('login'))




@app.route('/change_password/<id>',methods = ['GET','POST'])
def change_password(id):
	global current,type1
	message = None
	if session.get('logged_in'):
		if request.method == 'GET':
			conn = sqlite3.connect('students.sqlite3')
			cur = conn.cursor()
			cur.execute("SELECT * FROM users WHERE username = (?)",(current,))
			users = cur.fetchone()
			cur.execute("SELECT * FROM query WHERE useremail = (?) and seen = (?) and reply_to_query != (?)",(id+"@iiita.ac.in",0,"None",))
			notifications = cur.fetchall()
			if notifications==[]:
				notifications=None
			conn.close()
			return render_template("changepwd.html",type1=type1,users=users,notifications=notifications,message=message)
		if request.method=="POST":
			conn = sqlite3.connect('students.sqlite3')
			cur = conn.cursor()
			cur.execute("SELECT * FROM users WHERE username = (?)",(current,))
			users = cur.fetchone()
			cur.execute("SELECT * FROM query WHERE useremail = (?) and seen = (?) and reply_to_query !=(?)",(id+"@iiita.ac.in",0,"None",))
			notifications = cur.fetchall()
			if notifications==[]:
				notifications=None
			cur.execute("SELECT password FROM users WHERE username = (?)",(current,))
			currpass = cur.fetchone()
			old1 = request.form.get("old1",)
			new1 = request.form.get("new1",)
			new2 = request.form.get("new2",)
			print (old1,currpass[0])
			if old1 != currpass[0]:
				message = "Wrong password"
				return render_template("changepwd.html",type1=type1,users=users,notifications=notifications,message=message)
			elif new1!=new2:
				message = "password doesn't match"
				return render_template("changepwd.html",type1=type1,users=users,notifications=notifications,message=message)
			else:
				message = "password changed successfully"
				cur.execute("UPDATE users set password = (?) where username = (?)",(new1,current,))
				conn.commit()
				conn.close()
				return render_template("changepwd.html",type1=type1,users=users,notifications=notifications,message=message)
			

	return redirect(url_for('login'))


@app.route('/notifications')
def notifications():
	global current,type1
	if session.get('logged_in'):
		conn = sqlite3.connect('students.sqlite3')
		cur = conn.cursor()
		cur.execute("SELECT * FROM users WHERE username = (?)",(current,))
		users = cur.fetchone()
		cur.execute("SELECT S_no,query,reply_to_query FROM query WHERE useremail = (?) and seen != (?) and reply_to_query != (?)",(current+"@iiita.ac.in",1,'None',))
		queries_ans = cur.fetchall()
		return render_template("notifications.html",type1=type1,users=users,queries_ans=queries_ans)

	return redirect(url_for('login'))
@app.route('/closenotify/<c_id>')
def closenotify(c_id):
	global current
	if session.get('logged_in'):
		conn = sqlite3.connect('students.sqlite3')
		cur = conn.cursor()
		cur.execute("SELECT * FROM users WHERE username = (?)",(current,))
		users = cur.fetchone()
		cur.execute("SELECT * FROM query WHERE S_no = (?) and useremail = (?) and seen != (?)",(c_id,current+"@iiita.ac.in",1,))
		s_no = cur.fetchall()
		if s_no != []:
			cur.execute("UPDATE query set seen = (?) where S_no = (?)",(1,c_id,))
			conn.commit()
			conn.close()
	return redirect(url_for('notifications')) 

@app.route('/logout')
def logout():
	global current,type1
	if session.get('logged_in'):
		session['logged_in']=False
		current = None
		type1 = ""

	return redirect(url_for('login'))


if __name__ == '__main__':
	app.debug = True
	app.secret_key = os.urandom(12)

	db.create_all()

	app.run(debug = True)
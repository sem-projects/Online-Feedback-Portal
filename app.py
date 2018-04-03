from flask import Flask,render_template,redirect, url_for, request
import sqlite3
from functools import wraps
from flask import Flask,render_template,redirect, url_for,request,session,flash
import os
import random
from flask_sqlite_admin.core import sqliteAdminBlueprint
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__, static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
app.config['SECRET_KEY'] = "random string"
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://///C:/Users/DELL/new/DBMS-Project/dbms.db'
db = SQLAlchemy(app)

class courses(db.Model):
	__tablename__ = 'courses'
	course_code = db.Column(db.String(20), primary_key=True)
	course_name = db.Column(db.String(40))
	credits = db.Column(db.Integer)
	semester = db.Column(db.Integer)
	department = db.Column(db.String(40))

	def __init__(self, course_code, course_name, credits,department,semester):
		self.course_code = course_code
		self.course_name = course_name
		self.credits = credits
		self.semester = semester
		self.department = department
		

class users(db.Model):
	__tablename__ = 'users'
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

	def __init__(self, email,username,name,dob,password,type1,semester,department,is_active,secret_key):
		self.email = email
		self.username = username
		self.name = name
		self.dob = dob
		self.password= password
		self.type1 = type1
		self.semester = semester
		self.department = department
		self.is_active = is_active
		self.secret_key = secret_key

class users_courses(db.Model):
	S_no = db.Column(db.Integer, primary_key = True, autoincrement=True)
	useremail = db.Column(db.String(40), db.ForeignKey('users.email'))
	course_code = db.Column(db.String(20),db.ForeignKey('courses.course_code'))
	def __init__(self,useremail, course_code):
		self.useremail = useremail
		self.course_code = course_code

class admin(db.Model):
	username = db.Column(db.String(40), primary_key = True)
	password = db.Column(db.String(40))
	email = db.Column(db.String(40))
	def __init__(self,username,password,email):
		self.username = username
		self.password = password
		self.email = email

class query(db.Model):
	S_no = db.Column(db.Integer, primary_key = True, autoincrement=True)
	useremail = db.Column(db.String(40), db.ForeignKey('users.email'))
	query = db.Column(db.String(40))
	reply_to_query = db.Column(db.String(40))
	seen = db.Column(db.Integer)
	
	def __init__(self,useremail,query,reply_to_query,seen):
		self.useremail = useremail 
		self.query = query
		self.reply_to_query = reply_to_query
		self.seen = seen



class question(db.Model):
	S_no = db.Column(db.Integer,primary_key=True, autoincrement=True)
	question_type = db.Column(db.String(30))
	question = db.Column(db.String(200))


db.create_all()
admin = Admin(app)
admin.add_view(ModelView(courses,db.session))
admin.add_view(ModelView(users,db.session))
admin.add_view(ModelView(users_courses,db.session))
admin.add_view(ModelView(query,db.session))



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
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'iit2016047@iiita.ac.in'
app.config['MAIL_PASSWORD'] = 'cricketstar'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

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


'''@app.route('/adminlogin', methods=['POST'])
def admin_login():
    if request.form['password'] == 'password' and request.form['username'] == 'admin':
        session['admin_logged_in'] = True
        print "auth done.................................."
        return redirect('http://127.0.0.1:5000/admin')				####change to host
    else:
        flash('wrong password!')


def check_validity(func):
	@wraps(func)
	def decorated_function(*args, **kwargs):
		if request.referrer != "http://127.0.0.1:5000/login" and request.referrer != "http://localhost:5000/login":
			print ("dont be smart")
			return redirect(url_for('login'))
		return func(*args, **kwargs)

	return decorated_function

def do_admin_login(func):
	@wraps(func)
	def decorated_function(*args, **kwargs):
		if not session.get('admin_logged_in'):
			print "decorater called..........................."
			return render_template('adminlogin.html')
		#session['admin_logged_in'] = False
		return func(*args, **kwargs)

	return decorated_function



sqliteAdminBP = sqliteAdminBlueprint(
  dbPath = 'students.sqlite3',
  decorator = do_admin_login
)	
app.register_blueprint(sqliteAdminBP, url_prefix='/admin')'''



current = None
   

@app.route('/')
def index():
   return render_template("index.html")




@app.route('/login',methods = ['GET','POST'])
def login():
	message = None
	global current
	if session.get('logged_in'):
		return redirect(url_for('dashboard',id = current))
	if request.method == 'GET':
		return render_template("login.html",message = None	)
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
			message = "the user does not exists please register"
		if data !=0:
			print('Component %s found in %s row(s)'%(username,data))
			curr.execute("SELECT count(*) FROM users WHERE email = (?) and is_active = (?)",(username,1))
			check = curr.fetchone()[0]
			if check==0:
				return render_template("login.html",message = "Please verify your email first")

			curr.execute("SELECT count(*) FROM users WHERE email = (?) and password = (?) and is_active = (?)",(username,password,1))
			print ("pass2")
			check = curr.fetchone()[0]
			print (check)
			if check != 0:
				message = "success"
				print ("success")
				user=username.split("@")[0]
				session['logged_in'] = True
				current = user
				curr.execute("SELECT type1 FROM users WHERE email = (?)",(username,))
				user_type=curr.fetchone()[0]
				conn.close()
				if user_type == "Student" :
					return redirect(url_for('dashboard',id=user))
				elif user_type == "Faculty" :
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



@app.route('/admin_course/add',methods=['GET','POST'])
def admin_course_add():
	if request.method=="POST":
		conn = sqlite3.connect('students.sqlite3')
		cur = conn.cursor()
		cur.execute("INSERT into courses values (?,?,?,?,?)",(request.form.get('course_id',),request.form.get('course_name',),int(request.form.get('course_credits',)),int(request.form.get('course_semester',)),request.form.get('course_department',)))
		conn.commit()
		conn.close()
	return render_template("admin_course_add.html")


@app.route('/dashboard/<id>')
def dashboard(id):
	global current
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
		cur.execute("SELECT * FROM query WHERE useremail = (?) and seen = (?)",(id+"@iiita.ac.in",0,))
		notifications = cur.fetchall()
		if notifications==[]:
			notifications=None
		conn.close()
		return render_template("dashboard.html",users=users,notifications=notifications,courses = courses)
	return redirect(url_for('login'))




@app.route('/facultydashboard/<id>')
def facultydashboard(id):
	global current

	if session.get('logged_in') and id == current:
		conn = sqlite3.connect('students.sqlite3')
		cur = conn.cursor()
		cur.execute("SELECT * FROM users WHERE username = (?)",(id,))
		users = cur.fetchone()
		cur.execute("SELECT courses.course_code,couse_name,credits,department FROM users_courses,courses WHERE username = (?) and users_courses.course_code = courses.course_code",(id,))
		courses = cur.fetchall()
		#cur.execute("SELECT * FROM query where username = (?) and reply_to_query = (?)",(id,));
		print (users)
		print (courses)
		cur = conn.cursor()
		cur.execute("SELECT * FROM query WHERE useremail = (?) and seen = (?)",(id+"@iiita.ac.in",0,))
		notifications = cur.fetchall()
		if notifications==[]:
			notifications=None
		conn.close()
		return render_template("facultydashboard.html",users=users,notifications=notifications,courses = courses)
	return redirect(url_for('login'))


@app.route('/profile/<id>',methods = ['GET','POST'])
def profile(id):
	global current
	message=None
	if session.get('logged_in') :
		if request.method == 'GET':
			conn = sqlite3.connect('students.sqlite3')
			cur = conn.cursor()
			cur.execute("SELECT * FROM users WHERE username = (?)",(current,))
			users = cur.fetchone()
			cur.execute("SELECT * FROM query WHERE useremail = (?) and seen = (?)",(id+"@iiita.ac.in",0,))
			notifications = cur.fetchall()
			if notifications==[]:
				notifications=None
			conn.close()
			return render_template("user.html",users=users,notifications=notifications,message=message)
	
		if request.method == 'POST':
			conn = sqlite3.connect('students.sqlite3')
			cur = conn.cursor()
			cur.execute("SELECT * FROM users WHERE username = (?)",(current,))
			users = cur.fetchone()
			cur.execute("SELECT * FROM query WHERE useremail = (?) and seen = (?)",(id+"@iiita.ac.in",0,))
			notifications = cur.fetchall()
			if notifications==[]:
				notifications=None
			nm = request.form.get('name',)
			email=request.form.get('mail',)
			dob = str(request.form.get('dob',))
			sem = request.form.get('sem',)
			depart = request.form.get('depart',)
			message = "profile editied successfully"
			cur.execute("UPDATE users SET name = (?) , dob = (?) , semester = (?) , department = (?) WHERE username = (?)",(nm,dob,sem,depart,current,))
			conn.commit()
			conn.close()
			return render_template("user.html",users=users,notifications=notifications,message=message)
	
	return redirect(url_for('login'))

@app.route('/courses',methods = ['GET','POST'])
def courses():
	global currrent
	course = None 
	if session.get('logged_in'):

		if request.method=="POST":
			pass

		conn = sqlite3.connect('students.sqlite3')
		cur = conn.cursor()
		cur.execute("SELECT * FROM users WHERE username = (?)",(current,))
		users = cur.fetchone()
		cur.execute("SELECT type1 from users where username = (?)",(current,))
		type1 = cur.fetchone()[0]
		cur.execute("SELECT semester from users where username = (?)",(current,))
		sem = int(cur.fetchone()[0])
		if type1 == "Student" :
			cur.execute("SELECT course_code,course_name from courses where semester = (?) ",(sem,))
			course = cur.fetchall()
		else :
			cur.execute("SELECT course_code,course_name from courses order by semester ")
			course = cur.fetchall()
		return render_template("courses.html",users=users,courses=course)
	return redirect(url_for('login'))




@app.route('/query',methods = ['GET','POST'])
def query():
	global current
	if session.get('logged_in'):
		if request.method == 'GET':
			conn = sqlite3.connect('students.sqlite3')
			cur = conn.cursor()
			cur.execute("SELECT * FROM users WHERE username = (?)",(current,))
			users = cur.fetchone()
			conn.close()
			return render_template("query.html",users=users,message = None)
		if request.method == 'POST':
			conn = sqlite3.connect('students.sqlite3')
			cur = conn.cursor()
			cur.execute("SELECT * FROM users WHERE username = (?)",(current,))
			users = cur.fetchone()
			print ("query post")
			qu = request.form.get('query',)
			print (qu)
			cur.execute("INSERT INTO query (useremail,query,reply_to_query,seen) values (?,?,?,?)",\
				(current+"@iiita.ac.in",qu,None,0,))
			conn.commit()
			print ("query updated")
			conn.close()
			return render_template("query.html",users=users,message = "Query updated successfully")

	return redirect(url_for('login'))


@app.route('/feedback/pid', methods = ['GET','POST'])
def feedback(pid=None):
	global current
	if session.get('logged_in'):
		if request.method == 'GET' :
			conn = sqlite3.connect('students.sqlite3')
			cur = conn.cursor()
			cur.execute("SELECT * FROM questions")
			questions = cur.fetchall()
			cur.execute("SELECT * FROM query WHERE useremail = (?) and seen = (?)",(current+"@iiita.ac.in",0,))
			notifications = cur.fetchall()
			if notifications==[]:
				notifications=None
			
			if pid == None:
				cur.execute("SELECT * FROM users WHERE type = (?)",('Faculty',))	
				teachers = cur
				return render_template("feedback.html",questions = None,users = current,teachers = teachers)

		if request.method == 'POST' :
			conn = sqlite3.connect('students.sqlite3')
			cur = conn.cursor()
			cur.execute("SELECT * FROM questions")
			questions = cur.fetchall()
			cur.execute("SELECT * FROM query WHERE useremail = (?) and seen = (?)",(current+"@iiita.ac.in",0,))
			notifications = cur.fetchall()
			if notifications==[]:
				notifications=None
			faculty = request.form.get('facultyname',)
			return render_template("questions.html",questions = questions,users = current , techers = teachers)
	return redirect(url_for('login'))




@app.route('/question/<id>')
def question(id):
	global current

	if session.get('logged_in'):
		conn = sqlite3.connect('students.sqlite3')
		cur = conn.cursor()
		cur.execute("SELECT * FROM users WHERE username = (?)",(current,))
		users = cur.fetchone()
		cur.execute("SELECT * FROM query WHERE useremail = (?) and seen = (?)",(id+"@iiita.ac.in",0,))
		notifications = cur.fetchall()
		if notifications==[]:
			notifications=None
		conn.close()
		return render_template("questions.html",qu=id,users=users,notifications=notifications)

	return redirect(url_for('login'))




@app.route('/change_password/<id>',methods = ['GET','POST'])
def change_password(id):
	global current
	message = None
	if session.get('logged_in'):
		if request.method == 'GET':
			conn = sqlite3.connect('students.sqlite3')
			cur = conn.cursor()
			cur.execute("SELECT * FROM users WHERE username = (?)",(current,))
			users = cur.fetchone()
			cur.execute("SELECT * FROM query WHERE useremail = (?) and seen = (?)",(id+"@iiita.ac.in",0,))
			notifications = cur.fetchall()
			if notifications==[]:
				notifications=None
			conn.close()
			return render_template("changepwd.html",users=users,notifications=notifications,message=message)
		if request.method=="POST":
			conn = sqlite3.connect('students.sqlite3')
			cur = conn.cursor()
			cur.execute("SELECT * FROM users WHERE username = (?)",(current,))
			users = cur.fetchone()
			cur.execute("SELECT * FROM query WHERE useremail = (?) and seen = (?)",(id+"@iiita.ac.in",0,))
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
				return render_template("changepwd.html",users=users,notifications=notifications,message=message)
			elif new1!=new2:
				message = "password doesn't match"
				return render_template("changepwd.html",users=users,notifications=notifications,message=message)
			else:
				message = "password changed successfully"
				cur.execute("UPDATE users set password = (?) where username = (?)",(new1,current,))
				conn.commit()
				conn.close()
				return render_template("changepwd.html",users=users,notifications=notifications,message=message)
			

	return redirect(url_for('login'))


@app.route('/notifications')
def notifications():
	global current
	if session.get('logged_in'):
		conn = sqlite3.connect('students.sqlite3')
		cur = conn.cursor()
		cur.execute("SELECT * FROM users WHERE username = (?)",(current,))
		users = cur.fetchone()
		cur.execute("UPDATE query SET seen = (?) WHERE useremail = (?) and seen = (?)",(1,current+"@iiita.ac.in",0,))
		conn.commit()
		conn.close()
		return render_template("notifications.html",users=users)

	return redirect(url_for('login'))



@app.route('/logout')
def logout():
	if session.get('logged_in'):
		session['logged_in']=False

	return redirect(url_for('login'))


if __name__ == '__main__':
	app.debug = True
	app.secret_key = os.urandom(12)

	db.create_all()

	app.run(debug = True)
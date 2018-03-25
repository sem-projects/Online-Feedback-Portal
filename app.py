from flask import Flask,render_template,redirect, url_for, request
import sqlite3
from functools import wraps
from flask import Flask,render_template,redirect, url_for,request,session,flash
import os
from flask_sqlite_admin.core import sqliteAdminBlueprint


app = Flask(__name__, static_url_path='/static')


conn = sqlite3.connect('database.db')
print ("Opened database successfully")

sqliteAdminBP = sqliteAdminBlueprint(dbPath = 'database.db')
#app.register_blueprint(sqliteAdminBP, url_prefix='/admin')

conn.execute('CREATE TABLE IF NOT EXISTS users ( email TEXT primary key, username TEXT,name TEXT, dob DATE, pass TEXT, type TEXT)')
print ("USERS Table created successfully")

conn.execute('CREATE TABLE IF NOT EXISTS users_courses (S_no integer not null primary key AUTOINCREMENT,username TEXT,course_code TEXT)')
print ("USERS_courses Table created successfully")

conn.execute('CREATE TABLE IF NOT EXISTS admin (email TEXT primary key, pass TEXT)')
print ("ADMIN Table created successfully")

conn.execute('CREATE TABLE IF NOT EXISTS courses (S_no integer not null primary key AUTOINCREMENT,course_code TEXT,couse_name TEXT, credits INT, department TEXT)')
print ("COURSES Table created successfully")

conn.execute('CREATE TABLE IF NOT EXISTS query (S_no integer not null primary key AUTOINCREMENT,username TEXT,query TEXT,reply_to_query TEXT,seen integer)')
print ("QUERY Table created successfully")

conn.execute('CREATE TABLE IF NOT EXISTS questions (question_id TEXT primary key, question_type TEXT, question TEXT)')
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
conn.close()


@app.route('/adminlogin', methods=['POST'])
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
  dbPath = 'database.db',
  decorator = do_admin_login
)	
app.register_blueprint(sqliteAdminBP, url_prefix='/admin')



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
		conn = sqlite3.connect('database.db')
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
			curr.execute("SELECT count(*) FROM users WHERE email = (?) and pass = (?)",(username,password,))
			print ("pass2")
			check = curr.fetchone()[0]
			print (check)
			if check != 0:
				message = "success"
				print ("success")
				user=username.split("@")[0]
				session['logged_in'] = True
				current = user
				conn.close()
				return redirect(url_for('dashboard',id=user))
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
			conn = sqlite3.connect('database.db')
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
			cur.execute("INSERT INTO USERS (email,username,name,dob,pass,type) values (?,?,?,?,?,?)",\
				(email,email.split("@")[0],nm,dob,password,user_type,))	
			print ("insert into user success")
			conn.commit() 
			conn.close()
			return redirect(url_for('login'))
	return render_template("student_register.html", message = message)


@app.route('/dashboard/<id>')
def dashboard(id):
	global current
	if session.get('logged_in') and id == current:
		conn = sqlite3.connect('database.db')
		cur = conn.cursor()
		cur.execute("SELECT * FROM users WHERE username = (?)",(id,))
		users = cur.fetchone()
		cur.execute("SELECT courses.course_code,couse_name,credits,department FROM users_courses,courses WHERE username = (?) and users_courses.course_code = courses.course_code",(id,))
		courses = cur.fetchall()
		#cur.execute("SELECT * FROM query where username = (?) and reply_to_query = (?)",(id,));
		print users
		print courses
		cur = conn.cursor()
		cur.execute("SELECT * FROM query WHERE username = (?) and seen = (?)",(id,0,))
		notifications = cur.fetchall()
		if notifications==[]:
			notifications=None
		conn.close()
		return render_template("dashboard.html",users=users,notifications=notifications,courses = courses)
	return redirect(url_for('login'))



@app.route('/profile/<id>')
def profile(id):
	global current
	if session.get('logged_in') and id == current:
		conn = sqlite3.connect('database.db')
		cur = conn.cursor()
		cur.execute("SELECT * FROM users WHERE username = (?)",(id,))
		users = cur.fetchone()
		cur.execute("SELECT * FROM query WHERE username = (?) and seen = (?)",(id,0,))
		notifications = cur.fetchall()
		if notifications==[]:
			notifications=None
		conn.close()
		return render_template("user.html",users=users,notifications=notifications)
	return redirect(url_for('login'))


@app.route('/query',methods = ['GET','POST'])
def query():
	global current
	if session.get('logged_in'):
		if request.method == 'GET':
			conn = sqlite3.connect('database.db')
			cur = conn.cursor()
			cur.execute("SELECT * FROM users WHERE username = (?)",(current,))
			users = cur.fetchone()
			conn.close()
			return render_template("query.html",users=users,message = None)
		if request.method == 'POST':
			conn = sqlite3.connect('database.db')
			cur = conn.cursor()
			cur.execute("SELECT * FROM users WHERE username = (?)",(current,))
			users = cur.fetchone()
			print "query post"
			qu = request.form.get('query',)
			print qu
			cur.execute("INSERT INTO query (username,query,reply_to_query,seen) values (?,?,?,?)",\
				(current,qu,None,0,))
			conn.commit()
			print "query updated"
			conn.close()
			return render_template("query.html",users=users,message = "Query updated successfully")

	return redirect(url_for('login'))


@app.route('/feedback')
def feedback():
	global current
	if session.get('logged_in'):
		conn = sqlite3.connect('database.db')
		cur = conn.cursor()
		cur.execute("SELECT * FROM users WHERE username = (?)",(current,))
		users = cur.fetchone()
		cur.execute("SELECT * FROM query WHERE username = (?) and seen = (?)",(id,0,))
		notifications = cur.fetchall()
		if notifications==[]:
			notifications=None
		conn.close()
		return redirect(url_for('question',qu=1,users=users,notifications=notifications))

	return redirect(url_for('login'))


@app.route('/question/<id>')
def question(id):
	global current

	if session.get('logged_in'):
		conn = sqlite3.connect('database.db')
		cur = conn.cursor()
		cur.execute("SELECT * FROM users WHERE username = (?)",(current,))
		users = cur.fetchone()
		cur.execute("SELECT * FROM query WHERE username = (?) and seen = (?)",(id,0,))
		notifications = cur.fetchall()
		if notifications==[]:
			notifications=None
		conn.close()
		return render_template("questions.html",qu=id,users=users,notifications=notifications)

	return redirect(url_for('login'))


@app.route('/change_password')
def change_password():
	global current
	if session.get('logged_in'):
		conn = sqlite3.connect('database.db')
		cur = conn.cursor()
		cur.execute("SELECT * FROM users WHERE username = (?)",(current,))
		users = cur.fetchone()
		cur.execute("SELECT * FROM query WHERE username = (?) and seen = (?)",(id,0,))
		notifications = cur.fetchall()
		if notifications==[]:
			notifications=None
		conn.close()
		return render_template("changepwd.html",users=users,notifications=notifications)

	return redirect(url_for('login'))


@app.route('/notifications')
def notifications():
	global current
	if session.get('logged_in'):
		conn = sqlite3.connect('database.db')
		cur = conn.cursor()
		cur.execute("SELECT * FROM users WHERE username = (?)",(current,))
		users = cur.fetchone()
		cur.execute("UPDATE query SET seen = (?) WHERE username = (?) and seen = (?)",(1,current,0,))
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
	app.run()
	app.run(debug = True)	
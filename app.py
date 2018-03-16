from flask import Flask,render_template,redirect, url_for, request
import sqlite3
from functools import wraps
from flask import Flask,render_template,redirect, url_for,request
from flask_sqlite_admin.core import sqliteAdminBlueprint
app = Flask(__name__, static_url_path='/static')


conn = sqlite3.connect('database.db')
print ("Opened database successfully")

sqliteAdminBP = sqliteAdminBlueprint(dbPath = 'database.db')
app.register_blueprint(sqliteAdminBP, url_prefix='/database')

conn.execute('CREATE TABLE IF NOT EXISTS users ( email TEXT primary key,name TEXT, dob DATE, pass TEXT, type TEXT)')
print ("USERS Table created successfully")

conn.execute('CREATE TABLE IF NOT EXISTS admin (email TEXT primary key, pass TEXT)')
print ("ADMIN Table created successfully")

conn.execute('CREATE TABLE IF NOT EXISTS courses (code TEXT primary key, credits INT, department TEXT)')
print ("COURSES Table created successfully")

conn.execute('CREATE TABLE IF NOT EXISTS query_feedback (faculty_email TEXT,student_email TEXT, course_code TEXT,feedback TEXT, query TEXT,reply_to_query TEXT)')
print ("QUERY_FEEDBACK Table created successfully")

conn.execute('CREATE TABLE IF NOT EXISTS questions (question TEXT)')
print ("QUESTIONS Table created successfully")

conn.execute('CREATE TABLE IF NOT EXISTS rating (course_code TEXT, question TEXT, faculty_email TEXT,student_email TEXT,rating INT)')
print ("RATING Table created successfully")
cur = conn.cursor()
cur.execute("SELECT * FROM users")
al = cur.fetchall()
print (al)
conn.close()

def check_validity(func):
	@wraps(func)
	def decorated_function(*args, **kwargs):
		if request.referrer != "http://127.0.0.1:5000/login" and request.referrer != "http://localhost:5000/login":
			print ("dont be smart")
			return redirect(url_for('login'))
		return func(*args, **kwargs)

	return decorated_function

@app.route('/')
def index():
   return render_template("index.html")

@app.route('/login',methods = ['GET','POST'])
def login():
	message = None
	if request.method == 'GET':
		return render_template("login.html",message = None	)
	if request.method == 'POST':
		username=request.form.get('username',)
		password=request.form.get('pass',)
		print username
		print password
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
        		return redirect(url_for('dashboard',id=user))	
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
			cur.execute("INSERT INTO USERS (email,name,dob,pass,type) values (?,?,?,?,?)",\
				(email,nm,dob,password,user_type,))	
			print ("insert into user success")
			conn.commit() 
			conn.close()
			return redirect(url_for('login'))
	return render_template("student_register.html", message = message)


@app.route('/dashboard/id')
@check_validity
def dashboard():
	print ("dashboard")
	return render_template("userdash.html")




if __name__ == '__main__':
	app.debug = True
	app.run()
	app.run(debug = True)	
from flask import Flask,render_template,redirect, url_for, request
import sqlite3
from flask import Flask,render_template,redirect, url_for,request
app = Flask(__name__, static_url_path='/static')


conn = sqlite3.connect('database.db')
print ("Opened database successfully")

conn.execute('CREATE TABLE IF NOT EXISTS users (name TEXT, dob DATE, email TEXT, pass TEXT)')
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
conn.close()


@app.route('/')
def index():
   return redirect(url_for('login'))

@app.route('/login',methods = ['GET','POST'])
def login():
	message = None
	if request.method == 'GET':
		return render_template("login.html",message = None	)
	if request.method == 'POST':
		username=request.form.get('username','')
		password=request.form.get('pass','')
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
        	check = curr.fetchone()[0]
        	if check != 0:
        		print ("success")
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
		if password != passwordc:
			print ("successf")
			message="password doesn't match"
			return render_template("student_register.html", message = message)
        if password == passwordc:
			print ("success")
			conn = sqlite3.connect('database.db')
			cur = conn.cursor()
			cur.execute("INSERT INTO USERS (name,dob,email,pass) values (?,?,?,?)",\
				(nm,dob,email,password,))	
			print ("insert into user success")
			conn.commit() 
			conn.close()
			return redirect(url_for('login'))
	return render_template("student_register.html", message = message)

@app.route('/dashboard/<id>')
def dashboard(id):
	return ("login")




if __name__ == '__main__':
	app.debug = True
	app.run()
	app.run(debug = True)
from flask import Flask,render_template,redirect, url_for, request
import sqlite3
from flask import Flask,render_template,redirect, url_for,request
app = Flask(__name__, static_url_path='/static')


conn = sqlite3.connect('database.db')
print ("Opened database successfully")

conn.execute('CREATE TABLE IF NOT EXISTS users (name TEXT, dob DATE, email TEXT, pass TEXT)')
print ("USERS Table created successfully")

conn.execute('CREATE TABLE IF NOT EXISTS admin (email TEXT, pass TEXT)')
print ("ADMIN Table created successfully")

conn.execute('CREATE TABLE IF NOT EXISTS courses (code TEXT, credits INT, department TEXT)')
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
	if request.method == 'POST':
		username=request.form['username']
		password=request.form['pass']
	return render_template("login.html")
      


@app.route('/register',methods = ['GET','POST'])
def register():
	message = None
	if request.method == 'POST':
		nm = request.form.get('name','')
		dob = str(request.form.get('dob',''))
		email = request.form.get('email','')
		password=request.form.get('pass','')
		passwordc=request.form.get('passc','')
		if password != passwordc:
			message="password doesn't match"
			return render_template("student_register.html", message = message)
        else:
        	conn = sqlite3.connect('database.db')
        	cur = conn.cursor()
        	cur.execute("INSERT INTO USERS (name,dob,email,pass) values (?,?,?,?)",(request.form.get('name',''),str(request.form.get('dob','')),request.form.get('email',''),request.form.get('password')))
        #	
        #	print ("insert into user success")
        #	conn.close()
        #	return redirect(url_for('login'))	
	return render_template("student_register.html", message = message)


@app.route('/dashboard/<id>')
def dashboard(id):
	return ("login")




if __name__ == '__main__':
	#app.debug = True
	app.run()
	#app.run(debug = True)
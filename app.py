from flask import Flask,render_template,redirect, url_for, request
import sqlite3
from flask import Flask,render_template,redirect, url_for,request
app = Flask(__name__, static_url_path='/static')


conn = sqlite3.connect('database.db')
print ("Opened database successfully")

conn.execute('CREATE TABLE IF NOT EXISTS students (name TEXT, addr TEXT, city TEXT, pin TEXT)')
print ("Table created successfully")
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
      


@app.route('/register')
def register():
	return render_template("student_register.html")


@app.route('/dashboard/<id>')
def dashboard(id):
	return ("login")



if __name__ == '__main__':
	app.debug = True
	app.run()
	app.run(debug = True)
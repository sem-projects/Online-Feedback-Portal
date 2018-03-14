<<<<<<< HEAD
from flask import Flask,render_template,redirect, url_for, request
import sqlite3
=======
from flask import Flask,render_template,redirect, url_for,request
>>>>>>> 9905a7b5a4ff0136271915c6d4fa784906f27c05
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
<<<<<<< HEAD

	if request.method == 'POST':
		username=request.form['username']
		password=request.form['pass']
		
=======
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
>>>>>>> 9905a7b5a4ff0136271915c6d4fa784906f27c05
	return render_template("login.html")
      


@app.route('/register')
def register():
	return ("login")


@app.route('/dashboard/<id>')
def dashboard(id):
	return ("login")



if __name__ == '__main__':
	app.debug = True
	app.run()
	app.run(debug = True)
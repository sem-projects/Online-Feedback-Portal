from flask import Flask,render_template,redirect, url_for,request
app = Flask(__name__, static_url_path='/static')

@app.route('/')
def index():
   return redirect(url_for('login'))

@app.route('/login',methods = ['GET','POST'])
def login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
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
from flask import Flask,render_template,redirect, url_for
app = Flask(__name__, static_url_path='/static')

@app.route('/')
def index():
   return redirect(url_for('login'))

@app.route('/login')
def login():
	return render_template("index.html")


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
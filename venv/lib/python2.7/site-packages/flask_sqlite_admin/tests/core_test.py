import unittest
import os
import tempfile
from flask import Flask, make_response, redirect, url_for, request
from core import sqliteAdminBlueprint
import sqlite3
from functools import wraps


db_file = tempfile.mkstemp()

class flask_test_app:
	""" basic app setup """
	app = Flask(__name__)
	
	@app.route('/')
	def index():
		return "hello world"

	bpTest = sqliteAdminBlueprint(bpName = 'sqliteTest',dbPath=db_file[1])
	app.register_blueprint(bpTest, url_prefix='/sqlite')		
		
class testSQLiteBlueprint(unittest.TestCase):
	""" test basic blueprint functionality """
	
	def setUp(self):
		self.db_fd, flask_test_app.app.config['DATABASE'] = db_file
		flask_test_app.app.config['TESTING'] = True
		self.app = flask_test_app.app.test_client()		
		self.con = sqlite3.connect(flask_test_app.app.config['DATABASE'])
		self.con.execute('CREATE TABLE company( id integer PRIMARY KEY autoincrement, name TEXT NOT NULL, age integer NOT NULL, address CHAR(50), salary REAL );')
		self.con.execute('CREATE TABLE department(dept CHAR(50) NOT NULL, emp_id INT NOT NULL );')

	def tearDown(self):
		os.unlink(flask_test_app.app.config['DATABASE'])
		
	def test_index_page(self):
		rv = self.app.get('/')
		assert "hello world" in rv.data
		
	def test_base_page(self):
		rv = self.app.get('/sqlite/')
		assert '<h1>sqlite Admin</h1>' in rv.data
		
	def test_api_get_table(self):
		rv = self.app.get('/sqlite/api?table=company&sort=&dir=asc&offset=0')
		assert '<input class="form-control state-add" name="name"></input>' in rv.data
		assert '<input class="form-control state-add" name="salary"></input>' in rv.data
		
	def test_api_get_invalid_table(self):
		with self.assertRaises(Exception) as cm:
			rv = self.app.get('/sqlite/api?table=test&sort=&dir=asc&offset=0')
		self.assertEqual('invalid table `test`',str(cm.exception) )

	def test_api_get_invalid_no_primary_key(self):
		with self.assertRaises(Exception) as cm:
			rv = self.app.get('/sqlite/api?table=department&sort=&dir=asc&offset=0')
		self.assertEqual('No primary key for first column in table `department`',str(cm.exception) )	
		
	def test_api_add_row(self):
		rv = self.app.post('/sqlite/api',data={"action": "add", "table": "company", "address": "1469 Beverly Glen", "age": "23", "name": "testee mc test", "primaryKey": "id", "salary": "0"})
		self.assertEqual('{"status": 1, "message": "<a href="" class="alert-link">Refresh Page</a>"}',rv.data.replace('\\',""))
		
		rv = self.app.get('/sqlite/api?table=company&sort=&dir=asc&offset=0')
		assert '<span class="state-rest">testee mc test</span>' in rv.data
		assert '<span class="state-rest">1469 Beverly Glen</span>' in rv.data
		
	def test_api_add_row_invalid_table(self):
		rv = self.app.post('/sqlite/api',data={"action": "add", "table": "test", "address": "1469 Beverly Glen", "age": "23", "name": "testee mc test", "primaryKey": "id", "salary": "0"})
		self.assertEqual('{"status": 0, "error": "invalid table `test`"}',rv.data.replace('\\',""))
				
	def test_api_add_row_invalid_column(self):
		rv = self.app.post('/sqlite/api',data={"action": "add", "table": "company", "test": "1469 Beverly Glen", "age": "23", "name": "testee mc test", "primaryKey": "id", "salary": "0"})
		self.assertEqual('{"status": 0, "error": "table company has no column named test"}',rv.data.replace('\\',""))
		
	def test_api_add_row_invalid_no_primary_key(self):
		rv = self.app.post('/sqlite/api',data={"action": "add", "table": "department", "dept": "dinosaurs", "emp_id": "23"})
		self.assertEqual('{"status": 0, "error": "primaryKey"}',rv.data.replace('\\',""))

	def test_api_edit_row(self):
		self.test_api_add_row()
		
		rv = self.app.post('/sqlite/api',data={"action": "edit", "table": "company","id":"1", "address": "1123 East Marlow Street", "age": "23", "name": "testee mc test", "primaryKey": "id", "salary": "0"})
		self.assertEqual('{"status": 1, "message": ""}',rv.data.replace('\\',""))
		
		rv = self.app.get('/sqlite/api?table=company&sort=&dir=asc&offset=0')
		assert '<span class="state-rest">1123 East Marlow Street' in rv.data
		
	def test_api_edit_row_invalid_no_id(self):
		rv = self.app.post('/sqlite/api',data={"action": "edit", "table": "company", "address": "1123 East Marlow Street", "age": "23", "name": "testee mc test", "primaryKey": "id", "salary": "0"})
		self.assertEqual('{"status": 0, "error": "Request must include an id"}',rv.data.replace('\\',""))
		
	def test_api_edit_row_invalid_table(self):
		rv = self.app.post('/sqlite/api',data={"action": "edit", "table": "test", "id":"1", "address": "1123 East Marlow Street", "age": "23", "name": "testee mc test", "primaryKey": "id", "salary": "0"})
		self.assertEqual('{"status": 0, "error": "invalid table `test`"}',rv.data.replace('\\',""))
		
	def test_api_edit_row_invalid_column(self):
		rv = self.app.post('/sqlite/api',data={"action": "edit", "table": "company","id":"1", "test": "1123 East Marlow Street", "age": "23", "name": "testee mc test", "primaryKey": "id", "salary": "0"})
		self.assertEqual('{"status": 0, "error": "no such column: test"}',rv.data.replace('\\',""))
		
	def test_api_edit_row_invalid_no_primary_key(self):
		rv = self.app.post('/sqlite/api',data={"action": "edit", "table": "company","id":"1", "address": "1123 East Marlow Street", "age": "23", "name": "testee mc test", "salary": "0"})
		self.assertEqual('{"status": 0, "error": "primaryKey"}',rv.data.replace('\\',""))
		
	def test_api_delete_row(self):
		self.test_api_add_row()

		rv = self.app.get('/sqlite/api?table=company&sort=&dir=asc&offset=0')
		assert '<span class="state-rest">1469 Beverly Glen' in rv.data
		
		rv = self.app.post('/sqlite/api',data={"action": "delete", "table": "company","id":"1", "address": "1469 Beverly Glen", "age": "23", "name": "testee mc test", "primaryKey": "id", "salary": "0"})
		self.assertEqual('{"status": 1, "message": "Row deleted"}',rv.data.replace('\\',""))

		rv = self.app.get('/sqlite/api?table=company&sort=&dir=asc&offset=0')
		assert '<span class="state-rest">1469 Beverly Glen' not in rv.data

	def test_api_delete_row_invalid_table(self):
		rv = self.app.post('/sqlite/api',data={"action": "delete", "table": "test", "id":"1", "address": "1123 East Marlow Street", "age": "23", "name": "testee mc test", "primaryKey": "id", "salary": "0"})
		self.assertEqual('{"status": 0, "error": "invalid table `test`"}',rv.data.replace('\\',""))

	def test_api_edit_row_invalid_no_id(self):
		rv = self.app.post('/sqlite/api',data={"action": "edit", "table": "company", "address": "1123 East Marlow Street", "age": "23", "name": "testee mc test", "primaryKey": "id", "salary": "0"})
		self.assertEqual('{"status": 0, "error": "Request must include an id"}',rv.data.replace('\\',""))
		
	def test_api_delete_row_invalid_no_primary_key(self):
		rv = self.app.post('/sqlite/api',data={"action": "delete", "table": "company","id":"1", "address": "1123 East Marlow Street", "age": "23", "name": "testee mc test", "salary": "0"})
		self.assertEqual('{"status": 0, "error": "primaryKey"}',rv.data.replace('\\',""))


class flask_test_app_extra_rules:
	""" app setup with extra rules and a decorator """
	
	app = Flask(__name__)
	
	@app.route('/')
	def index():
		return "hello world"
		
	def ruleTest1(self):
		if 'name' in self.colData['name'] and self.value != 'Bob Barker':
			raise ValueError('This is not Bob Barker!')

	def ruleTest2(self):
		if 'address' in self.colData['name'] and 'Beverly Glen' not in self.value:
			raise ValueError('You cant live here!')

	bpTest = sqliteAdminBlueprint(bpName = 'sqliteTest',dbPath=db_file[1],extraRules=[ruleTest1,ruleTest2])
	app.register_blueprint(bpTest, url_prefix='/sqlite')		

class testSQLiteBlueprintExtraRules(unittest.TestCase):
	""" test blueprint when extra rules are passed """
	
	def setUp(self):
		self.db_fd, flask_test_app_extra_rules.app.config['DATABASE'] = db_file
		flask_test_app_extra_rules.app.config['TESTING'] = True
		self.app = flask_test_app_extra_rules.app.test_client()		
		self.con = sqlite3.connect(flask_test_app_extra_rules.app.config['DATABASE'])
		self.con.execute('CREATE TABLE company( id integer PRIMARY KEY autoincrement, name TEXT NOT NULL, age integer NOT NULL, address CHAR(50), salary REAL );')

	def tearDown(self):
		os.unlink(flask_test_app_extra_rules.app.config['DATABASE'])
		
	def test_index_page(self):
		rv = self.app.get('/')
		assert "hello world" in rv.data
		
	def test_base_page(self):
		rv = self.app.get('/sqlite/')
		assert '<h1>sqlite Admin</h1>' in rv.data
		
	def test_api_get_table(self):
		rv = self.app.get('/sqlite/api?table=company&sort=&dir=asc&offset=0')
		assert '<input class="form-control state-add" name="name"></input>' in rv.data
		assert '<input class="form-control state-add" name="salary"></input>' in rv.data
		
	def test_api_add_row_pass(self):
		rv = self.app.post('/sqlite/api',data={"action": "add", "table": "company", "address": "1469 Beverly Glen", "age": "23", "name": "Bob Barker", "primaryKey": "id", "salary": "0"})
		self.assertEqual('{"status": 1, "message": "<a href="" class="alert-link">Refresh Page</a>"}',rv.data.replace('\\',""))
		
		rv = self.app.get('/sqlite/api?table=company&sort=&dir=asc&offset=0')
		assert '<span class="state-rest">Bob Barker</span>' in rv.data
		assert '<span class="state-rest">1469 Beverly Glen</span>' in rv.data

	def test_api_add_row_fail_new_rule1(self):
		rv = self.app.post('/sqlite/api',data={"action": "add", "table": "company", "address": "1469 Beverly Glen", "age": "23", "name": "testee mc test", "primaryKey": "id", "salary": "0"})
		self.assertEqual('{"status": 0, "error": "This is not Bob Barker!"}',rv.data.replace('\\',""))

	def test_api_edit_row_fail_new_rule1(self):
		rv = self.app.post('/sqlite/api',data={"action": "edit", "table": "company","id":"1","address": "1469 Beverly Glen", "age": "23", "name": "testee mc test", "primaryKey": "id", "salary": "0"})
		self.assertEqual('{"status": 0, "error": "This is not Bob Barker!"}',rv.data.replace('\\',""))

	def test_api_add_row_fail_new_rule2(self):
		rv = self.app.post('/sqlite/api',data={"action": "add", "table": "company", "address": "1221 Sacremento St", "age": "23", "name": "Bob Barker", "primaryKey": "id", "salary": "0"})
		self.assertEqual('{"status": 0, "error": "You cant live here!"}',rv.data.replace('\\',""))

	def test_api_edit_row_fail_new_rule2(self):
		rv = self.app.post('/sqlite/api',data={"action": "edit", "table": "company","id":"1","address": "1221 Sacremento St", "age": "23", "name": "Bob Barker", "primaryKey": "id", "salary": "0"})
		self.assertEqual('{"status": 0, "error": "You cant live here!"}',rv.data.replace('\\',""))


class flask_test_app_with_login_decorator:
	""" app setup with a decorator that always redirects to login page """
	
	app = Flask(__name__)
	
	@app.route('/')
	def index():
		return "hello world"

	@app.route('/login')
	def login():
		return "im a login page"
				
	def decoratorTest(f):
		@wraps(f)
		def decorated_function(*args, **kwargs):
			if 1==1:
				return redirect(url_for('login', next=request.url))
			return make_response(f(*args, **kwargs))
		return decorated_function

	bpTest = sqliteAdminBlueprint(bpName = 'sqliteTest',dbPath=db_file[1],decorator=decoratorTest)
	app.register_blueprint(bpTest, url_prefix='/sqlite')		

class testSQLiteBlueprintLoginDecorator(unittest.TestCase):
	""" test blueprint when decorator is passed """
	
	def setUp(self):
		flask_test_app_with_login_decorator.app.config['TESTING'] = True
		self.app = flask_test_app_with_login_decorator.app.test_client()		

	def test_index_page(self):
		rv = self.app.get('/')
		assert "hello world" in rv.data

	def test_base_page_get(self):
		rv = self.app.get('/sqlite/', follow_redirects=True)
		assert 'im a login page' in rv.data

	def test_base_page_post(self):
		rv = self.app.post('/sqlite/api',data={"action": "add", "table": "company", "address": "1469 Beverly Glen", "age": "23", "name": "testee mc test", "primaryKey": "id", "salary": "0"}, follow_redirects=True)
		assert 'im a login page' in rv.data
      
if __name__ == '__main__':
	unittest.main()
from flask import Blueprint, render_template, flash, request, abort, make_response
from sqliteFunctions import sqliteAdminFunctions, rules
import sqlite3
import json
import types
from flask_secure_headers.core import Secure_Headers
from functools import wraps
import os.path

# decorators
sh = Secure_Headers()
sh.update({'CSP':{'default-src':['localhost'],'script-src':['self','code.jquery.com','sha256-0U0JKOeLnVrPAm22MQQtlb5cufdXFDzRS9l-petvH6U=']}})

def defaultDecorator(f): 
	@wraps(f)
	def decorated_function(*args, **kwargs):
		return make_response(f(*args, **kwargs))
	return decorated_function

def sqliteAdminBlueprint(dbPath,bpName='sqliteAdmin',tables=[],title='sqlite Admin',h1='sqlite Admin',baseLayout='base.html',extraRules=[],decorator=defaultDecorator):
	""" create routes for admin """
	
	sqlite = Blueprint(bpName, __name__,template_folder='templates',static_folder='static')
	
	@sqlite.route('/',methods=['GET'])
	@decorator
	@sh.wrapper()
	def index():	
		db = sqlite3.connect(dbPath)	
		sf = sqliteAdminFunctions(db,tables=tables,extraRules=extraRules)
		res = sf.tableList(tables)
		if len(res) == 0:
			raise ValueError('No sqlite db and/or tables found at path = %s' % dbPath)
		else:
			return render_template('sqlite.html',res=res,title=title,h1=h1,baseLayout=baseLayout,bpName=bpName)	

	@sqlite.route('/api',methods=['GET','POST','PUT','DELETE'])
	@decorator
	@sh.wrapper()
	def api():
		# create sqliteAdminFunctions object
		db = sqlite3.connect(dbPath)
		sf = sqliteAdminFunctions(db,tables=tables,extraRules=extraRules)

		# GET request
		if request.method == 'GET':
			q = request.args			
			try:
				res = sf.tableContents(request.args['table'],request.args['sort'],request.args['dir'],request.args['offset'])
				return render_template('sqlite_ajax.html',data=res,title=title,h1=h1,baseLayout=baseLayout,bpName=bpName,q=q,qJson=json.dumps(q))
			except Exception, e:
				return render_template('sqlite_ajax.html',error=e.message)
		# POST request
		else:
			try:
				res = {'status':1,'message':sf.editTables(request.form,request.method)}
			except Exception, e:
				res = {'status':0,'error':e.message}
			return json.dumps(res)	

	return sqlite
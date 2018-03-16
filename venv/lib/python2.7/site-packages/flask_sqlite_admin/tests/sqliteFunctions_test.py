import unittest
import sqlite3
import tempfile
import os

from sqliteFunctions import *

class TestFunctions(unittest.TestCase):
	def setUp(self):
		self.db_fd,self.f = tempfile.mkstemp()
		self.con = sqlite3.connect(self.f)
		self.con.execute('CREATE TABLE company( id integer PRIMARY KEY autoincrement, name TEXT NOT NULL, age integer NOT NULL, address CHAR(50), salary REAL );')
		self.con.execute('CREATE TABLE department( id INT PRIMARY KEY, dept CHAR(50) NOT NULL, emp_id INT NOT NULL );')
		self.sf = sqliteAdminFunctions(self.con)
		
	def tearDown(self):
		os.close(self.db_fd)
		os.unlink(self.f)
	
	def test_valid_addition(self):
		self.sf.editTables( { 'action':u'add','table': u'company','primaryKey': u'id','name': u'Bob Barker', 'age': u'71', 'address': u'123 Fake Street', 'salary':'1000000.1'} )
		
		c = self.con.execute('select * from company').fetchall()[0]	
		self.assertEquals(c[0],1)
		self.assertEquals(c[1],'Bob Barker')
		self.assertEquals(c[2],71)
		self.assertEquals(c[3],'123 Fake Street')
		self.assertEquals(c[4],1000000.1)
	
	def test_valid_edit(self):
		self.test_valid_addition()
		self.sf.editTables( { 'action':u'edit','table': u'company','primaryKey': u'id', 'id':'1','name': u'Tom Tucker', 'age': u'-71', 'address': u'123 Fake Street', 'salary':'1000000'} )
		
		c = self.con.execute('select * from company').fetchall()[0]
		self.assertEquals(c[0],1)
		self.assertEquals(c[1],'Tom Tucker')
		self.assertEquals(c[2],-71)
		
	def test_valid_delete(self):
		self.test_valid_addition()
		self.sf.editTables( { 'action':u'delete','table': u'company','primaryKey': u'id', 'id':'1','name': u'Tom Tucker', 'age': u'71', 'address': u'123 Fake Street', 'salary':'1000000'} )
		self.assertEquals(len(self.con.execute('select * from company').fetchall()),0)
				
	def test_invalid_table(self):
		with self.assertRaises(Exception) as cm:
			self.sf.editTables( { 'action':u'add','table': u'employees'} )
		self.assertEqual( 'invalid table `employees`',str(cm.exception) )
	
	def test_invalid_action(self):
		with self.assertRaises(Exception) as cm:
			self.sf.editTables( { 'action':u'jormp','table': u'company'} )
		self.assertEqual( 'invalid action `jormp`',str(cm.exception) )		

	def test_invalid_idRequired(self):
		with self.assertRaises(Exception) as cm:
			self.sf.editTables( { 'action':u'edit','table': u'company'} )
		self.assertEqual( 'Request must include an id',str(cm.exception) )		

	def test_invalid_notNull(self):
		with self.assertRaises(Exception) as cm:
			self.sf.editTables( {'action':u'add','table': u'company'} )
		self.assertEqual('name field required',str(cm.exception) )		
		
		with self.assertRaises(Exception) as cm:
			self.sf.editTables( {'action':u'add','table': u'company','name': u'Bob Barker'} )
		self.assertEqual('age field required',str(cm.exception) )	
		
	def test_invalid_notInteger(self):
		with self.assertRaises(Exception) as cm:
			self.sf.editTables( { 'action':u'add','table': u'company', 'name': u'Bob Barker', 'age': u'test', 'address': u'123 Fake Street', 'salary':'1000000'} )
		self.assertEqual('Non integer value `test` for field age',str(cm.exception) )	

	def test_invalid_notReal(self):
		with self.assertRaises(Exception) as cm:
			self.sf.editTables( { 'action':u'add','table': u'company', 'name': u'Bob Barker', 'age': u'71', 'address': u'123 Fake Street', 'salary':'test'} )
		self.assertEqual('Non real/float value `test` for field salary',str(cm.exception) )

	def test_table_list(self):
		r = self.sf.tableList([])
		assert 'company' in r
		assert 'department' in r
		
	def test_table_schemas(self):
		r = self.sf.tableSchemas('department')
		self.assertEquals(r[0]['name'], 'id')
		self.assertEquals(r[0]['dataType'], 'INT')
		self.assertEquals(r[0]['primaryKey'], 1)
		
		r = self.sf.tableSchemas('company')
		self.assertEquals(r[2]['name'], 'age')
		self.assertEquals(r[2]['dataType'], 'integer')
		self.assertEquals(r[2]['notNull'], 1)
		
	def test_table_contents_empty(self):
		r = self.sf.tableContents('department','id','asc','0')
		self.assertEquals(r['contents'], [])
	
	def test_table_contents(self):
		self.test_valid_addition()
		r = self.sf.tableContents('company','id','asc','0')
		self.assertEquals(r['contents'], [{'salary': 1000000.1, 'age': 71, 'address': u'123 Fake Street', 'id': 1, 'name': u'Bob Barker'}])

	def mult_table_add(self):
		self.sf.editTables( { 'action':u'add','table': u'company','primaryKey': u'id','name': u'Bob Barker', 'age': u'71', 'address': u'123 Fake Street', 'salary':'123.1'} )
		self.sf.editTables( { 'action':u'add','table': u'company','primaryKey': u'id','name': u'Tom Tucker', 'age': u'23', 'address': u'123 Fake Street', 'salary':'1000000.1'} )
		self.sf.editTables( { 'action':u'add','table': u'company','primaryKey': u'id','name': u'Zuck Zuckerberg', 'age': u'55', 'address': u'123 Fake Street', 'salary':'125.1'} )		

	def test_table_contents_sort_desc_name(self):
		self.mult_table_add()
		
		r = self.sf.tableContents('company','name','desc','0')
		self.assertEquals(r['contents'][0]['name'],'Zuck Zuckerberg')
	
	def test_table_contents_sort_asc_age(self):
		self.mult_table_add()
		
		r = self.sf.tableContents('company','age','asc','0')
		self.assertEquals(r['contents'][0]['age'],23)
		self.assertEquals(r['contents'][-1]['age'],71)
		
	def test_table_contents_sort_desc_salary(self):
		self.mult_table_add()	
		
		r = self.sf.tableContents('company','salary','desc','0')
		self.assertEquals(r['contents'][0]['name'],'Tom Tucker')
		self.assertEquals(r['contents'][-1]['name'],'Bob Barker')
		
if __name__ == '__main__':
    unittest.main()
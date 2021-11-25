import sqlite3
conn=sqlite3.connect('student.sqlite')
cur=conn.cursor()
cur.execute('DROP TABLE IF EXISTS student')
cur.execute('CREATE TABLE student(id,name TEXT,uuid INTEGER)')
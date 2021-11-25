import sqlite3
conn=sqlite3.connect('name.sqlite')
cur=conn.cursor()
cur.execute('DROP TABLE IF EXISTS vidata')
cur.execute('CREATE TABLE vidata(id,name TEXT,title TEXT,description TEXT,subject TEXT,extension TEXT,teachername TEXT,idd  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,date TEXT)')
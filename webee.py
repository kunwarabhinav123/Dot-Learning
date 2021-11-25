import sqlite3
from flask import Flask, request, render_template, session, url_for, logging, redirect, flash
from flask_session import Session
conn=sqlite3.connect('web.sqlite')
cur=conn.cursor()
cur.execute('DROP TABLE IF EXISTS Counts')
cur.execute('CREATE TABLE Counts(id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,name TEXT,username TEXT,gender TEXT,person TEXT,phone INTEGER,email TEXT,dob TEXT,password TEXT,confirm TEXT)')


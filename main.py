from flask import Flask, request, render_template, session, url_for, logging, redirect, flash
from flask_mail import Mail,Message
from random import *
from datetime import datetime
from pymongo import MongoClient
import json
import sqlite3
import time
import re
from werkzeug.utils import secure_filename
import os
import random
import string
import time


app = Flask(__name__,static_folder='uploads')

app.config["VIDEO_UPLOADS"] = "uploads"
app.config["ALLOWED_VIDEO_EXTENSIONS"] = ["MP4", "MPEG", "AVI", "GIF","PPTX","DOCX","PDF","JPG","JPEG"]
app.config["MAX_VIDEO_FILESIZE"] = 1000* 1024 * 1024

mail = Mail(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'dotlearning1@gmail.com'
app.config['MAIL_PASSWORD'] = '7388225515'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
conn=sqlite3.connect('web.sqlite')
cur=conn.cursor()


d=0
auser=list()

def randStr(chars = string.ascii_uppercase + string.digits, N=10):
	return ''.join(random.choice(chars) for _ in range(N))

mail = Mail(app)  
otp = randint(000000,999999)   
print(otp)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/otpp",methods=['GET','POST'])
def otpp():
    if request.method == 'POST':
        email=request.form['email']
        session['email']=email
        msg = Message("Verification code is:",sender = 'dotlearning', recipients = [session['email']])  
        msg.body = str(otp)  
        mail.send(msg)
          
        
        return render_template("verify.html")
        
    else:
        return render_template("otp.html")


@app.route("/register",methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        #print(json.dumps(request.form, indent=4))
        name = request.form['name']
        username = request.form['username']
        gender=request.form['gender']
        person=request.form['person']
        phone=request.form['phone']
        email=request.form['email']
        session['email']=email
        dob=request.form['dob']
        password = request.form['password']
        confirm = request.form['confirm password']
        conn=sqlite3.connect('web.sqlite')
        cur=conn.cursor()
        cur.execute('SELECT username FROM Counts where username=?',(username,))
        auser=cur.fetchall()
        if not auser:
        
            if(password==confirm):
            
                #cur.execute('DROP TABLE IF EXISTS Counts')
            
                try:
                    cur.execute('CREATE TABLE Counts(id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,name TEXT,username TEXT,gender TEXT,person TEXT,phone INTEGER,email TEXT,dob TEXT,password TEXT,confirm TEXT)')
                    cur.execute('INSERT INTO Counts(name,username,gender,person,phone,email,dob,password,confirm) VALUES (?,?,?,?,?,?,?,?,?)',(name,username,gender,person,phone,email,dob,password,confirm))
                    flash("Registration successful", "success")
                except:
                    cur.execute('INSERT INTO Counts(name,username,gender,person,phone,email,dob,password,confirm) VALUES (?,?,?,?,?,?,?,?,?)',(name,username,gender,person,phone,email,dob,password,confirm))
                    flash("Registration successful", "success")
                conn.commit()
             
                
                return render_template("login.html")
            else:
                flash("Password do not match", "danger")
                return render_template("register.html")
        else:
             flash("Username already exist", "danger")
             return render_template("register.html")
    else:
        return render_template('register.html')


@app.route("/login", methods=["POST","GET"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        
        conn=sqlite3.connect('web.sqlite')
        cur=conn.cursor()
        cur.execute('SELECT password FROM Counts where username=?',(username,))
        pw=cur.fetchall()
        cur.execute('SELECT name FROM Counts where username=?',(username,))
        pwn=cur.fetchall()
        cur.execute('SELECT person FROM Counts where username=?',(username,))
        pt=cur.fetchall()
        cur.execute('SELECT id FROM Counts where username=?',(username,))
        ptt=cur.fetchall()
        try:
            c2=pt[0]
            c=pw[0]
            c3=ptt[0]
            c4=pwn[0]
            session['name']=c4[0]
            session['d']=c3[0]
            print(c2)
            
            if (c[0]==password and c2[0]=='teacher'):
                    session['log'] = True
                    flash("You are logged in", "success")
                    return redirect('/vid')
                    
            elif (c[0]==password and c2[0]=='student'):
                    session['log1'] = True
                    flash("You are logged in", "success")   
                    return redirect('/student')         
            else:
                    flash("Incorrect password", "danger")           
                    return render_template("login.html")
        except:
        
            if not pw:
                flash("You are not registered", "danger")
                return redirect("/register")
    else:
        return render_template("login.html")

@app.route("/verify",methods = ["POST","GET"])  
def verify():
    if request.method == "POST":
        user_otp = request.form['otp']  
        if otp == int(user_otp):  
            flash("Email verification successful","success")  
            return render_template("register.html",email=session["email"])
        else:
            flash("Verificaton code is incorrect","danger")
            return render_template('verify.html')
    else:
        return render_template('verify.html')


@app.route("/logout")
def logout():
    session.clear()
    flash("You are logged out!","success")
    return redirect("/")
    
    
    
    
def allowed_video(filename):

    if not "." in filename:
        return False

    ext = filename.split(".")[-1]
    
    if ext.upper() in app.config["ALLOWED_VIDEO_EXTENSIONS"]:
        return True
    else:
        return False


def allowed_video_filesize(filesize):

    if int(filesize) <= app.config["MAX_VIDEO_FILESIZE"]:
        return True
    else:
        return False


@app.route('/vid', methods=["GET", "POST"])
def upload_video():

    if request.method == "POST":

       # if request.form:

                conn=sqlite3.connect('name.sqlite')
                cur=conn.cursor()
                
                
                title = request.form['title']
                description = request.form['description']
                subject=request.form['subject']
                uuid=request.form['uuid']
                teachername=request.form['teachername']
                print(teachername)
                video = request.files["video"]
                ext = video.filename.split(".")[-1]
                ext=ext.upper()
                if video.filename == "":
                    flash("No filename","danger")
                    return redirect('/vid')
                    
                  

                if allowed_video(video.filename):
                    filename = video.filename

                    video.save(os.path.join(app.config["VIDEO_UPLOADS"], filename))

                    flash("File Uploaded","success")
                    t=time.localtime()
                    lt=time.strftime("%H:%M:%S  %d %b",t)
                    try:
                        cur.execute('CREATE TABLE vidata(id,name TEXT,title TEXT,description TEXT,subject TEXT,extension TEXT,teachername TEXT,date TEXT)')
                        cur.execute('INSERT INTO vidata(id,name,title,description,subject,extension,teachername) VALUES (?, ?,?,?,?,?,? )', (int(uuid[0]), video.filename,title,description,subject, ext,teachername,) )
                    
                    except:
                        cur.execute('INSERT INTO vidata(id,name,title,description,subject,extension,teachername,date) VALUES ( ?,?,?,?,?,?,?,?)', (int(uuid), video.filename,title,description,subject,ext,teachername,lt, ) )
                    
                    conn.commit()

                    return redirect('/vid')

                else:
                    flash("File extension is not allowed","danger")
                    return redirect('/vid')
    else:
        conn=sqlite3.connect('name.sqlite')
        
        cur=conn.cursor()
        cur.execute('SELECT*FROM vidata ORDER BY idd DESC')
        #conn.commit()
        #cur.execute('SELECT name FROM vidata')
        a=cur.fetchall()
        #print(a)
        
        
        return render_template("vid.html",vid=a,uid=session.get('d'),ran=randStr(N=7),name=session.get('name'))
    
@app.route('/vid/delete/<string:name>')   
def delete(name):
    conn=sqlite3.connect('name.sqlite')
    cur=conn.cursor()
    #print(name)
    cur.execute('DELETE FROM vidata WHERE name=(?)',(name,))
    conn.commit()
    path = os.path.join(app.config["VIDEO_UPLOADS"], name)
    os.remove(path)    
    return redirect('/vid') 
    
    

@app.route('/vid/edit/<string:name>',methods=['GET', 'POST'])   
def edit(name):
    conn=sqlite3.connect('name.sqlite')
    cur=conn.cursor()
    #print(name)
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        cur.execute('UPDATE vidata SET title=(?) where name=(?)',(title,name,))
        cur.execute('UPDATE vidata SET description=(?) where name=(?)',(description,name,))
        conn.commit()
        return redirect('/vid') 
    else:
            
        cur.execute('SELECT*FROM vidata where name=(?)',(name,))
        a=cur.fetchall()
        print(a)
        return render_template("edit.html",vid=a)   
    
@app.route('/student',methods=["GET", "POST"])
def student():
    if request.method =='POST':
        conn=sqlite3.connect('student.sqlite')
        cur=conn.cursor()
        name=session.get('name')
        uuid=request.form['uuid']
        cur.execute('SELECT uuid FROM student where name=?',(name,))
        
        cur.execute('INSERT OR IGNORE INTO student(id,name,uuid) VALUES(?,?,?)',(session.get('d'),name,int(uuid),))
        conn.commit()
        return redirect('/student')
    
    else:
        conn=sqlite3.connect('name.sqlite')
            
        cur=conn.cursor()
        cur.execute('SELECT*FROM vidata ORDER BY idd DESC')
        #conn.commit()
        #cur.execute('SELECT name FROM vidata')
        a=cur.fetchall()
        conn=sqlite3.connect('student.sqlite')
        cur=conn.cursor()
        cur.execute("SELECT*FROM student")
        b=cur.fetchall()
       
        namee=session.get('name')
        lst=list()
       
        for i in a:
            
            for j in b:
                
                if(namee==j[1] and j[2]==i[0]):
                    lst.append(i[6])
        
        
        k=dict()
        for line in lst:
            k[line]=k.get(line,0)+1   
            
         
        return render_template("student.html",vid=a,filter=k,uid=b,name=session.get('name'),uuid=session.get('d'))

@app.route("/academic")
def academic():
   
    return render_template("academic.html")    

app.secret_key="12ddededd"
app.run(debug=True)
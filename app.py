from flask import Flask, flash,render_template,request,redirect,url_for,session
import mysql.connector as c
import database as db
from flaskext.mysql import MySQL
import pymysql
import json
import os.path
import smtplib  
from datetime import date
from flask_wtf import FlaskForm
from wtforms import FileField,SubmitField
from wtforms.validators import InputRequired
from werkzeug.utils import secure_filename 
from email.message import EmailMessage



app = Flask(__name__)
app.secret_key = "Sudheer"
app.config['UPLOAD_FOLDER'] = "static/attachments"


mysql = MySQL()
# MySQL Configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'sudheer123'
app.config['MYSQL_DATABASE_DB'] = 'nsrit'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
con = mysql.connect()
cur = con.cursor(pymysql.cursors.DictCursor)
@app.route('/')
def home():
    return render_template('home.html')
@app.route('/signin', methods = ['GET','POST'])
def signin():
    if request.method=='GET':
        return render_template('signin.html')
    email = request.form['email']
    passw = request.form['password']
    con = mysql.connect()
    cur = con.cursor(pymysql.cursors.DictCursor)
    cur.execute("select pwd from admindata where email = %s;",(email))
    data = cur.fetchall()
    con.commit()
    cur.close()
    d = data[0]
    if passw == d['pwd']:
        return render_template('home.html')
    else:
        return render_template('signin.html')
@app.route('/signup',methods = ['GET','POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    name   = request.form['fullname']
    email  = request.form['email']
    mobile = request.form['number']
    gender = request.form['gender']
    pass1  = request.form['password1']
    pass2  = request.form['password2']
    con = mysql.connect()
    cur = con.cursor(pymysql.cursors.DictCursor)
    cur.execute('select email from admindata;')
    data = cur.fetchall()
    con.commit()
    cur.close()
    if email in data:
        return render_template('signup.html',msg = 'Looks like you are already registered')
    elif pass1 == pass2:
         con = mysql.connect()
         cur = con.cursor(pymysql.cursors.DictCursor)
         cur.execute('INSERT INTO admindata(name,email,mobile,gender,pwd) VALUES(%s,%s,%s,%s,%s);',(name,email,mobile,gender,pass2))
         con.commit()
         cur.close()
         return render_template('signup.html',msg = "successfully Registered")
    else:
        return render_template('signup.html',msg ='Password Miss match')
@app.route('/filters')
def filters():
        return render_template('form.html')

@app.route('/upload_sheet')
def upload_sheet():
        return render_template('sheet.html')


@app.route('/show_table',methods = ['GET','POST'])
def show_table():
    if request.method == 'GET':
        data1 = db.male()
        data2 = db.female()
        return render_template('table.html')
    elif request.method == 'POST':
        c = request.form['company']
        per_b = request.form['criteria_btech']
        per_i = request.form['criteria_inter']
        per_t = request.form['criteria_tenth']
        b = request.form['backlog-selection']
        gen = request.form['gender']
        # data table for eligible list
        data_eligible = db.showList(per_b,per_i,per_t,gen,b)
        c_count = len(data_eligible)
        # push into company data base
        con = mysql.connect()
        cur = con.cursor(pymysql.cursors.DictCursor)
        cur.execute('INSERT INTO Companies(c_name,c_per_b,c_per_i,c_per_t,c_gen,c_b,c_count) VALUES(%s,%s,%s,%s,%s,%s,%s);',(c,per_b,per_i,per_t,gen,b,c_count))
        con.commit()
        data_eligible = db.showList(per_b,per_i,per_t,gen,b)  
        return render_template('table.html', table_eligible = data_eligible, c = " Eligible Students List For {}".format(c))



@app.route('/send_mail/<id>')
def send_mail(id):
    con = mysql.connect()
    cur = con.cursor(pymysql.cursors.DictCursor)
    cur.execute('SELECT * FROM Companies WHERE c_id = %s',(id))
    data = cur.fetchall()
    cur.close()
    d = data[0]
    per_b = d['c_per_b'] 
    per_i = d['c_per_i'] 
    per_t = d['c_per_t']
    gen = d['c_gen']
    b = d['c_b']
    data_mailList = db.mailList(per_b,per_i,per_t,gen,b)
    email_li = []
    for i in data_mailList:
        s = i[0]
        s = str(s)
        if('\xa0' in s):
            s = s.replace(u'\xa0', u' ')
            email_li.append(s[1:])
        else:
            email_li.append(s)   
    with open('mails.json','w') as url_file:
        json.dump(email_li,url_file)
    
    if os.path.exists('mails.json'):
        with open('mails.json') as urls_file:
            mails = json.load(urls_file)
        
    server=smtplib.SMTP_SSL("smtp.gmail.com",465)
    server.login("lolday606@gmail.com","ztskhwqzmvanmjqn")
    for i in mails:
        if(' ' in i):
            continue
        elif('@' in i):
            server.sendmail("sudheer.edu.feb@gmail.com",i,"If It's Working plz reply with a kk msg(It is just a project done by your seniors we are testing it).....!!!!")
            flash("Mail Sent to {} {}".format(i,date.today()))
    server.quit()
    return render_template("output1.html",mails_li = mails)


@app.route('/show_logs',methods=["GET","POST"])
def show_logs():
    con = mysql.connect()
    cur = con.cursor(pymysql.cursors.DictCursor)
    cur.execute('SELECT * FROM Companies;')
    data = cur.fetchall()
    cur.close()
    return render_template('company.html', sample = data)

@app.route('/students',methods=["GET","POST"])
def students():
    con = mysql.connect()
    cur = con.cursor(pymysql.cursors.DictCursor)
    cur.execute('select sqldb1.False,sqldb2.Roll,sqldb2.Student_Name,sqldb1.Gender,sqldb1.SSC_Percentage,sqldb1.Inter_Percentage,sqldb2.Percentage,sqldb2.Total_Backlogs,sqldb1.Mobile_No,sqldb1.Email FROM sqldb2 JOIN sqldb1 ON sqldb1.False=sqldb2.False')
    data = cur.fetchall()
    cur.close()
    sam = data[0]
    return render_template('student_table.html',student_data = data, sam = sam)

@app.route('/edit_student_data/<id>')
def edit_student_data(id):
    con = mysql.connect()
    cur = con.cursor(pymysql.cursors.DictCursor)
    cur.execute('select sqldb1.False,sqldb2.Roll,sqldb2.Student_Name,sqldb1.Gender,sqldb1.SSC_Percentage,sqldb1.Inter_Percentage,sqldb2.Percentage,sqldb2.Total_Backlogs,sqldb1.Mobile_No,sqldb1.Email FROM sqldb2 JOIN sqldb1 ON sqldb1.False=sqldb2.False WHERE sqldb1.False = {}'.format(id))
    data = cur.fetchall()
    cur.close()
    return render_template('edit_student_data.html', student_data = data[0])

@app.route('/update_student_data_1/<em>',methods=['GET','POST'])
def update_student_data_1(em):
    con = mysql.connect()
    cur = con.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST':
        i = request.form['ID']
        roll = request.form['Roll']
        ssc = request.form['ssc_p']
        inter = request.form['inter_p']
        gen = request.form['Gender']
        phone = request.form['phone']
        email = request.form['email'],
        print(gen)
        print(type(gen))
        print(id)
        print(type(id))
        cur.execute("UPDATE sqldb1 SET Gender = '{}' WHERE Email = {};".format(gen,em))
        con.commit()
        return redirect(url_for('students'))
    else:
        return render_template('error.html',id = id)


@app.route('/update_student_data_2/<id>',methods=['GET','POST'])
def update_student_data_2(id):
    con = mysql.connect()
    cur = con.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST':
        i = request.form['ID']
        roll = request.form['Roll']
        name = request.form['Name']
        btech = request.form['btech_p']
        b = request.form['Backlogs']
        cur.execute('UPDATE sqldb2 SET False = {},Roll = {},Student_Name = {},Percentage = {},Total_Backlogs = {} WHERE False = {};'.format(i,roll,name,btech,b,id))
        con.commit()
        return redirect(url_for('students'))
    else:
        return "error page 2"

@app.route('/analysis/<id>')
def analysis(id):
    con = mysql.connect()
    cur = con.cursor(pymysql.cursors.DictCursor)
    cur.execute('SELECT * FROM Companies WHERE c_id = %s',(id))
    data = cur.fetchall()
    cur.close()
    d = data[0]
    per_b = d['c_per_b'] 
    per_i = d['c_per_i'] 
    per_t = d['c_per_t']
    gen = d['c_gen']
    b = d['c_b']
    data_eligible = db.showList(per_b,per_i,per_t,gen,b)  
    
    # 'c_count': '37', 
    # 'c_date_time': datetime.datetime(2022, 10, 6, 23, 42, 47)}
    return render_template('table1.html', table_eligible = data_eligible, c = " Eligible Students List For {}".format(d['c_name']))
    

@app.route('/delete/<string:id>',methods=['GET','POST'])
def delete_contact(id):
    con = mysql.connect()
    cur = con.cursor(pymysql.cursors.DictCursor)
    cur.execute('DELETE FROM Companies WHERE c_id = {};'.format(id))
    con.commit()
   
    return redirect(url_for('show_logs'))

if __name__ =='__main__':
    app.run(port =5000,debug =True)
    print("welcome!!!!!!!!")
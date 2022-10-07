
from flask import Flask, flash,render_template,request,redirect,url_for
import mysql.connector as c
import database as db
from flaskext.mysql import MySQL
import pymysql
import json
import os.path
import smtplib
from datetime import date




app = Flask(__name__)
app.secret_key = "Sudheer"


mysql = MySQL()
# MySQL Configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'sudheer123'
app.config['MYSQL_DATABASE_DB'] = 'nsrit'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route('/',methods = ['GET','POST'])
def home():
        return render_template('form.html')


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
        if('@' in i):
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
    return render_template('index.html', sample = data)


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
    



if __name__ =='__main__':
    app.run(port =5000,debug =True)
    print("welcome!!!!!!!!")
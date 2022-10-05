from flask import Flask,render_template,request,redirect,url_for
import mysql.connector as c
import database as db
import json
import os.path
import smtplib

app = Flask(__name__)

@app.route('/',methods = ['GET','POST'])
def home():
        return render_template('form.html')


@app.route('/show_table',methods = ['GET','POST'])
def show_table():
    if request.method == 'GET':
        data1 = db.male()
        data2 = db.female()

    elif request.method == 'POST':
        c = request.form['company']
        per_b = request.form['criteria_btech']
        per_i = request.form['criteria_inter']
        per_t = request.form['criteria_tenth']
        b = request.form['backlog-selection']
        gen = request.form['gender']
        # for sending the filters into a json file as a dictionary
        l = []
        dict = {}
        dict['c_name'] = c
        dict['per_b'] = per_b
        dict['per_i'] = per_i
        dict['per_t'] = per_t
        dict['b'] = b
        dict['gen'] = gen
        l.append(dict)
        with open('filters.json','w') as url_file:
            json.dump(l,url_file)

        data_eligible = db.showList(per_b,per_i,per_t,gen,b)  
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
        return render_template('table.html', table_eligible = data_eligible, c = c)
    
    

@app.route('/mail')
def send_mail():
    if request.method == 'GET':
        if os.path.exists('mails.json'):
            with open('mails.json') as urls_file:
                mails = json.load(urls_file)
        
        ''' server=smtplib.SMTP_SSL("smtp.gmail.com",465)
        server.login("lolday606@gmail.com","ztskhwqzmvanmjqn")
        for i in mails:
            if '@gmail.com' in i:
                server.sendmail("sudheer.edu.feb@gmail.com",i,"If It's Working plz reply with a kk msg(It is just a project done by your seniors we are testing it).....!!!!")
        server.quit()'''
        
        return render_template("output1.html",mails_li = mails)


if __name__ =='__main__':
    app.run(port =5000,debug =True)
    print("welcome!!!!!!!!")
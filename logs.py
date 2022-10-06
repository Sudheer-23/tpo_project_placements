from flask import Flask, render_template, request, url_for, redirect, flash, get_flashed_messages
from flaskext.mysql import MySQL
import pymysql

app = Flask(__name__)
app.secret_key = "Sudheer"


mysql1 = MySQL()
# MySQL Configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'sudheer123'
app.config['MYSQL_DATABASE_DB'] = 'sample'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql1.init_app(app)

@app.route('/')
def sample():
    con1 = mysql1.connect()
    cur1 = con1.cursor(pymysql.cursors.DictCursor)
    cur1.execute('SELECT * FROM TimeStamp;')
    data1 = cur1.fetchall()
    cur1.close()
    return render_template('index.html', sample = data1)




@app.route('/greet')
def greet():
    return render_template('layout1.html')

if __name__ == '__main__':
    app.run(debug=True)
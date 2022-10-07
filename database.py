import mysql.connector as c
con = c.connect(host = "localhost",user = "root",password = "sudheer123",database = "nsrit")
con1 = c.connect(host = "localhost",user = "root",password = "sudheer123",database = "college")
def male():
    cursor = con.cursor()
    cursor.execute("""UPDATE sqldb1 SET gender='Male' WHERE gender='\xa0Male';""")
    table1 = cursor.fetchall()
    con.commit()
    cursor.close()
    return table1

def female():
    cursor = con.cursor()
    cursor.execute("""UPDATE sqldb1 SET gender='Female' WHERE gender='\xa0Female';""")
    table1 = cursor.fetchall()
    con.commit()
    cursor.close()
    return table1

def showList(per_b,per_i,per_t,gen,b):
    cursor = con.cursor()
    if (gen == 'Male') or (gen == 'Female'):
        cursor.execute("""select sqldb1.False,sqldb2.Roll,sqldb2.Student_Name,sqldb1.Gender,sqldb1.SSC_Percentage,sqldb1.Inter_Percentage,sqldb2.Percentage,sqldb2.Total_Backlogs,sqldb1.Mobile_No,sqldb1.Email FROM sqldb2 JOIN sqldb1 ON sqldb1.False=sqldb2.False WHERE Percentage>={per_b} AND Inter_Percentage>={per_i} AND SSC_Percentage>={per_t} AND Gender="{gen}" AND Total_Backlogs>={b};""".format(per_b=per_b,per_i=per_i,per_t=per_t,gen=gen,b=b))
    else:
        cursor.execute("""select sqldb1.False,sqldb2.Roll,sqldb2.Student_Name,sqldb1.Gender,sqldb1.SSC_Percentage,sqldb1.Inter_Percentage,sqldb2.Percentage,sqldb2.Total_Backlogs,sqldb1.Mobile_No,sqldb1.Email FROM sqldb2 JOIN sqldb1 ON sqldb1.False=sqldb2.False WHERE Percentage>={per_b} AND Inter_Percentage>={per_i} AND SSC_Percentage>={per_t} AND Total_Backlogs>={b};""".format(per_b=per_b,per_i=per_i,per_t=per_t,b=b))
    table_eligible = cursor.fetchall()
    con.commit()
    cursor.close()
    return table_eligible

def mailList(per_b,per_i,per_t,gen,b):
    cursor = con.cursor()
    cursor.execute("""select sqldb1.Email FROM sqldb2 JOIN sqldb1 ON sqldb1.False=sqldb2.False WHERE Percentage>={per_b} AND Inter_Percentage>={per_i} AND SSC_Percentage>={per_t} AND Gender="{gen}" AND Total_Backlogs>={b};""".format(per_b=per_b,per_i=per_i,per_t=per_t,gen=gen,b=b))  
    #cursor.execute('select email from students;')
    table_mailList = cursor.fetchall()
    con.commit()
    cursor.close()
    return table_mailList

def mails():
    cursor1 = con1.cursor()
    cursor1.execute('''select email from students;''')
    table_email = cursor1.fetchall()
    con1.commit()
    cursor1.close()
    return table_email

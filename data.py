import pandas as pd
import pymysql
from sqlalchemy  import create_engine
import sqlalchemy
pymysql.install_as_MySQLdb()
engine = create_engine('mysql://root:sudheer123@localhost/NSRIT')
df1 = pd.read_excel('new_results\combined_cse3-1.xlsx',sheet_name='combined')
df2 = pd.read_excel('new_results\cse3-1 results.xlsx',sheet_name='cse3-1 results')
sd1 = pd.DataFrame()
sd2 = pd.DataFrame()
df3 = pd.DataFrame()
df4 = pd.DataFrame()
sd1 = df1[["Roll","Caste","SSC_Percentage","Inter_Percentage","Gender","Mobile_No","Email"]]
sd2 = df2[["Roll","Student_Name","Percentage","Total_Backlogs"]]

df3 = pd.merge(sd1,sd2, on = "Roll", how = "left")
df4 = pd.merge(sd1,sd2, on = "Roll", how = "right")

df3.drop('Student_Name',axis=1,inplace=True)  
df3.drop('Percentage',axis=1,inplace=True) 
df3.drop('Total_Backlogs',axis=1,inplace=True) 
print(df3.head())


df4.drop('Caste',axis=1,inplace=True)  
df4.drop('SSC_Percentage',axis=1,inplace=True) 
df4.drop('Inter_Percentage',axis=1,inplace=True)
df4.drop('Gender',axis=1,inplace=True)  
df4.drop('Mobile_No',axis=1,inplace=True)
df4.drop('Email',axis=1,inplace=True)
print(df4.head())

df3.to_excel('results_data\excel_L.xls', index = False)
#df3.to_sql("sqldb1",con= engine,if_exists ="append",index="False")

df4.to_excel('results_data\excel_R.xls', index = False)
#df4.to_sql("sqldb2",con= engine,if_exists ="append",index="False")
print('Success')
import pandas as pd
import pymysql
from sqlalchemy  import create_engine
import sqlalchemy
pymysql.install_as_MySQLdb()
engine = create_engine('mysql://root:sudheer123@localhost/NSRIT')
print(engine)
df1 = pd.read_excel("results_data\excel_L.xls",dtype = {"SSC_Percentage":float,"Inter_Percentage":float})
print(df1.dtypes)
df1.to_sql("sqldb1",con= engine,if_exists ="append",index="False")
df2 = pd.read_excel("results_data\excel_R.xls")
print(df2.dtypes)
print(df2.head())
#df2.to_sql("sqldb2",con= engine,if_exists ="append",index="False")

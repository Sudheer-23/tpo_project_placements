import pandas as pd

df1 = pd.DataFrame()
df2 = pd.read_excel('results_data\cse3-1.xls',sheet_name='cse-a')
df3 = pd.read_excel('results_data\cse3-1.xls',sheet_name='cse-b')
df1 = pd.concat([df2,df3])
print(df1.head())
df1.to_excel('C:\Sudheer\Pandas\combined_cse3-1.xls')


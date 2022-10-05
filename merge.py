# importing the module
import pandas as pd
import pymongo

uri = "mongodb://localhost:27017/"
client = pymongo.MongoClient(uri)  
mydb =  client["nsrit"]
fields = mydb["pandasData"] 
print(client)
# reading the files
f1 = pd.read_excel('results_data\combined_cse3-1.xls',sheet_name='combined')
f2 = pd.read_excel('results_data\cse3-1 results.xls',sheet_name='cse3-1 results')
sd1 = pd.DataFrame()
sd2 = pd.DataFrame()
f3 = pd.DataFrame()
sd1 = f1[["Roll","Caste","SSC_Percentage","Inter_Percentage","Mobile_No.","Email"]].to_dict("records")
sd2 = f2[["Roll","Student_Name","Percentage","Total_Backlogs"]].to_dict("records")
# merging the files
#f3 = pd.merge(left = sd1,right = sd2, on = "Roll.No", how = "outer")
# creating a new file

fields.insert_many(sd1)
fields.insert_many(sd2)
print("success")
#f5.to_excel('Results.xls', index = False)
ans =fields.find_one()
print(ans)
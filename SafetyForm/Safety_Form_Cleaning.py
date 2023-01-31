### Import Libarary
#Basic
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
#Plotting Library
import matplotlib.pyplot as plt
import seaborn as sns
import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))
import datetime
import time

### Load the CSV
Form_File_Read = pd.read_csv('Construction_Data_PM_Forms_All_Projects.csv')

### Data Cleaning
## 1. Eliminate useless column **Association/Images/Comments/Documents/**
Form_File = Form_File_Read.drop(columns=['Association','Images','Comments','Documents'])

## 2. Transform the date data back to UNIX timestamp in Sec to calculate the duration
def To_TimestampSEC(date):
    element = datetime.datetime.strptime(date,"%d/%m/%Y") 
    tuple = element.timetuple() 
    timestamp = int(time.mktime(tuple))
    return timestamp

Form_File['Created_Sec'] = Form_File['Created'].apply(lambda x: To_TimestampSEC(x))
Form_File['Status Changed_Sec'] = Form_File['Status Changed'].apply(lambda x: To_TimestampSEC(x))

## 3. Time Related Calculation
Form_File['Create_to_Last_StatusChanged(s)'] = Form_File['Status Changed_Sec']- Form_File['Created_Sec']
Form_File['Create_to_Last_StatusChanged(weeks)'] = Form_File['Create_to_Last_StatusChanged(s)'].apply(lambda x: x// (3600*24*7))
Form_File['Create_to_Last_StatusChanged(days)'] = Form_File['Create_to_Last_StatusChanged(s)'].apply(lambda x: x// (3600*24))

Form_File = Form_File[Form_File["Type"] == 'Safety Forms'] 
print(Form_File.head())

Form_File.to_csv('Safety_Form.csv')

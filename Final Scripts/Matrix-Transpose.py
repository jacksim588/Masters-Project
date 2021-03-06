import pandas as pd
import numpy as np

directory = r'C:\Users\Clamfighter\Machine_Learning_Project\my_env\Masters\T2_5679_predicted_crystals\JS_Low_Energy_MM(200).csv'
df = pd.read_csv(directory, index_col=[0])
max = np.nanmax(df.values)#gets max value in dataframe
df = df.add(df.T, fill_value=0)#creates a transposed matrix, and adds it to the orignal
df=df.replace(max*2,max)#matched molecules will double value when i,j are the same, replace with original value
df.to_csv(directory[:-4]+'(full).csv')
print(directory[:-4]+'(full).csv')
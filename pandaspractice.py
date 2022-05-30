import pandas as pd
import numpy as np

df = pd.read_csv("C:/Users/ravi/Downloads/BTU.csv")
print(df)
print(df.shape)
print(df.iloc[2:3,5:])
print(df[df['Temperature (DegC)']=='--']) # or has below
print(df[df[2:]=='--'])
print(df[(df['Temperature (DegC)']=='--')|(df['Temperature (DegC)']=='--')].index)
print(df.iloc[1:])
print(df.dropna())
print(df.fillna({'CHWR':df['CHWR'].mean(),'CHWS':df['CHWS'].mean(),'Flow':df['Flow'].mean(),'Load':df['Load'].mean()}))


# Python program to illustrate
# creating a data frame using CSV files

# import pandas module


import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile

# creating a data frame

df = pd.read_excel('/Users/macbookpro/Documents/Database.xlsx')

print(df.LP.values)









def CheckLicencePlate(df, v):
    result = {}

    for element in v:
        if element in df.values:
            result[element] = True
        else:
            result[element] = False

    return result


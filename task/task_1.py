import pandas as pd

# Read files
table_0 = pd.ExcelFile("data/Table_0.xlsx")
table_1 = pd.read_csv("data/Table_1.csv")
table_2 = pd.ExcelFile("data/Table_0.xlsx")

# Read sheets
table_0 = list({sheet_name: table_0.parse(sheet_name) for sheet_name in table_0.sheet_names}.values())[0]
table_2 = list({sheet_name: table_2.parse(sheet_name) for sheet_name in table_2.sheet_names}.values())[0]

print(table_0.head())
print(table_1.head())
print(table_2.head())

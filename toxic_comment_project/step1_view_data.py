import pandas as pd

# Load dataset
data = pd.read_csv("train.csv")

# Show first 5 rows
print(data.head())

# Show number of rows
print("Total rows:", len(data))
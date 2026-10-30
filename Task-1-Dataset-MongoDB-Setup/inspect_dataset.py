
import pandas as pd
import os

# Dataset path
file_path = os.path.join("dataset", "weatherAUS.csv")

# Load dataset
df = pd.read_csv(file_path)

print("\n========== WEATHER DATASET INSPECTION ==========\n")

# 1. Dataset overview
print("1. DATASET OVERVIEW")
print("Dataset Name       : WeatherAUS")
print("Total Records      :", f"{len(df):,}")
print("Total Columns      :", len(df.columns))
print("File Size          :", 
      f"{os.path.getsize(file_path) / (1024 * 1024):.2f} MB")

# 2. Column information
print("\n2. IMPORTANT COLUMNS")
important_columns = [
    "Date", "Location", "MinTemp", "MaxTemp",
    "Rainfall", "Humidity9am", "Humidity3pm",
    "WindSpeed9am", "WindSpeed3pm",
    "RainToday", "RainTomorrow"
]

print(", ".join(important_columns))

# 3. Location information
print("\n3. LOCATION DETAILS")
print("Unique Locations   :", df["Location"].nunique())
print("Sample Locations   :",
      ", ".join(df["Location"].dropna().unique()[:5]))

# 4. Date range
print("\n4. DATE RANGE")
print("Start Date         :", df["Date"].min())
print("End Date           :", df["Date"].max())

# 5. Missing values summary
print("\n5. MISSING VALUES")
total_missing = df.isnull().sum().sum()
total_cells = df.size

print("Missing Cells      :", f"{total_missing:,}")
print("Missing Percentage :",
      f"{(total_missing / total_cells) * 100:.2f}%")

print("\nColumns with most missing values:")
missing = df.isnull().sum().sort_values(ascending=False)
for column, count in missing.head(5).items():
    print(f"{column}: {count:,}")

# 6. Target variable distribution
print("\n6. RAIN TOMORROW DISTRIBUTION")
print(df["RainTomorrow"].value_counts(dropna=False).to_string())

# 7. Sample records
print("\n7. SAMPLE DATA (FIRST 3 RECORDS)")
print(df[important_columns].head(3).to_string(index=False))

print("\n========== INSPECTION COMPLETED ==========\n")

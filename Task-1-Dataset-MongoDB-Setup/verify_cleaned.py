
import pandas as pd
import os

file_path = "dataset/cleaned_weather.csv"

df = pd.read_csv(file_path)

print("\n===== CLEANED DATASET VERIFICATION =====")

print("File exists:", os.path.exists(file_path))
print("Total records:", len(df))
print("Total columns:", len(df.columns))
print("File size:", round(os.path.getsize(file_path) / (1024 * 1024), 2), "MB")

print("\nFirst 3 records:")
print(df[["Date", "Location", "MinTemp", "MaxTemp", "Rainfall"]].head(3).to_string(index=False))

print("\nData types:")
print(df[["Date", "Location", "MinTemp", "MaxTemp", "Rainfall"]].dtypes)

print("\n===== VERIFICATION COMPLETED =====")

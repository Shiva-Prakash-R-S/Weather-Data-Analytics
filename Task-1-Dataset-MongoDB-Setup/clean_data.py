
import pandas as pd
import os

# =====================================
# 1. FILE PATHS
# =====================================

input_file = "dataset/weatherAUS.csv"
output_file = "dataset/cleaned_weather.csv"

print("\n========== WEATHER DATA CLEANING ==========\n")

# =====================================
# 2. LOAD DATASET
# =====================================

df = pd.read_csv(input_file)

original_records = len(df)

print("Original Records:", original_records)

# =====================================
# 3. REMOVE DUPLICATE RECORDS
# =====================================

duplicates = df.duplicated().sum()
df = df.drop_duplicates()

print("Duplicate Records Removed:", duplicates)

# =====================================
# 4. CLEAN TEXT COLUMNS
# =====================================

text_columns = df.select_dtypes(
    include=["object"]
).columns

for column in text_columns:
    df[column] = df[column].apply(
        lambda x: x.strip() if isinstance(x, str) else x
    )

# =====================================
# 5. CONVERT DATE COLUMN
# =====================================

df["Date"] = pd.to_datetime(
    df["Date"],
    errors="coerce"
)

# =====================================
# 6. CONVERT NUMERIC COLUMNS
# =====================================

numeric_columns = [
    "MinTemp", "MaxTemp", "Rainfall",
    "Evaporation", "Sunshine", "WindGustSpeed",
    "WindSpeed9am", "WindSpeed3pm",
    "Humidity9am", "Humidity3pm",
    "Pressure9am", "Pressure3pm",
    "Cloud9am", "Cloud3pm", "Temp9am", "Temp3pm"
]

for column in numeric_columns:
    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )

# =====================================
# 7. NORMALIZE WEATHER LABELS
# =====================================

for column in ["RainToday", "RainTomorrow"]:
    df[column] = df[column].replace({
        "Yes": "Yes",
        "No": "No"
    })

# =====================================
# 8. REMOVE INVALID ESSENTIAL RECORDS
# =====================================

before_removal = len(df)

df = df.dropna(
    subset=["Date", "Location"]
)

invalid_records = before_removal - len(df)

# =====================================
# 9. SAVE CLEANED DATASET
# =====================================

df.to_csv(
    output_file,
    index=False,
    date_format="%Y-%m-%d"
)

# =====================================
# 10. CLEANING SUMMARY
# =====================================

print("\n========== CLEANING SUMMARY ==========\n")

print("Original Records       :", original_records)
print("Duplicates Removed     :", duplicates)
print("Invalid Records Removed:", invalid_records)
print("Final Records          :", len(df))
print("Total Columns          :", len(df.columns))

print(
    "Remaining Missing Cells:",
    f"{df.isnull().sum().sum():,}"
)

print(
    "Missing Data Percentage:",
    f"{df.isnull().sum().sum() / df.size * 100:.2f}%"
)

print("\nCleaned Dataset Saved At:")
print(output_file)

print("\n========== CLEANING COMPLETED ==========\n")

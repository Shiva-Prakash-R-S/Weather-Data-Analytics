
import pandas as pd
from pymongo import MongoClient
from datetime import datetime

# 1. Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")

# 2. Select database and collection
db = client["weather_analytics"]
collection = db["weather_records"]

print("\n===== WEATHER DATA MONGODB IMPORT =====")

# 3. Check MongoDB connection
client.admin.command("ping")
print("MongoDB Connection: Successful")

# 4. Read cleaned dataset
df = pd.read_csv("dataset/cleaned_weather.csv")

print("Dataset Records:", len(df))

# 5. Convert Date into datetime format
df["Date"] = pd.to_datetime(
    df["Date"],
    errors="coerce"
)

# 6. Convert missing values into None
df = df.astype(object).where(pd.notna(df), None)

# Convert pandas timestamps to Python datetime
df["Date"] = df["Date"].apply(
    lambda x: x.to_pydatetime()
    if pd.notna(x) else None
)

# 7. Check whether data is already imported
existing_records = collection.count_documents({})

if existing_records > 0:
    print("Existing MongoDB records:", existing_records)
    print("Import skipped to prevent duplicate insertion.")

else:
    records = df.to_dict("records")

    # 8. Insert records in batches
    batch_size = 5000

    for i in range(0, len(records), batch_size):
        batch = records[i:i + batch_size]
        collection.insert_many(batch)

        print(
            f"Imported {min(i + batch_size, len(records))}"
            f" / {len(records)} records"
        )

# 9. Display final database details
print("\n===== IMPORT SUMMARY =====")

print("Database:", db.name)
print("Collection:", collection.name)
print("Total Documents:", collection.count_documents({}))

# 10. Display sample document
print("\nSample Weather Record:")

sample = collection.find_one(
    {},
    {"_id": 0}
)

print(sample)

print("\n===== IMPORT COMPLETED =====")

client.close()

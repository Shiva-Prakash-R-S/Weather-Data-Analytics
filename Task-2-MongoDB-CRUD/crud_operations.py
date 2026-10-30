
from pymongo import MongoClient
from datetime import datetime

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")

# Select database and collection
db = client["weather_analytics"]
collection = db["weather_records"]

print("MongoDB Connected Successfully!")


# CREATE OPERATION
# Insert a new weather record

new_weather = {
    "Date": datetime(2026, 10, 30),
    "Location": "Test_Location",
    "MinTemp": 18.5,
    "MaxTemp": 29.5,
    "Rainfall": 5.2,
    "Humidity9am": 75.0,
    "Humidity3pm": 60.0,
    "RainToday": "Yes",
    "RainTomorrow": "No"
}

result = collection.insert_one(new_weather)

print("\n===== CREATE OPERATION =====")
print("New weather record inserted successfully!")
print("Inserted Document ID:", result.inserted_id)


# READ OPERATION

print("\n===== READ OPERATION =====")

# 1. Count total weather records
total_records = collection.count_documents({})
print("Total Weather Records:", total_records)


# 2. Retrieve first 5 records
print("\nFirst 5 Weather Records:")

records = collection.find().limit(5)

for record in records:
    print({
        "Location": record.get("Location"),
        "Date": record.get("Date"),
        "MinTemp": record.get("MinTemp"),
        "MaxTemp": record.get("MaxTemp"),
        "Rainfall": record.get("Rainfall")
    })


# 3. Retrieve records for Albury
print("\nWeather Records for Albury:")

albury_records = collection.find(
    {"Location": "Albury"}
).limit(5)

for record in albury_records:
    print({
        "Location": record.get("Location"),
        "MaxTemp": record.get("MaxTemp"),
        "Rainfall": record.get("Rainfall")
    })


# UPDATE OPERATION

print("\n===== UPDATE OPERATION =====")

# Find and update the test weather record
result = collection.update_one(
    {
        "Location": "Test_Location",
        "Date": datetime(2026, 10, 30)
    },
    {
        "$set": {
            "MaxTemp": 31.5,
            "Rainfall": 8.0
        }
    }
)

print("Matched Documents:", result.matched_count)
print("Modified Documents:", result.modified_count)

# Display updated record
updated_record = collection.find_one({
    "Location": "Test_Location",
    "Date": datetime(2026, 10, 30)
})

print("\nUpdated Weather Record:")

print(updated_record)


# DELETE OPERATION

print("\n===== DELETE OPERATION =====")

# Delete test weather records
result = collection.delete_many({
    "Location": "Test_Location"
})

print("Deleted Documents:", result.deleted_count)

# Verify deletion
remaining_records = collection.count_documents({
    "Location": "Test_Location"
})

print("Remaining Test Records:", remaining_records)

if remaining_records == 0:
    print("Test records deleted successfully!")


client.close()



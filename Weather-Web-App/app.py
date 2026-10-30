
import os
from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from bson import ObjectId
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static")
)
app.secret_key = "weather_project_secret"

# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")

db = client["weather_analytics"]
collection = db["weather_records"]


# Home Dashboard
@app.route("/")
def dashboard():

    try:
        total_records = collection.count_documents({})

        total_locations = len(
            collection.distinct("Location")
        )

        records = list(
            collection.find().sort("Date", -1).limit(8)
        )

        return render_template(
            "dashboard.html",
            total_records=total_records,
            total_locations=total_locations,
            records=records
        )

    except PyMongoError:
        flash("MongoDB connection failed!", "error")
        return render_template(
            "dashboard.html",
            total_records=0,
            total_locations=0,
            records=[]
        )


# CRUD Page
@app.route("/crud")
def crud():

    records = list(
        collection.find().sort("Date", -1).limit(100)
    )

    return render_template(
        "crud.html",
        records=records
    )


# CREATE Operation
@app.route("/create", methods=["POST"])
def create():

    try:
        record = {
            "Date": datetime.strptime(
                request.form["Date"], "%Y-%m-%d"
            ),
            "Location": request.form["Location"],
            "MinTemp": float(request.form["MinTemp"]),
            "MaxTemp": float(request.form["MaxTemp"]),
            "Rainfall": float(request.form["Rainfall"]),
            "RainToday": request.form["RainToday"]
        }

        collection.insert_one(record)

        flash("Weather record added successfully!", "success")

    except (ValueError, KeyError, PyMongoError) as error:
        flash(f"Could not add record: {error}", "error")

    return redirect(url_for("crud"))


# DELETE Operation
@app.route("/delete/<record_id>", methods=["POST"])
def delete(record_id):

    try:
        collection.delete_one({
            "_id": ObjectId(record_id)
        })

        flash("Record deleted successfully!", "success")

    except Exception:
        flash("Unable to delete record.", "error")

    return redirect(url_for("crud"))


# UPDATE Page
@app.route("/edit/<record_id>")
def edit(record_id):

    record = collection.find_one({
        "_id": ObjectId(record_id)
    })

    if record is None:
        flash("Record not found.", "error")
        return redirect(url_for("crud"))

    return render_template(
        "edit.html",
        record=record
    )


# UPDATE Operation
@app.route("/update/<record_id>", methods=["POST"])
def update(record_id):

    try:
        updated_data = {
            "Date": datetime.strptime(
                request.form["Date"], "%Y-%m-%d"
            ),
            "Location": request.form["Location"],
            "MinTemp": float(request.form["MinTemp"]),
            "MaxTemp": float(request.form["MaxTemp"]),
            "Rainfall": float(request.form["Rainfall"]),
            "RainToday": request.form["RainToday"]
        }

        collection.update_one(
            {"_id": ObjectId(record_id)},
            {"$set": updated_data}
        )

        flash("Record updated successfully!", "success")

    except (ValueError, KeyError, PyMongoError):
        flash("Unable to update record.", "error")

    return redirect(url_for("crud"))


@app.route("/analytics")
def analytics():

    # 1. Average temperature by location
    temperature = list(collection.aggregate([
        {
            "$group": {
                "_id": "$Location",
                "min": {"$avg": "$MinTemp"},
                "max": {"$avg": "$MaxTemp"}
            }
        },
        {"$sort": {"_id": 1}}
    ]))

    # 2. Top 10 rainfall locations
    rainfall = list(collection.aggregate([
        {
            "$match": {
                "Rainfall": {"$type": "number"}
            }
        },
        {
            "$group": {
                "_id": "$Location",
                "total": {"$sum": "$Rainfall"}
            }
        },
        {"$sort": {"total": -1}},
        {"$limit": 10}
    ]))

    # 3. Rain today distribution
    rainy = list(collection.aggregate([
        {
            "$match": {
                "RainToday": {"$in": ["Yes", "No"]}
            }
        },
        {
            "$group": {
                "_id": "$RainToday",
                "count": {"$sum": 1}
            }
        }
    ]))

    # 4. Average humidity by location
    humidity = list(collection.aggregate([
        {
            "$group": {
                "_id": "$Location",
                "nine": {"$avg": "$Humidity9am"},
                "three": {"$avg": "$Humidity3pm"}
            }
        },
        {"$sort": {"nine": -1}},
        {"$limit": 15}
    ]))

    # Prepare chart data
    data = {
        "temperature": [
            {
                "location": item["_id"],
                "min": round(item["min"], 2) if item.get("min") is not None else None,
                "max": round(item["max"], 2) if item.get("max") is not None else None
            }
            for item in temperature
        ],

        "rainfall": [
            {
                "location": item["_id"],
                "total": round(item["total"], 2) if item.get("total") is not None else 0
            }
            for item in rainfall
        ],

        "rainy": [
            {
                "label": item["_id"],
                "count": item["count"]
            }
            for item in rainy
        ],

        "humidity": [
            {
                "location": item["_id"],
                "nine": round(item["nine"], 2) if item.get("nine") is not None else None,
                "three": round(item["three"], 2) if item.get("three") is not None else None
            }
            for item in humidity
        ]
    }

    print("\n===== RAINFALL DEBUG =====")
    print("Number of locations:", len(rainfall))
    print("Rainfall results:", rainfall)

    return render_template(
        "analytics.html",
        data=data
    )


# Run Application
if __name__ == "__main__":
    app.run(debug=True)

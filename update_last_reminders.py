from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime

# MongoDB
uri = "mongodb+srv://cm44228:XMq8lmQDpOUsK2cT@furbot.dmsu2.mongodb.net/"

client = MongoClient(uri)
db = client["furbot"]
reminders = db["reminders"]
pets = db["pets"]

# Step 1: Loop through reminders and find latest per type per pet
pet_reminders = {}

for reminder in reminders.find():
    pet_id = str(reminder["pet_id"])
    r_type = reminder["type"]
    r_date = datetime.strptime(reminder["date"], "%Y-%m-%d")

    if pet_id not in pet_reminders:
        pet_reminders[pet_id] = {}

    # Store most recent reminder per type
    if r_type not in pet_reminders[pet_id] or r_date > pet_reminders[pet_id][r_type]:
        pet_reminders[pet_id][r_type] = r_date

# Step 2: Update each pet in the database with lastReminders field
for pet_id, reminders_dict in pet_reminders.items():
    formatted_reminders = {k: v.strftime("%Y-%m-%d") for k, v in reminders_dict.items()}
    pets.update_one(
        {"_id": ObjectId(pet_id)},
        {"$set": {"lastReminders": formatted_reminders}}
    )

print("Pets updated with lastReminders.")

import os
from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Securely load SECRET_KEY from .env
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

# Connect to MongoDB
client = MongoClient(os.getenv("MONGO_URI"))
db = client["furbot"]  # Database name
users = db["users"]  # Users collection
pets = db["pets"] # Pets collection

# ------------------------------
# API: Add a new pet
# ------------------------------
@app.route("/pets", methods=["POST"]) 
def add_pet():
    data = request.json

    #Validate input
    if "owner_id" not in data or "name" not in data or "dob" not in data:
        return jsonify({"error": "Missing required fields (owner_id), name, dob"}), 400
    
    try:
        owner_obj_id = ObjectId(data["owner_id"]) # validate owner_id format

    except Exception:
        return jsonify({"error": "Invalid owner_id format"}), 400
        
    # Check if pet already exists for the owner
    existing_pet = pets.find_one({"owner_id": owner_obj_id, "name": data["name"]})
    if existing_pet:
        return jsonify({"error": "A Pet with this name already exists for the owner"}), 400
        
    #Insert pet into the database
    pet_id = pets.insert_one({
        "owner_id": ObjectId(data["owner_id"]),
        "name": data["name"],
        "species": data.get("species", ""),
        "dob": data["dob"], #(format: YYYY-MM-DD)
        "color": data.get("color", ""),
        "breed": data.get("breed", ""),
        "medical_history": data.get("medical_history", []),
        "created_at": datetime.datetime.now(datetime.timezone.utc)
    }).inserted_id

    return jsonify({"message": "Pet added successfully", "pet_id": str(pet_id)}), 201

# ------------------------------
# API: Get all pets of an owner
# ------------------------------
@app.route("/pets/<owner_id>", methods=["GET"])
def get_pets(owner_id):
    try:
        owner_obj_id = ObjectId(owner_id)  # Validate owner_id format
    except Exception:
        return jsonify({"error": "Invalid owner_id format"}), 400


    pets_list = list(pets.find({"owner_id": owner_obj_id}, {"_id": 1, "name": 1, "species": 1, "breed": 1, "dob": 1, "medical_history": 1}))

    if not pets_list:
        return jsonify({"message": "No pets found for the owner"}), 404
        
    # Convert ObjectId to string before returning the response
    today = datetime.date.today()

    for pet in pets_list:
        pet["_id"] = str(pet["_id"])

        # Calculate the age of the pet
        if "dob" in pet:
            dob = datetime.datetime.strptime(pet["dob"], "%Y-%m-%d").date()

            age = today.year - dob.year
            if (today.month, today.day) < (dob.month, dob.day):
                age -= 1 # Subtract if the birthday hasn't occurred yet

            pet["age"] = age
        else:
            pet["age"] = "Unknown"

    return jsonify(pets_list), 200


# ------------------------------
# API: Delete a pet
# ------------------------------
@app.route("/pets/<pet_id>", methods=["DELETE"])
def delete_pet(pet_id):
    try:
        ObjectId(pet_id)  # Validate pet_id format
    except Exception:
        return jsonify({"error": "Invalid pet_id format"}), 400

    # Check if pet exists
    pet = pets.find_one({"_id": ObjectId(pet_id)})
    if not pet:
        return jsonify({"error": "Pet not found"}), 404

    pets.delete_one({"_id": ObjectId(pet_id)})
    return jsonify({"message": "Pet deleted successfully"}), 200


# ------------------------------
# User Registration API
# ------------------------------
@app.route("/register", methods=["POST"])
def register():
    data = request.json

    # Check if email already exists
    if users.find_one({"email": data["email"]}):
        return jsonify({"error": "Email already exists"}), 400

    # Hash the password before storing
    hashed_password = generate_password_hash(data["password"])
    users.insert_one({"email": data["email"], "password": hashed_password})
    return jsonify({"message": "User registered successfully!"}), 201


# ------------------------------
# User Login API
# ------------------------------
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    user = users.find_one({"email": data["email"]})

    # Verify password
    if user and check_password_hash(user["password"], data["password"]):
        # Generate a JWT token (valid for 1 hour)
        token = jwt.encode(
            {"email": data["email"], "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)},
            app.config["SECRET_KEY"],
            algorithm="HS256",
        )
        return jsonify({"token": token, "user_id": str(user["_id"])}), 200  # Return token to client

    return jsonify({"error": "Invalid credentials"}), 401


# ------------------------------
# Run Flask App
# ------------------------------
if __name__ == "__main__":
    app.run(debug=True)
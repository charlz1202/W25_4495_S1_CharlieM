import os # This is for environment variables
from flask import Flask, request, jsonify, send_from_directory # This is for Flask web framework
import logging # This is for logging used for devbugging and error tracking
from flask_cors import CORS, cross_origin # This is for Cross-Origin Resource Sharing
from flask_mail import Mail, Message # This is for sending emails
from pymongo import MongoClient # This is for MongoDB connection
from bson.objectid import ObjectId # This is for MongoDB ObjectId handling
import requests # This is for making HTTP requests to the Yelp API
from werkzeug.security import generate_password_hash, check_password_hash # This is for password hashing and checking
import jwt # This is for JWT token generation and verification
import pytz # This is for timezone handling
import datetime # This is for date and time handling
from dotenv import load_dotenv # This is for loading environment variables from a .env file
from flask_apscheduler import APScheduler # This is for scheduling tasks
from fuzzywuzzy import fuzz  # This is for string matching algorithm



# These are the types of reminders we support in the app
reminder_type_aliases = {
    "grooming": "Grooming",
    "groom": "Grooming",
    "groomin": "Grooming",
    "haircut": "Grooming",
    "vaccine": "Vaccination",
    "vaccination": "Vaccination",
    "vaccines": "Vaccination",
    "booster": "Vaccination",
    "shots": "Vaccination",
    "inoculation": "Vaccination",
    "immunization": "Vaccination",
    "dose": "Vaccination",
    "jab": "Vaccination",
    "vaccinate": "Vaccination",
}



# This is to load the .env file in development mode
if os.getenv("FLASK_ENV") != "production":
    load_dotenv()


# Configure logging for debugging
logging.basicConfig(level=logging.INFO)

# Used for productionInitialize Flask app and set static folder for frontend
# When a user visits your site (like /, /login, /dashboard, etc.):
# Flask checks ../frontend/dist for a matching file
# If it finds one, it serves that file (like index.html or app.js).
# If it doesn't find one, it returns a 404 error.
app = Flask(__name__, static_folder="../frontend/dist")


# Initialize APScheduler
scheduler = APScheduler()
scheduler.init_app(app)

# Define API Prefix for production and development
# In production, the API prefix is "/api" to avoid conflicts with frontend routes
IS_PRODUCTION = os.getenv("FLASK_ENV") == "production"
API_PREFIX = "/api" if IS_PRODUCTION else ""

# Print environment variables for debugging
print("FLASK_ENV:", os.getenv("FLASK_ENV"))
print("Running in PRODUCTION?" , os.getenv("FLASK_ENV") == "production")
print("REGISTERED ROUTE:", f"{API_PREFIX}/login") # Debugging route for login

# Handle CORS Globally
allowed_origins = os.getenv("CORS_ORIGINS", "*").split(",") # Comma-separated list of allowed origins
print("Allowed CORS Origins:", allowed_origins)
CORS(app,
     origins=allowed_origins,
     supports_credentials=True,
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     allow_headers=["Content-Type", "Authorization"])


# Serve Vue.js frontend files
# This is the route that serves the Vue.js frontend files.
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_vue(path):
    if path and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, "index.html")


# Set up MongoDB connection
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
client = MongoClient(os.getenv("MONGO_URI"))
db = client["furbot"]  # Database name
users = db["users"]    # Users collection
pets = db["pets"]      # Pets collection
reminders = db["reminders"]  # Reminders collection
favorites =db["favorites"] # Collection to store user's saved businesses from yelp results

# Load Yelp API Key
YELP_API_KEY = os.getenv("YELP_API_KEY")

# --------------------------------
# Config: Flask-Mail Configuration
# --------------------------------
app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER")
app.config["MAIL_PORT"] = int(os.getenv("MAIL_PORT"))
app.config["MAIL_USE_SSL"] = os.getenv("MAIL_USE_SSL").lower() == "true"
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_DEFAULT_SENDER")

mail = Mail(app)

def send_email(to_email, subject, body):
    msg = Message(subject, recipients=[to_email])
    msg.body = body
    mail.send(msg)

# ------------------------------------------
# API: Saving a favorite result to favorites  
# -------------------------------------------
@app.route(f"{API_PREFIX}/favorites", methods=["POST"])
def add_favorite():
    data = request.json

    try:
        # to prevent duplicate entries, check if the user already has this favorite
        existing = favorites.find_one({
            "owner_id": ObjectId(data["owner_id"]),
            "business_id": data["business_id"]
        })
        if existing:
            return jsonify({"error": "This is already in your favorites."}), 200
        
        data["owner_id"] = ObjectId(data["owner_id"]) # Convert owner_id to ObjectId
        favorites.insert_one(data) # Insert the favorite into the database
        return jsonify({"message": "Favorite added successfully!"}), 201
    except Exception as e:
        print("Error adding favorite:", str(e))
        return jsonify({"error": "Failed to add favorite"}), 500



# ------------------------------------------
# API: Get all favorites for a user
# ------------------------------------------
@app.route(f"{API_PREFIX}/favorites/<owner_id>", methods=["GET"])
def get_favorites(owner_id):
    try:
        owner_obj_id = ObjectId(owner_id)  # Validate owner_id format
    except Exception:
        return jsonify([]), 200  # Return empty list if invalid owner_id

    favorites_list = list(favorites.find({"owner_id": owner_obj_id}, {"_id": 1, "business_id": 1, "owner_id": 1, "name": 1, "image_url": 1, "rating": 1, "location": 1})) # Get all favorites for the user

    # Convert ObjectId to string before returning the response
    for favorite in favorites_list:
        favorite["_id"] = str(favorite["_id"])
        favorite["owner_id"] = str(favorite.get("owner_id", "unknown"))

    return jsonify(favorites_list), 200



# ------------------------------------------
# API: Delete a favorite
# ------------------------------------------
@app.route(f"{API_PREFIX}/favorites/<favorite_id>", methods=["DELETE"])
def delete_favorite(favorite_id):
    try:
        favorite_obj_id = ObjectId(favorite_id)  # Validate favorite_id format
    except Exception:
        return jsonify({"error": "Invalid favorite_id format"}), 400

    # Check if favorite exists
    favorite = favorites.find_one({"_id": favorite_obj_id})
    if not favorite:
        return jsonify({"error": "Favorite not found"}), 404

    favorites.delete_one({"_id": favorite_obj_id})
    return jsonify({"message": "Favorite deleted successfully"}), 200




# ------------------------------
# API: Yelp Search  
# ------------------------------
@app.route(f"{API_PREFIX}/yelp/search", methods=["GET"])
def yelp_search():
    location = request.args.get("location")
    term = request.args.get("term")
    category = request.args.get("category", "petstores,groomer,vets,petservices,petphotography,pet_sitting") # Categories according to Yelp API

    headers = {
        "Authorization": f"Bearer {YELP_API_KEY}",
        "Content-Type": "application/json"
    }

    print("Using API Key:", "Yes" if YELP_API_KEY else "Missing") # Debugging

    url = f"https://api.yelp.com/v3/businesses/search?term={term}&location={location}&categories={category}"

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Yelp API Error Response:", response.status_code, response.text)

    return response.json() if response.status_code == 200 else {"error": "Failed to fetch Yelp data"}

# ------------------------------
# API: Add a Reminder
# ------------------------------
@app.route(f"{API_PREFIX}/reminders", methods=["POST"])
def add_reminder():
    data = request.json

    # Validate input
    if "owner_id" not in data or "pet_id" not in data or "date" not in data:
        print("Missing required fields", data)
        return jsonify({"error": "Missing required fields (owner_id, pet_id, date)"}), 400
    
    try:
        owner_obj_id = ObjectId(data["owner_id"])
        pet_obj_id = ObjectId(data["pet_id"])
    except Exception as e:
        print("Invalid owner_id or pet_id format", str(e))
        return jsonify({"error": "Invalid owner_id or pet_id format"}), 400
    
    try: 

         # Normalize the reminder type using aliases on top of this code
        user_type = data.get("type", "Other").lower()
        normalized_type = reminder_type_aliases.get(user_type, user_type.title())


        reminder_id = reminders.insert_one({
            "owner_id": owner_obj_id,
            "pet_id": pet_obj_id,
            "date": data["date"],  # (format: YYYY-MM-DD)
            "type": normalized_type,
            "notes": data.get("notes", ""),
            "status": "Pending"
        }).inserted_id

        print("Reminder added successfully", reminder_id)

        # Update the pet's lastReminders field for the proactive reminder check
        pets.update_one(
            {"_id": pet_obj_id},
            {"$set": {f"lastReminders.{normalized_type}": data["date"]}}
        )  

        return jsonify({"message": "Reminder added successfully", "reminder_id": str(reminder_id)}), 201

    except Exception as e:
        print("Error adding reminder", str(e))
        return jsonify({"error": "Error adding reminder"}), 500

# ------------------------------
# API: Get Reminders for a pet
# ------------------------------
@app.route(f"{API_PREFIX}/reminders/<pet_id>", methods=["GET"])
def get_reminders(pet_id):
    try:
        pet_obj_id = ObjectId(pet_id)  # Validate pet_id format
    except Exception:
        return jsonify({"error": "Invalid pet_id format"}), 400

    reminders_list = list(reminders.find({"pet_id": pet_obj_id}, 
                                         {"_id": 1, "date": 1, "type": 1, "notes": 1, "status": 1, "pet_id": 1}))

    if not reminders_list:
        return jsonify({"message": "No reminders found for this pet"}), 404

    # Convert ObjectId to string before returning the response
    for reminder in reminders_list:
        reminder["_id"] = str(reminder["_id"])
        reminder["pet_id"] = str(reminder.get("pet_id", "unknown"))

    return jsonify(reminders_list), 200

# ------------------------------------
# API: Get All Reminders for an owner
# ------------------------------------
@app.route(f"{API_PREFIX}/reminders/owner/<owner_id>", methods=["GET"])
def get_all_reminders(owner_id):
    try:
        owner_obj_id = ObjectId(owner_id)  # Validate owner_id format
    except Exception:
        return jsonify({"error": "Invalid owner_id format"}), 400       
    
    reminders_list = list(reminders.find({"owner_id": owner_obj_id},
                                         {"_id": 1, "date": 1, "type": 1, "notes": 1, "status": 1, "pet_id": 1}))
    
    if not reminders_list:
        return jsonify({"message": "No reminders found for this owner"}), 404   
    
    # Convert ObjectId to string before returning the response
    for reminder in reminders_list:
        reminder["_id"] = str(reminder["_id"])
        reminder["pet_id"] = str(reminder.get("pet_id", "unknown"))

    return jsonify(reminders_list), 200


# ------------------------------
# API: Delete a Reminder
# ------------------------------
@app.route(f"{API_PREFIX}/reminders/<reminder_id>", methods=["DELETE"])
def delete_reminder(reminder_id):
    try:
        reminder_obj_id = ObjectId(reminder_id)  # Validate reminder_id format
    except Exception:
        return jsonify({"error": "Invalid reminder_id format"}), 400
    
    # Check if reminder exists
    reminder = reminders.find_one({"_id": reminder_obj_id})
    if not reminder:
        return jsonify({"error": "Reminder not found"}), 404

    pet_id = reminder["pet_id"] # Get the pet_id from the reminder
    reminder_type = reminder["type"] # Get the type of the reminder
    
    # Update the pets lastReminders field to remove the deleted reminder
    result = reminders.delete_one({"_id": reminder_obj_id})

    if result.deleted_count == 0:
        return jsonify({"error": "Reminder not found"}), 404
    
    # Check if there are other reminders of this type for this pet
    latest_reminder = reminders.find_one(
        {"pet_id": pet_id, "type": reminder_type},
        sort=[("date", -1)]  # Get the date of most recent remaining reminder
    )

    if latest_reminder:
        # Update lastReminders with the new most recent date
        pets.update_one(
            {"_id": pet_id},
            {"$set": {f"lastReminders.{reminder_type}": latest_reminder["date"]}}
        )
    else:
        # No more reminders of this type — remove the field
        pets.update_one(
            {"_id": pet_id},
            {"$unset": {f"lastReminders.{reminder_type}": ""}}
        )
    
    return jsonify({"message": "Reminder deleted successfully"}), 200


# -------------------------------------------------------------
# JOB: Scheduler for upcoming reminders and proactive reminders
# -------------------------------------------------------------
def check_reminders():
    vancouver_tz = pytz.timezone("America/Vancouver") # Set timezone to Vancouver
    # Set the date to the current date in Vancouver timezone
    today = datetime.datetime.now(vancouver_tz).date()
    print("Running check_reminders for:", today) # Console log for debugging
    
    # Fetch reminders for today
    reminders_list = list(reminders.find({"date": str(today), "status": "Pending"}))
    print("Reminders found:", len(reminders_list)) # Console log for debugging

    # If no reminders found, log and return
    if not reminders_list:
        logging.info("No reminders for today")
        return

    # Iterate through each reminder
    for reminder in reminders_list:
        # Retrieve pet and owner details
        pet = pets.find_one({"_id": reminder["pet_id"]})
        if not pet:
            logging.warning(f"Pet not found for reminder: {reminder}")
            continue
        
        # Retrieve owner details
        owner = users.find_one({"_id": reminder["owner_id"]})
        if not owner:
            logging.warning(f"Owner not found for reminder: {reminder}")
            continue

        # Log reminder details
        logging.info(f"Reminder for {pet['name']} ({pet['species']})")
        logging.info(f"Owner: {owner['email']}")
        logging.info(f"Type: {reminder['type']}")
        logging.info(f"Notes: {reminder['notes']}")
        logging.info("----------------------------")

        # Send email reminder to the owner
        email_body = (
            f"Hello {owner['email']},\n\n"
            f"This is a reminder for {pet['name']}'s {reminder['type']} today.\n"
            f"Notes: {reminder['notes']}\n\n"
            "Regards,\nFurbot"
        )

        send_email(owner["email"], "Furbot Reminder", email_body)
            
        # Update reminder status to "Completed" so it won't be sent again
        reminders.update_one({"_id": reminder["_id"]}, {"$set": {"status": "Completed"}})
        logging.info("Reminder status updated to Completed")


# Schedule the job to run
scheduler.add_job(id="check_reminders", func=check_reminders, trigger="cron", minute="*") # For testing, run every minute



# Function to check proactive reminders
def check_proactive_reminders():
    vancouver_tz = pytz.timezone("America/Vancouver") # Set timezone to Vancouver
    today = datetime.datetime.now(vancouver_tz).date() # Set the date to the current date in Vancouver timezone
    print("Running check_proactive_reminders for:", today) # Console log for debugging

    reminder_gap_days = {
        "Grooming": 30, # Grooming reminders every 30 days
        "Vaccination": 365, # Vaccination reminders every 365 days
    }

    pets_found = 0
    suggestions_made = 0

    # Fetch all pets and their last reminders
    for pet in pets.find():
        pets_found += 1 # Count the number of pets found
        pet_name = pet.get("name", "your pet") # Get the pet name or default to "your pet"
        owner_id = pet.get("owner_id") # Get the owner ID
        last_reminders = pet.get("lastReminders", {}) # Dictionary to hold last reminder dates
        suggested = [] # List to hold suggested reminders

        
        for reminder_type, max_days in reminder_gap_days.items():  # Check for each reminder type 
            last_date_str = last_reminders.get(reminder_type) # Get the last reminder date for the type
            if not last_date_str: # If no last reminder date, skip this type
                continue

            last_date = datetime.datetime.strptime(last_date_str, "%Y-%m-%d").date() # Convert string to date
            if (today - last_date).days >= max_days: # Check if the gap exceeds the threshold
                # Suggest a new reminder    
                message = (
                    f"It's been over {max_days} days since your last {reminder_type.lower()} for {pet_name}. "
                    f"Log in to FurBot to schedule a {reminder_type.lower()} appointment: https://furbot.app/login"
)
                suggested.append({"type": reminder_type, "message": message})

        # Update pet with user suggestions, this is in preparation for limiting the number of email suggestions sent
        if suggested:
            pets.update_one(
                {"_id": pet["_id"]},
                {
                    "$set": {
                        "suggestedReminders": suggested,
                        "suggestedReminders_last_sent": today.strftime("%Y-%m-%d")
                    }
                }
            )
            suggestions_made += 1 # Count the number of suggestions made

            # Send email if there is user info
            owner = users.find_one({"_id": owner_id})
            if owner and owner.get("email"):
                subject = f"Reminder for {pet_name}"
                body = "\n\n".join([s["message"] for s in suggested])
                send_email(owner["email"], subject, body)
                print(f"Sent suggestion email to {owner['email']} for {pet_name}") # Console log for debugging

    print(f"Proactive check complete. Pets checked: {pets_found}, Suggestions made: {suggestions_made}") # Console log for debugging

scheduler.add_job(id="check_proactive_reminders", func=check_proactive_reminders, trigger="cron", minute="*") # For testing, run every minute change to hour="1" in production to run at 1 AM.
       

# ------------------------------
# API: Add a new pet
# ------------------------------
@app.route(f"{API_PREFIX}/pets", methods=["POST"])
def add_pet():
    data = request.json

    owner_id = str(data.get("owner_id", "")) ## Get the owner_id from the request data
    # Check if the owner exists

    # Check if required fields are present
    if not owner_id or "name" not in data or "dob" not in data:
        return jsonify({"error": "Missing required fields (owner_id, name, dob)"}), 400
    
    # Validate the owner_id format
    try:
        owner_obj_id = ObjectId(owner_id)
    except Exception:
        return jsonify({"error": "Invalid owner_id format"}), 400
        
    # Check if pet already exists for the owner
    existing_pet = pets.find_one({"owner_id": owner_obj_id, "name": data["name"]})
    if existing_pet:
        return jsonify({"error": "A Pet with this name already exists for the owner"}), 400
        
    # Insert pet into the database
    pet_id = pets.insert_one({
        "owner_id": owner_obj_id,
        "name": data["name"],
        "species": data.get("species", ""),
        "dob": data["dob"],  # (format: YYYY-MM-DD)
        "color": data.get("color", ""),
        "breed": data.get("breed", ""),
        "medical_history": data.get("medical_history", []),
        "created_at": datetime.datetime.now(datetime.timezone.utc)
    }).inserted_id

    return jsonify({"message": "Pet added successfully", "pet_id": str(pet_id)}), 201

# ------------------------------
# API: Get all pets of an owner
# ------------------------------
@app.route(f"{API_PREFIX}/pets/<owner_id>", methods=["GET"])
def get_pets(owner_id):
    try:
        owner_obj_id = ObjectId(owner_id)  # Validate owner_id format
    except Exception:
        return jsonify({"error": "Invalid owner_id format"}), 400

    pets_list = list(pets.find({"owner_id": owner_obj_id}, {"_id": 1, "name": 1, "species": 1, "breed": 1, "dob": 1, "color": 1, "medical_history": 1}))

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
                age -= 1  # Subtract if the birthday hasn't occurred yet
            pet["age"] = age
        else:
            pet["age"] = "Unknown"
    return jsonify(pets_list), 200

# ------------------------------
# API: Delete a pet
# ------------------------------
@app.route(f"{API_PREFIX}/pets/<pet_id>", methods=["DELETE"])
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
# API: User Registration
# ------------------------------
@app.route(f"{API_PREFIX}/register", methods=["POST"])
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
# API: User Login
# ------------------------------
@app.route(f"{API_PREFIX}/login", methods=["POST","OPTIONS"])
@cross_origin(origins=allowed_origins, supports_credentials=True, methods=["POST", "OPTIONS"])
def login():
    if request.method == "OPTIONS":
        return '', 200 # Handle preflight request
    
    try:
        data = request.get_json()
        if not data or "email" not in data or "password" not in data:
            return jsonify({"error": "Invalid request, missing email or password"}), 400
        
        user = users.find_one({"email": data["email"]})
        if not user or not check_password_hash(user["password"], data["password"]):
            return jsonify({"error": "Invalid credentials"}), 401
        
        # Generate a JWT token (valid for 1 hour)
        token = jwt.encode(
            {"email": data["email"], "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)},
            app.config["SECRET_KEY"],
            algorithm="HS256",
        )
        return jsonify({"token": token, "user_id": str(user["_id"])}), 200

    except Exception as e:
        print("Login error:", str(e))
        return jsonify({"error": "Server error"}), 500

# ------------------------------
# API: Chatbot  
# ------------------------------
@app.route(f"{API_PREFIX}/chatbot", methods=["POST"])
def chatbot():
    data = request.json
    user_message = data.get("message", "").lower()

    # Simple chatbot logic
    if "hello" in user_message or "hi" in user_message:
        return jsonify({"reply": "Hello! How can I help you today?"})
    elif "help" in user_message:
        return jsonify({"reply": "I can help you find pet-related services. Try typing 'Find dog groomers'!"})
    else:
        # Additional logic using string matching via Fuzzywuzzy compares the user message with the examples in the database and
        # calculate levenshtein distance to find the best match
        intents = list(db["intents"].find({}))
        best_score = 0
        best_match = None

        for intent in intents:
            for example in intent.get("examples", []):
                score = fuzz.token_set_ratio(user_message, example.lower()) # Compares WORD similarity
                print(f"Comparing with: {example}, Score: {score}")
                if score > best_score:
                    best_score = score
                    best_match = intent

        if best_match and best_score >= 60: # Threshold for a good match
            print("Best Match:", best_match["examples"])
            print("Matched Intent:", best_match["intent"])
            return jsonify({
                "reply": best_match["response"],
                "link": best_match.get("more_info_link", "")
            })
        else:
            return jsonify({"reply": "I'm not sure what you mean. Can you rephrase?"})


# ------------------------------
# Run Flask App
# ------------------------------
with app.app_context():

# Calling the check_reminders and check_proactive_reminders functions once on startup for testing
    with app.app_context():
        check_reminders()  
        check_proactive_reminders() 
    
  
  # Print registered routes for debugging
    print("\nRegistered Routes:")
    for rule in app.url_map.iter_rules():
        print(f"- {rule}")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000)) # Default port is 5000
    app.run(host='0.0.0.0', port=port) # Run the Flask app on the specified port


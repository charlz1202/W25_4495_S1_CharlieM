import os
from sched import scheduler
from flask import Flask, logging, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_mail import Mail, Message
from pymongo import MongoClient
from bson.objectid import ObjectId
import requests
from werkzeug.security import generate_password_hash, check_password_hash
import jwt 
import datetime
from dotenv import load_dotenv
from flask_apscheduler import APScheduler


# Initialize scheduler
scheduler = APScheduler()

# Load environment variables (development)
if os.getenv("FLASK_ENV") != "production":
    load_dotenv()

# Initialize Flask app
app = Flask(__name__, static_folder="../frontend/dist")

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_vue(path):
    if path and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, "index.html")


# Apply CORS to all routes
allowed_origins = os.getenv("CORS_ORIGINS", "*").split(",")
CORS(app, resources={r"/*": {"origins": allowed_origins}}, supports_credentials=True)
    
# Securely load SECRET_KEY from .env
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

# Connect to MongoDB
client = MongoClient(os.getenv("MONGO_URI"))
db = client["furbot"]  # Database name
users = db["users"]  # Users collection
pets = db["pets"] # Pets collection
reminders = db["reminders"] # Reminders collection

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


# ------------------------------
# API: Yelp Search  
# ------------------------------
@app.route("/api/yelp/search", methods=["GET"])
def yelp_search():
    location = request.args.get("location")
    term = request.args.get("term")
    category = request.args.get("category", "petstores,groomer,vets,petservices,petphotography,pet_sitting")

    headers = {
        "Authorization": f"Bearer {YELP_API_KEY}",
        "Content-Type": "application/json"
    }
    url = f"https://api.yelp.com/v3/businesses/search?term={term}&location={location}&categories={category}"

    response = requests.get(url, headers=headers)
    return response.json() if response.status_code == 200 else {"error": "Failed to fetch Yelp data"}

    
# ------------------------------
# API: Add a Reminder
# ------------------------------
@app.route("/reminders", methods=["POST"])
def add_reminder():
    data = request.json

    # Validate input
    if "owner_id" not in data or "pet_id" not in data or "date" not in data:
        print("Missing required fields", data)
        return jsonify({"error": "Missing required fields (owner_id), pet_id, date"}), 400
    
    try:
        owner_obj_id = ObjectId(data["owner_id"])
        pet_obj_id = ObjectId(data["pet_id"])

    except Exception as e:
        print("Invalid owner_id or pet_id format", str(e))
        return jsonify({"error": "Invalid owner_id or pet_id format"}), 400
    
    try: 
        reminder_id = reminders.insert_one({
            "owner_id": owner_obj_id,
            "pet_id": pet_obj_id,
            "date": data["date"], #(format: YYYY-MM-DD)
            "type": data.get("type","Other"),
            "notes": data.get("notes", ""),
            "status": "Pending"
        }).inserted_id

        print("Reminder added successfully", reminder_id)   
        return jsonify({"message": "Reminder added successfully", "reminder_id": str(reminder_id)}), 201

    except Exception as e:
        print("Error adding reminder", str(e))
        return jsonify({"error": "Error adding reminder"}), 500


# ------------------------------
# API: Get Reminders for a pet
# ------------------------------
@app.route("/reminders/<pet_id>", methods=["GET"])
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
        reminder["pet_id"] = str(reminder.get("pet_id","unknown"))

    return jsonify(reminders_list), 200

# ------------------------------
# API: Get All Reminders for an owner
# ------------------------------
@app.route("/reminders/owner/<owner_id>", methods=["GET"])
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
        reminder["pet_id"] = str(reminder.get("pet_id","unknown"))  

    return jsonify(reminders_list), 200

# ------------------------------
# API: Delete a Reminder
# ------------------------------
@app.route("/reminders/<reminder_id>", methods=["DELETE"])
def delete_reminder(reminder_id):
    try:
        reminder_obj_id = ObjectId(reminder_id)  # Validate reminder_id format

    except Exception:
        return jsonify({"error": "Invalid reminder_id format"}), 400
    
    result = reminders.delete_one({"_id": reminder_obj_id})

    if result.deleted_count == 0:
        return jsonify({"error": "Reminder not found"}), 404
    
    return jsonify({"message": "Reminder deleted successfully"}), 200


# -------------------------------------
# JOB: Scheduler for upcoming reminders
# -------------------------------------
def check_reminders():
    today = datetime.datetime.now(datetime.timezone.utc).date()
    
    # Fetch reminders for today
    reminders_list = list(reminders.find({"date": str(today), "status": "Pending"}))

    if not reminders_list:
        logging.info("No reminders for today")
        return

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

            
        # Update reminder status to "Completed"
        reminders.update_one({"_id": reminder["_id"]}, {"$set": {"status": "Completed"}})
        logging.info("Reminder status updated to Completed")

# Schedule the job to run every day at 12:00 AM
scheduler.add_job(id="check_reminders", func=check_reminders, trigger="cron", hour=0, minute=0)
scheduler.start()


# ------------------------------
# API: Manual Test email
# ------------------------------
@app.route("/test_email", methods=["POST"])
def test_email():
    send_email("cm44228@gmail.com", "Test Email", "This is a test email from Furbot") 
    return jsonify({"message": "Test email sent successfully"}), 200    # Return success message


# ------------------------------
# API: Add a new pet
# ------------------------------
@app.route("/pets", methods=["POST"]) 
def add_pet():
    data = request.json

    owner_id = str(data.get("owner_id", ""))

    #Validate input
    if not owner_id or "name" not in data or "dob" not in data:
        return jsonify({"error": "Missing required fields (owner_id), name, dob"}), 400
    
    try:
        owner_obj_id = ObjectId(owner_id) # validate owner_id

    except Exception:
        return jsonify({"error": "Invalid owner_id format"}), 400
        
    # Check if pet already exists for the owner
    existing_pet = pets.find_one({"owner_id": owner_obj_id, "name": data["name"]})
    if existing_pet:
        return jsonify({"error": "A Pet with this name already exists for the owner"}), 400
        
    #Insert pet into the database
    pet_id = pets.insert_one({
        "owner_id": owner_obj_id,
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


    pets_list = list(pets.find({"owner_id": owner_obj_id}, {"_id": 1, "name": 1, "species": 1, "breed": 1, "dob": 1, "color": 1 ,"medical_history": 1}))

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
    try:
        data = request.get_json()
        if not data or "email" not in data or "password" not in data:
            return jsonify({"error": "Invalid request, missing email or password"}), 400
        
        user = users.find_one({"email": data["email"]})


        # Verify password
        if not check_password_hash(user["password"], data["password"]):
            return jsonify({"error": "Invalid credentials"}), 401  
            # Generate a JWT token (valid for 1 hour)
        token = jwt.encode(
            {"email": data["email"], "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)},
               app.config["SECRET_KEY"],
               algorithm="HS256",
            )
        return jsonify({"token": token, "user_id": str(user["_id"])}), 200  # Return token to client

    except Exception as e:
        print("Login error:", str(e))  # Log error
        return jsonify({"error": "Server error"}), 500

# ------------------------------
# API: Chatbot  
# ------------------------------
@app.route("/api/chatbot", methods=["POST"])

def chatbot():
    data = request.json
    user_message = data.get("message", "").lower()

# Simple chatbot logic
    if "hello" in user_message:
        return jsonify({"reply": "Hello! How can I help you today?"})
    elif "help" in user_message:
        return jsonify({"reply": "I can help you find pet-related services. Try typing 'Find dog groomers'!"})
    else:
        return jsonify({"reply": "I'm not sure what you mean. Can you rephrase?"})


   
# ------------------------------
# Run Flask App
# ------------------------------

if __name__ == "__main__":
    env = os.environ.get("FLASK_ENV", "development")  # Default to 'development' if not set
    debug_mode = env == "development"  # Enable debug only in development

    port = int(os.environ.get("PORT", 8080))  # Default to 5000 for local, Railway assigns dynamic port
    host = "localhost" if debug_mode else "0.0.0.0"  # Bind to localhost for local, 0.0.0.0 for production

    print(f"Running in {env} mode on {host}:{port} (Debug: {debug_mode})")
    app.run(host=host, port=port, debug=debug_mode)
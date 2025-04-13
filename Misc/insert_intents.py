from pymongo import MongoClient

# MongoDB connection string
MONGO_URI = "mongodb+srv://cm44228:XMq8lmQDpOUsK2cT@furbot.dmsu2.mongodb.net/"
DB_NAME = "furbot"
COLLECTION_NAME = "intents"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# List of intents
intents = [
    {
        "intent": "pet_travel_canada",
        "examples": [
            "How can I travel with my dog within Canada?",
            "Can I take my dog from Burnaby to Calgary?",
            "Traveling with pets across provinces"
        ],
        "category": "travel",
        "cities": ["Burnaby", "Calgary", "Vancouver", "Toronto"],
        "response": "To travel within Canada with your pet, check transport regulations and ensure vaccination records are updated."
    },
    {
        "intent": "pet_travel_international",
        "examples": [
            "Flying to the US with my cat",
            "Can I bring my dog to the Philippines?",
            "What do I need to travel internationally with my pet?"
        ],
        "category": "travel",
        "cities": [],
        "response": "International pet travel requires health certificates, microchipping, and sometimes quarantine. Let me know the country so I can help more!"
    },
    {
        "intent": "local_services_city",
        "examples": [
            "Pet groomers in Richmond",
            "Where can I take my dog in Burnaby?",
            "Doggy daycare in Vancouver"
        ],
        "category": "services",
        "cities": ["Richmond", "Burnaby", "Vancouver"],
        "response": "Here are some local pet services in your city. Let me know if you're looking for grooming, daycare, or pet boarding!"
    },
    {
        "intent": "grooming_request",
        "examples": [
            "I want to book a grooming session",
            "Where can I get my pet groomed?",
            "Dog grooming service near me"
        ],
        "category": "care",
        "cities": [],
        "response": "Grooming is important for your pet’s hygiene. Would you like me to find grooming services near you or set a reminder?"
    },
    {
        "intent": "vaccination_reminder",
        "examples": [
            "When is my dog's next vaccine?",
            "Remind me about my cat’s vaccination",
            "My puppy needs shots"
        ],
        "category": "care",
        "cities": [],
        "response": "Vaccination reminders help keep your pet healthy! I can check your records or help you set up a reminder."
    },
    {
        "intent": "find_pet_friendly_places",
        "examples": [
            "Pet friendly parks in Vancouver",
            "Where can I take my dog in Richmond?",
            "Dog friendly places in New Westminster"
        ],
        "category": "explore",
        "cities": ["Vancouver", "Richmond", "New Westminster"],
        "response": "Here are some pet-friendly places near you. Let me know if you’re looking for parks, cafes, or stores."
    },
    {
        "intent": "near_me_search",
        "examples": [
            "Any pet stores near me?",
            "Find a dog park nearby",
            "Pet friendly cafes around here"
        ],
        "category": "explore",
        "cities": [],
        "response": "Let me use your location to find pet-friendly spots nearby. Please enable location or provide your city."
    },
    {
        "intent": "pet_care_advice",
        "examples": [
            "How do I clean my dog’s ears?",
            "Tips for brushing my cat’s teeth",
            "Basic pet care guide"
        ],
        "category": "advice",
        "cities": [],
        "response": "Sure! I can give you advice on pet hygiene, diet, grooming, and more. What specifically would you like help with?"
    },
    {
        "intent": "emergency_vet_help",
        "examples": [
            "My dog is sick, what should I do?",
            "Emergency vet near me",
            "Urgent pet help"
        ],
        "category": "emergency",
        "cities": [],
        "response": "If it’s an emergency, please contact the nearest 24/7 animal hospital immediately. I can also list options nearby if needed."
    },
    {
        "intent": "add_pet_profile",
        "examples": [
            "I want to register my new puppy",
            "Add my cat’s profile",
            "How do I enter pet info?"
        ],
        "category": "profile",
        "cities": [],
        "response": "You can register your pet’s profile here. Just give me their name, type, breed, and birthday to get started."
    },
    {
        "intent": "grooming_due_suggestion",
        "examples": [
            "My dog hasn’t had grooming in 3 months",
            "Time for grooming?",
            "When was my pet last groomed?"
        ],
        "category": "care",
        "cities": [],
        "response": "If your pet hasn’t been groomed in a while, it’s probably time! Want to schedule a reminder or find a service near you?"
    },
    {
        "intent": "pet_lost_help",
        "examples": [
            "I lost my dog!",
            "What should I do if my pet goes missing?",
            "Help! My cat ran away"
        ],
        "category": "emergency",
        "cities": [],
        "response": "I'm sorry to hear that! Start by checking local shelters, creating a social media post, and alerting your neighborhood group."
    },
    {
        "intent": "pet_adoption",
        "examples": [
            "Where can I adopt a dog?",
            "Pet adoption centers in Vancouver",
            "I want to adopt a rescue cat"
        ],
        "category": "explore",
        "cities": ["Vancouver", "Toronto", "Calgary"],
        "response": "There are many amazing pets waiting to be adopted! I can list local shelters and adoption centers near you."
    },
    {
        "intent": "pet_training",
        "examples": [
            "How do I train my puppy?",
            "Tips for crate training",
            "Obedience school near me"
        ],
        "category": "care",
        "cities": [],
        "response": "Training is important for a happy and well-behaved pet! I can offer tips or recommend nearby training centers."
    },
    {
        "intent": "pet_first_aid",
        "examples": [
            "What should I do if my dog gets a cut?",
            "First aid for my cat",
            "My puppy injured his paw, help!"
        ],
        "category": "care",
        "cities": [],
        "response": "For minor injuries, gently clean the wound with pet-safe antiseptic and keep the area clean. For anything serious, consult a vet right away."
    },
    {
        "intent": "pet_grooming_basics",
        "examples": [
            "How often should I bathe my dog?",
            "Grooming tips for cats",
            "What’s the best way to brush my dog’s fur?"
        ],
        "category": "care",
        "cities": [],
        "response": "Regular grooming keeps your pet healthy! I can guide you on bathing, brushing, nail trimming, and ear cleaning — just ask!"
    },
    {
        "intent": "pet_diet_nutrition",
        "examples": [
            "What should I feed my puppy?",
            "Best diet for senior cats",
            "Can my dog eat carrots?"
        ],
        "category": "care",
        "cities": [],
        "response": "Pets have different dietary needs based on age, breed, and health. I can help you find the right food or answer nutrition questions!"
    },
    {
        "intent": "default_fallback",
        "examples": [
            "What?",
            "I don’t get it",
            "Can you explain that again?"
        ],
        "category": "fallback",
        "cities": [],
        "response": "Hmm, I’m not sure I understood that. Try asking about pet travel, grooming, reminders, or something else I can help with!"
    }
]


# Insert into MongoDB
result = collection.insert_many(intents)

print(f"{len(result.inserted_ids)} intents inserted successfully into '{COLLECTION_NAME}' collection.")

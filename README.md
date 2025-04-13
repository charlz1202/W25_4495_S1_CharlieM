# W25_4495_S1_CharlieM  
### Project Name: FurBot  

#### Student Information  
**Name:** Charlie Medialdea  
**Student Number:** 300374504  
**Email:** [medialdeac@student.douglascollege.ca](mailto:medialdeac@student.douglascollege.ca)  

---

### FurBot: Your Smart Assistant for Dog Owners  

FurBot is a **web-based chatbot** designed to help dog owners with everyday needs. Whether you're looking for **dog-friendly parks, restaurants, cafes, grooming salons, vet clinics, or supplies**, FurBot has you covered!  

#### Key Features  
-  **Pet Profile Management** – Add, update, or delete pet details (name, age, breed, etc.)  
-  **Reminder System** – Set and view reminders for grooming, vet visits, and vaccinations  
-  **Automated Email Notifications** – Get email alerts for upcoming pet care tasks  
-  **Chatbot Assistance** – Ask questions like “find groomers near me” or “dog-friendly cafes”  
-  **Favorites** – Save your most-used pet service businesses for quick access  
-  **Location Detection** – Uses spaCy NLP and regex to recognize city names from chat input 

#### Built With:  
FurBot is built using a modern full-stack architecture:

### Frontend  
- **Vue.js** – Responsive and dynamic user interface  
- **Axios** – Handles communication between frontend and backend  

### Backend  
- **Python (Flask)** – Lightweight RESTful API framework  
- **Flask-Mail** – Sends email reminders for pet care  
- **spaCy** – NLP library for detecting location-based queries  

### Database  
- **MongoDB** – Stores user profiles, pet information, reminders, and chatbot intents  

### External API Integration  
- **Yelp Fusion API** – Provides listings for dog-friendly businesses like cafes, vets, and grooming salons  

---

## Production Access  

You can try the deployed version of FurBot here:  
[https://furbot-production.up.railway.app](https://furbot-production.up.railway.app)

> *Note:* For full functionality, sign up for an account and explore the pet profile, reminder, and chatbot features directly in the live environment.

---

### Installation Guide (Development)  
FurBot is still in development. Follow these steps to set up and run the project locally:  

#### 1 Download the Project  
   - Clone or download the **Implementation** folder from this GitHub repository:  
     [GitHub Repo](https://github.com/charlz1202/W25_4495_S1_CharlieM)  

#### 2 Open the Project  
   - Launch **Visual Studio Code (VS Code)** and open the downloaded project folder.  

#### 3 Start the Backend Server  
   - Open the **Terminal** in VS Code.  
   - Navigate to the **backend folder**:  
     ```bash
     cd backend
     ```
   - Run the backend:  
     ```bash
     python app.py
     ```  

#### 4 Start the Frontend Server  
   - Open **another Terminal window** in VS Code.  
   - Navigate to the **frontend folder**:  
     ```bash
     cd frontend
     ```
   - Start the frontend development server:  
     ```bash
     npm run dev
     ```  

#### 5 Access the Application  
   - Open **Microsoft Edge** (or any browser).  
   - Go to:  
     ```
     http://localhost:5173/
     ```
   - This will load the homepage of FurBot.  

#### 6 User Registration & Pet Profile Setup  
   - **Sign up** for an account.  
   - Once logged in, you can **add a pet profile** and explore FurBot's features.  

---

### ℹ Notes  
- Ensure **Python** and **Node.js** are installed on your system before running the project.  
- The **backend must be running first** before starting the frontend to avoid errors.  
